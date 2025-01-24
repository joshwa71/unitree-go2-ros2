
import os

import launch_ros
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_joy = LaunchConfiguration("use_joy")
    dev = LaunchConfiguration("dev")
    
    declare_use_joy = DeclareLaunchArgument("use_joy", default_value="true", description="Use joy or keyboard")
    declare_dev = DeclareLaunchArgument("dev", default_value="/dev/input/js0", description="Path to joystick dev port")
    declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false", description="Use simulation (Gazebo) clock if true")

    joy = Node(
        package="joy",
        executable="joy_node",
        name="joy_node",
        output="screen",
        parameters=[{
            'use_sim_time': use_sim_time,
            'dev': dev,
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
            }]
    )

    champ_teleop = Node(
        package="champ_teleop",
        executable="champ_teleop.py",
        name="champ_teleop",
        output="screen",
        parameters=[{
            'use_sim_time': use_sim_time,
            'joy': True
            }]
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_use_joy,
        declare_dev,
        joy,
        champ_teleop
    ])
