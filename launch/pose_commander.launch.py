import os
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("xlerobot", package_name="aharo_moveit_config")
        .robot_description(file_path=os.path.join(get_package_share_directory('xlerobot_description'), 'urdf', 'xlerobot.urdf.xacro'))
        .robot_description_semantic(file_path="config/xlerobot.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .to_moveit_configs()
    )

    pose_commander_node = Node(
        package="aharo_manipulation",
        executable="pose_commander",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([pose_commander_node])
