import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    sim_dir = get_package_share_directory("robot_sim")

    urdf = DeclareLaunchArgument(name="urdf", 
                                 default_value=os.path.join(sim_dir, "urdf", "watcher.urdf.xacro"),
                                 description="Path to URDF file")
    
    urdf_xacro = ParameterValue(Command(["xacro ", LaunchConfiguration("urdf")]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": urdf_xacro}]
    )

    gz_resource = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(sim_dir).parent.resolve())]
    )

    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource([
        os.path.join(get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
        launch_arguments=[("gz_args", [" -v 4", " -r", " empty.sdf"] )]
    )

    gz_spawner = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "robot_description",
            "-name", "watcher"
        ],
        output="screen"
    )

    gz_timer_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"
        ]
    )

    return LaunchDescription([
        urdf,
        robot_state_publisher,
        gz_resource,
        gazebo,
        gz_spawner,
        gz_timer_bridge
    ])
