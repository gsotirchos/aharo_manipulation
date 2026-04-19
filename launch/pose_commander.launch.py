import os
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("xlerobot", package_name="aharo_moveit_config")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .to_moveit_configs()
    )

    pose_commander_node = Node(
        package="aharo_manipulation",
        executable="pose_commander",
        name="pose_commander",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"planning_pipelines": {"pipeline_names": ["ompl"]}}
        ],
    )

    return LaunchDescription([pose_commander_node])
