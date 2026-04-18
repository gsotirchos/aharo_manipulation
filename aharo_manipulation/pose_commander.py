import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

# MoveIt configuration will be loaded from the parameter server or via MoveItConfigsBuilder
from moveit.planning import MoveItPy

class PoseCommanderNode(Node):
    def __init__(self):
        super().__init__('pose_commander', allow_undeclared_parameters=True, automatically_declare_parameters_from_overrides=True)
        
        self.get_logger().info("Initializing MoveItPy...")
        
        # We must instantiate MoveItPy using the node's name
        # It relies on the parameters being passed to this node (from launch file)
        self.aharo = MoveItPy(node_name="pose_commander")

        # Get planning components
        self.left_arm = self.aharo.get_planning_component("left_arm")
        self.right_arm = self.aharo.get_planning_component("right_arm")
        
        self.get_logger().info("MoveItPy initialized successfully. Subscribing to target_pose topics.")

        self.left_sub = self.create_subscription(
            PoseStamped,
            '/aharo/left_arm/target_pose',
            self.left_pose_cb,
            10
        )
        
        self.right_sub = self.create_subscription(
            PoseStamped,
            '/aharo/right_arm/target_pose',
            self.right_pose_cb,
            10
        )
        
    def execute_pose(self, arm_component, msg: PoseStamped):
        self.get_logger().info(f"Received target pose for {arm_component.planning_group_name}. Planning...")
        arm_component.set_goal_state(pose_stamped_msg=msg, pose_link=f"Fixed_Jaw{'_2' if arm_component.planning_group_name == 'right_arm' else ''}")
        
        plan_result = arm_component.plan()
        
        if plan_result:
            self.get_logger().info("Path found! Executing...")
            self.aharo.execute(plan_result.trajectory, controllers=[])
        else:
            self.get_logger().error("Path planning failed!")

    def left_pose_cb(self, msg: PoseStamped):
        self.execute_pose(self.left_arm, msg)

    def right_pose_cb(self, msg: PoseStamped):
        self.execute_pose(self.right_arm, msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseCommanderNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
