#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Twist

def move():
	'''
	if len(sys.argv) == 1:
		print('hello there')
	else:
		for i in range(len(sys.argv)-1):
			print 'Argument',i+1, 'is:',sys.argv[i+1]
	'''

	#Initializing node
	rospy.init_node('goddamn_move_robot',anonymous=True)
	#node publishes to /turtle1/cmd_vel topic
	velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	#Initializing a Twist message
	vel_msg = Twist()
	


	#continuous input until a non-integer is entered
	print 'Enter input: '

	while(True):
		try:
			dist = int(raw_input('Input dist: '))
		except ValueError:
			break
		if dist < 0:
			vel_msg.linear.x = -1		#reverse		
		elif dist > 0:
			vel_msg.linear.x = 1		#forward	
		else:
			break

		#All other velocities are 0
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0
		
		dist = dist * 0.1
		
		#Current time
		t0 = float(rospy.Time.now().to_sec())
		current_distance = 0		

		#keep moving with prescribed velocity until required distance is reached
		while(current_distance < abs(dist)):			
			velocity_publisher.publish(vel_msg)
			t1 = float(rospy.Time.now().to_sec())			
			current_distance = abs(vel_msg.linear.x * (t1 - t0))
		
		#Forcing all velocities to be 0
		vel_msg.linear.x = 0
		velocity_publisher.publish(vel_msg)


if __name__=='__main__':
	try:
		move()
	except rospy.ROSInterruptException:		#If ^c is pressed, then node closes with no error
		pass
