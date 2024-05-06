#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose, Twist
from gazebo_msgs.msg import ModelState
from nav_msgs.msg import Odometry

def obstacle_publisher():
    rospy.init_node('obstacle_publisher', anonymous=True)
    obstacle_pub = rospy.Publisher('/obstacle', Odometry, queue_size=10)
    obstacle_model_pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    rate = rospy.Rate(500)  # 500Hz

    # Initial state
    obstacle_state = Odometry()
    obstacle_state.pose.pose.position.x = 4
    obstacle_state.pose.pose.position.y = 4
    obstacle_state.pose.pose.position.z = 0

    obstacle_twist = Twist()
    obstacle_twist.linear.x = -0.3
    obstacle_twist.linear.y = -0.3
    obstacle_twist.linear.z = 0

    obstacle_state.twist.twist.linear.x = obstacle_twist.linear.x
    obstacle_state.twist.twist.linear.y = obstacle_twist.linear.y

    model_state = ModelState()
    model_state.model_name = "cylinder_0"
    model_state.pose = obstacle_state.pose.pose
    model_state.twist = obstacle_twist

    while not rospy.is_shutdown():
        # Update model state
        model_state.pose.position.x += obstacle_twist.linear.x * (1.0 / 500)
        model_state.pose.position.y += obstacle_twist.linear.y * (1.0 / 500)

        # Publish to gazebo
        obstacle_model_pub.publish(model_state)

        # Publish to /obstacle
        obstacle_state.header.stamp = rospy.Time.now()
        obstacle_pub.publish(obstacle_state)

        rate.sleep()

if __name__ == '__main__':
    try:
        obstacle_publisher()
    except rospy.ROSInterruptException:
        pass
