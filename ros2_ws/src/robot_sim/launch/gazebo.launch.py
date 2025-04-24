from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
import os

def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_directory('robot_sim'),
        'urdf',
        'watcher.urdf.xacro'
    )

    return LaunchDescription([
        # Launch Gazebo with the factory plugin (so we can spawn robot later)
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Publish the robot description to /robot_description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_path])
            }]
        ),

        # Spawn the robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'watcher', '-topic', 'robot_description'],
            output='screen'
        )
    ])