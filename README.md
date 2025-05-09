# WatcherSD
Autonomous Navigation System.

This guide provides step-by-step instructions for setting up, building, and running the Watcher Wheelchair Simulation using ROS2, Gazebo and RVIZ.

---

## Requirements

Install the following:

```bash
sudo apt update && sudo apt install \
  ros-humble-desktop \
  ros-humble-xacro \
  ros-humble-joint-state-publisher-gui \
  ros-humble-gazebo-ros \
  ros-humble-gazebo-plugins \
  python3-colcon-common-extensions \
  ros-humble-teleop-twist-keyboard
```

---

## Project Structure

```
WatcherProject/
└── WatcherSD/
    ├── src/
    │   └── robot_sim/
    │       ├── launch/
    │       ├── urdf/
    │       │   ├── watcher.urdf.xacro
    │       │   └── depth_camera.xacro
    │       ├── rviz/
    │       └── package.xml
    ├── install/
    ├── build/
    └── log/
```

---

## Step 1: Build the Workspace

```bash
cd ~/WatcherProject/WatcherSD
colcon build
```

---

## Step 2: Source the Workspace

```bash
source install/setup.bash
```

(Optional) Add to your shell:

```bash
echo "source ~/WatcherProject/WatcherSD/install/setup.bash" >> ~/.bashrc
```

---

## Step 3: Launch Simulation in Gazebo

```bash
ros2 launch robot_sim gazebo.launch.py
```

This will:

- Spawn the wheelchair robot with differential drive and casters  
- Load a depth camera with ZED Mini dimensions  
- Spawn in an empty Gazebo world  

---

## Step 4: Control the Robot (Teleop)

In a **new terminal** (don’t forget to source again):

```bash
source ~/WatcherProject/WatcherSD/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


---

## Step 5: View in RViz2

```bash
rviz2
```

### In RViz:
- Set `Fixed Frame` to `base_footprint`
- Add:
  - **RobotModel**
  - **Image** → Topic: `/depth_camera/depth_camera/image_raw`
  - **DepthCloud** or **PointCloud2** → Topic: `/depth_camera/depth_camera/points`

---

## Step 6: Check Topics

```bash
ros2 topic list | grep camera
ros2 topic echo /depth_camera/depth_camera/image_raw
```

---

## Step 7: Visualize Odometry

1. In RViz:
   - Add **TF**
   - Add **Odometry**  
     → Topic: `/odom`  
     → Fixed Frame: `odom`

2. You can also echo odom data:

```bash
ros2 topic echo /odom
```

---

## Cleanup and Rebuild

```bash
rm -rf build/ install/ log/
colcon build
source install/setup.bash
```

---

## Troubleshooting

### Gazebo won't start:
```bash
killall -9 gzserver gzclient
```

### Plugin missing?
Ensure this is installed:

```bash
sudo apt install ros-humble-gazebo-plugins
```

---

## 📝 Notes

- The camera is modeled to match ZED Mini dimensions: `0.1245 × 0.0265 × 0.0305 m`
- All caster joints are `revolute` for realistic pivoting
- The differential drive plugin handles velocity commands from `cmd_vel`

---

## Contributing

New teammates should:
1. Clone the repo inside the `WatcherSD/src` directory
2. Run the build and launch steps above
3. Use this README to get up and running quickly