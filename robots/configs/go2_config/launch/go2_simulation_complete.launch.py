import os

import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    GroupAction,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    # === Gazebo simulation parameters ===
    use_sim_time = LaunchConfiguration("use_sim_time")
    description_path = LaunchConfiguration("description_path")
    base_frame = "base_link"

    config_pkg_share = launch_ros.substitutions.FindPackageShare(
        package="go2_config"
    ).find("go2_config")
    descr_pkg_share = launch_ros.substitutions.FindPackageShare(
        package="go2_description"
    ).find("go2_description")
    champ_description_share = launch_ros.substitutions.FindPackageShare(
        package="champ_description"
    ).find("champ_description")
    
    # Paths to configurations
    joints_config = os.path.join(config_pkg_share, "config/joints/joints.yaml")
    ros_control_config = os.path.join(
        config_pkg_share, "/config/ros_control/ros_control.yaml"
    )
    gait_config = os.path.join(config_pkg_share, "config/gait/gait.yaml")
    links_config = os.path.join(config_pkg_share, "config/links/links.yaml")
    default_model_path = os.path.join(descr_pkg_share, "xacro/robot_mid360_camera.xacro")
    default_world_path = os.path.join(config_pkg_share, "worlds/simple_environment.world")
    rviz_config_path = os.path.join(champ_description_share, "rviz/urdf_viewer.rviz")

    # === FAST-LIO parameters ===
    fastlio_pkg_path = get_package_share_directory('fast_lio')
    default_fastlio_config_path = os.path.join(fastlio_pkg_path, 'config')
    default_fastlio_rviz_config_path = os.path.join(
        fastlio_pkg_path, 'rviz', 'fastlio.rviz')
    
    fastlio_config_path = LaunchConfiguration('fastlio_config_path')
    fastlio_config_file = LaunchConfiguration('fastlio_config_file')
    fastlio_rviz_use = LaunchConfiguration('fastlio_rviz')
    fastlio_rviz_cfg = LaunchConfiguration('fastlio_rviz_cfg')
    fastlio_delay = LaunchConfiguration('fastlio_delay')

    # Declare all launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock if true",
    )
    declare_rviz = DeclareLaunchArgument(
        "rviz", default_value="true", description="Launch RViz for robot visualization"
    )
    declare_robot_name = DeclareLaunchArgument(
        "robot_name", default_value="go2", description="Robot name"
    )
    declare_lite = DeclareLaunchArgument(
        "lite", default_value="false", description="Lite"
    )
    declare_ros_control_file = DeclareLaunchArgument(
        "ros_control_file",
        default_value=ros_control_config,
        description="Ros control config path",
    )
    declare_gazebo_world = DeclareLaunchArgument(
        "world", default_value=default_world_path, description="Gazebo world name"
    )
    declare_gui = DeclareLaunchArgument(
        "gui", default_value="true", description="Use Gazebo GUI"
    )
    declare_world_init_x = DeclareLaunchArgument("world_init_x", default_value="0.0")
    declare_world_init_y = DeclareLaunchArgument("world_init_y", default_value="-3.0")
    declare_world_init_z = DeclareLaunchArgument("world_init_z", default_value="0.275")
    declare_world_init_heading = DeclareLaunchArgument(
        "world_init_heading", default_value="1.57"
    )
    
    # FAST-LIO launch arguments
    declare_fastlio_config_path = DeclareLaunchArgument(
        'fastlio_config_path', default_value=default_fastlio_config_path,
        description='FAST-LIO Yaml config file path'
    )
    declare_fastlio_config_file = DeclareLaunchArgument(
        'fastlio_config_file', default_value='unitree_go2_mid360.yaml',
        description='FAST-LIO Config file'
    )
    declare_fastlio_rviz = DeclareLaunchArgument(
        'fastlio_rviz', default_value='false',
        description='Use separate RViz for FAST-LIO (set to false to use main RViz)'
    )
    declare_fastlio_rviz_config_path = DeclareLaunchArgument(
        'fastlio_rviz_cfg', default_value=default_fastlio_rviz_config_path,
        description='FAST-LIO RViz config file path'
    )
    declare_fastlio_delay = DeclareLaunchArgument(
        'fastlio_delay', default_value='5.0',
        description='Delay in seconds before starting FAST-LIO (to ensure proper initialization)'
    )

    # Define included launch files
    # CHAMP bringup
    bringup_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("champ_bringup"),
                "launch",
                "bringup.launch.py",
            )
        ),
        launch_arguments={
            "description_path": default_model_path,
            "joints_map_path": joints_config,
            "links_map_path": links_config,
            "gait_config_path": gait_config,
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "robot_name": LaunchConfiguration("robot_name"),
            "gazebo": "true",
            "lite": LaunchConfiguration("lite"),
            "rviz": LaunchConfiguration("rviz"),
            "joint_controller_topic": "joint_group_effort_controller/joint_trajectory",
            "hardware_connected": "false",
            "publish_foot_contacts": "false",
            "close_loop_odom": "true",
        }.items(),
    )

    # Gazebo
    gazebo_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("champ_gazebo"),
                "launch",
                "gazebo.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "robot_name": LaunchConfiguration("robot_name"),
            "world": LaunchConfiguration("world"),
            "lite": LaunchConfiguration("lite"),
            "world_init_x": LaunchConfiguration("world_init_x"),
            "world_init_y": LaunchConfiguration("world_init_y"),
            "world_init_z": LaunchConfiguration("world_init_z"),
            "world_init_heading": LaunchConfiguration("world_init_heading"),
            "gui": LaunchConfiguration("gui"),
            "close_loop_odom": "true",
        }.items(),
    )
    
    # Add a static transform publisher between livox and camera_init frames
    static_transform_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='livox_to_camera_init_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'livox', 'camera_init']
    )
    
    # FAST-LIO mapping (with delay)
    fast_lio_node = Node(
        package='fast_lio',
        executable='fastlio_mapping',
        parameters=[PathJoinSubstitution([fastlio_config_path, fastlio_config_file]),
                    {'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # Delay the start of FAST-LIO to ensure simulation is properly initialized
    delayed_fast_lio = TimerAction(
        period=fastlio_delay,
        actions=[fast_lio_node]
    )
    
    # FAST-LIO RViz (optional, use a separate condition)
    fastlio_rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='fastlio_rviz',
        arguments=['-d', fastlio_rviz_cfg],
        condition=IfCondition(fastlio_rviz_use)
    )
    
    # Also delay the start of FAST-LIO RViz
    delayed_fastlio_rviz = TimerAction(
        period=fastlio_delay,
        actions=[fastlio_rviz_node]
    )

    return LaunchDescription(
        [
            # Gazebo parameters
            declare_use_sim_time,
            declare_rviz,
            declare_robot_name,
            declare_lite,
            declare_ros_control_file,
            declare_gazebo_world,
            declare_gui,
            declare_world_init_x,
            declare_world_init_y,
            declare_world_init_z,
            declare_world_init_heading,
            
            # FAST-LIO parameters
            declare_fastlio_config_path,
            declare_fastlio_config_file,
            declare_fastlio_rviz,
            declare_fastlio_rviz_config_path,
            declare_fastlio_delay,
            
            # Launch files
            bringup_ld,
            gazebo_ld,
            
            # Static transforms needed for FAST-LIO
            static_transform_publisher,
            
            # FAST-LIO nodes (with delay)
            delayed_fast_lio,
            delayed_fastlio_rviz,
        ]
    ) 