#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Twist


def move():
	rospy.init_node('goddamn_move_robot',anonymous=True)
	velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	vel_msg = Twist()

	print 'Enter input: '

	while(True):
		try:
			dist = int(raw_input('Input degrees: '))
		except ValueError:
			break
	
		#Converting 30 degrees to radians, clockwise or anticlockwise
		if dist < 0:
			vel_msg.angular.z = -30 * 2*3.1415/360		
		else:
			vel_msg.angular.z = 30 * 2*3.1415/360

		vel_msg.linear.x=0
		vel_msg.linear.y=0
		vel_msg.linear.z=0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0

		#Converting degree angle to radians
		angle = dist * 2*3.1415/360


		t0 = float(rospy.Time.now().to_sec())
		current_distance = 0		

		#Keep rotating with prescribed angular velocity until rotation is complete
		while(current_distance < abs(angle)):			
			velocity_publisher.publish(vel_msg)
			t1 = float(rospy.Time.now().to_sec())			
			current_distance = abs(vel_msg.angular.z * (t1 - t0))
		
		#Force angular velocity to be 0
		vel_msg.angular.z= 0
		velocity_publisher.publish(vel_msg)

if __name__=='__main__':
	try:
		move()
	except rospy.ROSInterruptException:		#No error when ^c
		pass
