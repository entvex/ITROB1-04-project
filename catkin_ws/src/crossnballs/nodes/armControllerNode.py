#!/usr/bin/python
# coding=utf-8

import rospy
from std_msgs.msg import String
import sys
import crossNballsLib
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryFeedback
from control_msgs.msg import FollowJointTrajectoryResult
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from trajectory_msgs.msg import JointTrajectory
import math

class ArmControllerNode:

    def __init__(self):
        self.subBrinkPlacement = rospy.Subscriber(REQUESTBRINKPLACEMENT_KEY,String,self.callbackBrickPlacment)
        self.pubBrinkPlacement = rospy.Publisher(RESPONDBRICKPLACMENT_KEY,String)
        print REQUESTBRINKPLACEMENT_KEY

    def callbackBrickPlacment(self,data):
        print 'callbackBrickPlacment'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.publish(data.data)

    def publishBrickPlacment(self,data):
        print 'publishBrickPlacment'
        self.pubBrinkPlacement.publish(data)

    def invkin(self,xyz):
        """
        Python implementation of the the inverse kinematics for the crustcrawler
        Input: xyz position
        Output: Angels for each joint: q1,q2,q3,q4

        You might adjust parameters (d1,a1,a2,d4).
        The robot model shown in rviz can be adjusted accordingly by editing au_crustcrawler_ax12.urdf
        """
        print 'invkin'

        d1 = 0.166  # m (height of 2nd joint)
        a1 = 0  # (distance along "y-axis" to 2nd joint)        # Calulate Q2 Q3
        a2 = 0.173  # (distance between 2nd and 3rd joints)
        d4 = 0.065 + 0.165  # (distance from 3rd joint to gripper center - all inclusive, ie. also 4th joint)

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]

        # Calulate Q1
        q1 = math.atan2(y, x)

        # Calulate radius
        r = math.sqrt(math.pow(x - a1 * math.cos(q1), 2) + math.pow(y - a1 * math.sin(q1), 2))
        s = z - d1
        D = (math.pow(r, 2) + math.pow(s, 2) - math.pow(a2, 2) - math.pow(d4, 2)) / (2.*a2*d4)

        # Calulate Q2 Q3
        q3 = math.atan2(-math.sqrt(1 - math.pow(D, 2)), D)
        q2 = math.atan2(s, r) - math.atan2(d4 * math.sin(q3), a2 + d4 * math.cos(q3))

        q4 = 0

        print q1
        print q2
        print q3
        print q4
        # TODO VEND FORTEGN SÅ DEN ER ALBUE OP!!!
        return q1, q2-math.pi/2, q3, q4

    def followJointTrajectoryTest(self):
        print 'followJointTrajectoryTest'
        self.N_JOINTS = 4
        self.client = actionlib.SimpleActionClient("/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)

        self.joint_positions = []
        self.names = ["joint1",
                      "joint2",
                      "joint3",
                      "joint4"
                      ]
        # the list of xyz points we want to plan
        xyz_positions = [
            [0.310426, 0.058854, 0.0],
            [0.23, 0.0, 0.339],
            [0.188102, -0.064624, 0.0],
            [0.23, 0.0, 0.339],
        ]

        # initial duration
        dur = rospy.Duration(1)

        # construct a list of joint positions by calling invkin for each xyz point
        for p in xyz_positions:
            jtp = JointTrajectoryPoint(positions=self.invkin(p), velocities=[0.5] * self.N_JOINTS, time_from_start=dur)
            dur += rospy.Duration(2)
            self.joint_positions.append(jtp)

        self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
        self.goal = FollowJointTrajectoryGoal(trajectory=self.jt, goal_time_tolerance=dur + rospy.Duration(2))

    def send_command(self):
        print 'send_command'
        self.client.wait_for_server()
        print self.goal
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        print self.client.get_result()
    
if __name__ == '__main__':

    #Always load crossNballsLib first
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    rospy.init_node('ArmControllerNode', anonymous=False)
    ArmController = ArmControllerNode()

    x,y = coordinateconverter(304,167)
    print str(x) + " " + str(y)

    print 'followJointTrajectoryTest'
    ArmController.followJointTrajectoryTest()
    ArmController.send_command()

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass