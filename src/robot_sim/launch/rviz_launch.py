from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
import os

def generate_launch_description():

    watcher_model = DeclareLaunchArgument(
        name="watcher_model",
        default_value=os.path.join(get_package_share_directory("robot_sim"), "urdf", "watcher.urdf.xacro"),
        description="Path to Watcher URDF File"
    )

    model_parameter = ParameterValue(Command(["xacro ", LaunchConfiguration("watcher_model")]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": model_parameter}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(get_package_share_directory("robot_sim"), "rviz", "config.rviz")]
    )

    return LaunchDescription([
        watcher_model,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])
