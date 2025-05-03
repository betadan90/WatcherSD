#!/usr/bin/env python3
import cv2
import numpy as np
import pyzed.sl as sl
from ultralytics import YOLO

# Create ZED camera object
zed = sl.Camera()

# Define initialization parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.camera_fps = 30
init_params.coordinate_units = sl.UNIT.METER
init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE

# Open camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
        print(f"Error opening ZED camera: {err}")
        exit()

# Enable spatial tracking for depth and point cloud
tracking_param = sl.PositionalTrackingParameters()
zed.enable_positional_tracking(tracking_param)

obj_detection_params = sl.ObjectDetectionParameters()
err = zed.enable_object_detection(obj_detection_params)
if err != sl.ERROR_CODE.SUCCESS:
        print(f"Error enabling spatial tracking: {err}")
        exit()

# objects = sl.Objects()
# obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
# obj_runtime_param.detection_confidenece_threshold = 30

#cv2.nameWindow("ZED", cv2.WINDOW_NORMAL)


# Create Mat object to store the RGB image
img = sl.Mat()

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

while True:
    # Grab new frame from the ZED camera
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        #zed.retrieve_objects(objects, obj_runtime_param)
        # Retrieve RGB image
        zed.retrieve_image(img, sl.VIEW.LEFT)
        img_cv = img.get_data()

        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGRA2BGR)
        img_rgb = img_cv[:, :, :3]

        results = model(img_rgb)

        # if objects.is_new:
        #     obj_arr = objects.object_list
        #     print(str(len(obj_arr)))

        #     for obj in obj_arr:
        #         top_left = obj.bounding_box_2d[0]
        #         bottom_right = obj.bounding_box_2d[2]

        #         cv2.rectangle(img_cv, (int(top_left[0]), int(top_left[1])), (int(bottom_right[0]), int(bottom_right[1])), (0, 255, 0), 2)

        #         label = f"{obj.label} ({int(obj.confidence)}%)"

        #         cv2.putText(img_cv, label, (int(top_left[0]), int(top_left[1]-10)))


        for result in results:
            boxes = result.boxes.cpu().numpy()  # Add parentheses to call the method
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                label = f'{class_name}: {confidence:.2f}'
                cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img_cv, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the image with detections
        cv2.imshow("YOLOv8 Object detection with ZED", img_cv)

        # Press 'q' to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
         print("Error grabbing frame")
         break

# Close camera
zed.disable_object_detection()
zed.close()
cv2.destroyAllWindows()