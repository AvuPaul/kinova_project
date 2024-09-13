from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from launch_ros.actions import PushRosNamespace
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            default_value="192.168.100.20",
            description="IP address by which the robot can be reached.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument("dof", default_value="7", description="DoF of robot.")
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="false",
            description="Start robot with fake hardware mirroring command to its states.",
        )
    )

    # Get the path to the gen3.launch.py file
    gen3_launch_file_dir = get_package_share_directory('kortex_bringup')    
    gen3_launch_file_path = os.path.join(gen3_launch_file_dir, 'launch', 'gen3.launch.py')

    # Include the original gen3.launch.py with a namespace
    include_gen3_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gen3_launch_file_path),
        launch_arguments={
            'robot_ip': LaunchConfiguration('robot_ip'),
            'dof': LaunchConfiguration('dof'),
            'use_fake_hardware': LaunchConfiguration('use_fake_hardware')
        }.items(),
    )

    return LaunchDescription(declared_arguments + [
        PushRosNamespace('kinova'),
        include_gen3_launch
    ])