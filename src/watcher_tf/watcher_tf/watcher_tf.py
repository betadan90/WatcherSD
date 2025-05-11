import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


class WatcherTF(Node):
    def __init__(self):
        super().__init__("watcher_tf")
        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.update_tf, 10)

    def update_tf(self, msg: Odometry):
        transform_msg = TransformStamped()
        transform_msg.header.stamp = msg.header.stamp
        transform_msg.header.frame_id = 'odom'
        transform_msg.child_frame_id = 'base_link'
        transform_msg.transform.translation.x = msg.pose.pose.position.x
        transform_msg.transform.translation.y = msg.pose.pose.position.y
        transform_msg.transform.translation.z = msg.pose.pose.position.z
        transform_msg.transform.rotation = msg.pose.pose.orientation
        self.tf_broadcaster.sendTransform(transform_msg)


def main():
    rclpy.init()
    watcher_TF = WatcherTF()
    rclpy.spin(watcher_TF)
    watcher_TF.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
