# Refactored version of mbzirc_demo.launch.py

# The description of a launch-able system
from launch import LaunchDescription

# Actions allow user to express intent.
# Similar to argparse - specifies command-line args with `ros2 launch`
from launch.actions import DeclareLaunchArgument
# Used to include/source a Python launch file from elsewhere
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node

import mbzirc_ign.bridges

def generate_launch_description():

    # These arguments are passed directly to the standard ign_gazeob.launch.py
    ign_args = LaunchConfiguration('ign_args')
    ign_args_arg = DeclareLaunchArgument(
        'ign_args', default_value='',
        description='Arguments to be passed to Ignition Gazebo')

    # Include the standard ignition launch file with arguments
    ign_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('ros_ign_gazebo'),
                                  'launch',
                                  'ign_gazebo.launch.py'
            ])
        ]),
        launch_arguments = {'ign_args': ign_args}.items())


    # Ingition bridge
    bridges = [
      mbzirc_ign.bridges.score(),
      mbzirc_ign.bridges.clock(),
      mbzirc_ign.bridges.run_clock(),
      mbzirc_ign.bridges.phase(),
      mbzirc_ign.bridges.stream_status(),
    ]
    ibridge = Node(package='ros_ign_bridge',
                   executable='parameter_bridge',
                   output='screen',
                   arguments=[bridge.argument() for bridge in bridges],
                   remappings=[bridge.remapping() for bridge in bridges])
    
    return LaunchDescription([ign_args_arg,
                              ign_gazebo,
                              ibridge])


