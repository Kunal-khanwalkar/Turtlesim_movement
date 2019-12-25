#!/usr/bin/env python
import sys
import os
import tty
import termios
import rospy
from geometry_msgs.msg import Twist


#getch() function reads the stdin file continuously and return the file details simultaneously
#With this function we can get continuous keyboard input, and move the turtlebot/model using keyboard (or any keyboard input)
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(3)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


#For rectilinear movement
def translate(direction):
	
	if direction == 0:
		vel_msg.linear.x = -1
	else:
		vel_msg.linear.x = 1					

	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	
	t0 = float(rospy.Time.now().to_sec())
	current_distance = 0		

	while(current_distance < abs(0.1)):			
		velocity_publisher.publish(vel_msg)
		t1 = float(rospy.Time.now().to_sec())			
		current_distance = abs(vel_msg.linear.x * (t1 - t0))
	
	vel_msg.linear.x = 0
	velocity_publisher.publish(vel_msg)


#For rotation
def rotate(direction):

	if direction == 0:
		vel_msg.angular.z = -30 * 2*3.1415/360
	else:
		vel_msg.angular.z = 30 * 2*3.1415/360

	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0

	angle = 10 * 2*3.1415/360


	t0 = float(rospy.Time.now().to_sec())
	current_distance = 0		

	while(current_distance < abs(angle)):			
		velocity_publisher.publish(vel_msg)
		t1 = float(rospy.Time.now().to_sec())			
		current_distance = abs(vel_msg.angular.z * (t1 - t0))
	
	vel_msg.angular.z= 0
	velocity_publisher.publish(vel_msg)



def main():
	
	#Loop closes as soon as a key is pressed
	while True:	
		inp = getch()
		if inp != '':
			break
	
	#Up arrow key
	if inp=='\x1b[A':	
		translate(1)

	#Up down key	
	elif inp=='\x1b[B':
		translate(0)

	#Up left key	
	elif inp=='\x1b[C':
		rotate(0)

	#Up right key	
	elif inp=='\x1b[D':
		rotate(1)
	
	else:
		print "exiting"	
		exit()


if __name__=='__main__':
	#Initializing node and publishing it to /cmd_vel topic
	#To use with turtlesim, change the topic to /turtle1/cmd_vel
	rospy.init_node('fucking_move_robot',anonymous=True)
	velocity_publisher = rospy.Publisher('turtle1/cmd_vel',Twist,queue_size=10)
	vel_msg = Twist()

	#Continuously taking keyboard input	
	print 'Taking input: '
	while True:
		main()


