import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Include aharo_sim sim.launch.py
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('aharo_sim'), 'launch', 'sim.launch.py')
        )
    )

    # 2. Include aharo_manipulation pose_commander.launch.py
    manipulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('aharo_manipulation'), 'launch', 'pose_commander.launch.py')
        )
    )

    # 3. Publish the target pose message
    publish_pose = ExecuteProcess(
        cmd=[
            'ros2', 'topic', 'pub', '-1',
            '/aharo/right_arm/target_pose', 'geometry_msgs/msg/PoseStamped',
            "{header: {frame_id: 'base_footprint'}, pose: {position: {x: -0.4, y: 0.1, z: 0.495}, orientation: {x: 0.0, y: 0.707, z: 0.0, w: 0.707}}}"
        ],
        output='screen'
    )

    # Delay the publish command by 12 seconds to allow Gazebo and MoveIt to fully start
    delayed_pub = TimerAction(
        period=12.0,
        actions=[publish_pose]
    )

    return LaunchDescription([
        sim_launch,
        manipulation_launch,
        delayed_pub
    ])