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
import time


class ArmControllerNode:
    def __init__(self):
        self.waitForResponse = False
        self.DEFAULT_POS = [0.0, 0.0, 0.569]

        self.subBrinkPlacement = rospy.Subscriber(REQUEST_BRICKPLACEMENT_KEY, String, self.callbackBrickPlacment)
        self.pubBrinkPlacement = rospy.Publisher(RESPOND_BRICKPLACMENT_KEY, String)

        self.subGripper = rospy.Subscriber(RESPOND_GRIPPER_KEY, String, self.callbackGrip)
        self.pubGripper = rospy.Publisher(REQUEST_GRIPPER_KEY, String)

        self.boardPositions = [[255, 111],[306, 111],[361, 111],
                               [254, 165],[307, 164],[362, 164],
                               [255, 217],[307, 217],[362, 217]]

    def callbackGrip(self, data):
        self.waitForResponse = False


    def callbackBrickPlacment(self, data):
        if data.data == "DEFAULT_POS":
            self.moveToDefaultPosition()
            self.send_command()
            self.pubBrinkPlacement.publish("done")

        else :
            coordinate = data.data.split(',', 3)

            x = float(coordinate[0])
            y = float(coordinate[1])

            self.followJointTrajectoryTest(x=x,y=y)
            self.send_command()

            self.waitForResponse = True
            self.pubGripper.publish("GRIP")
            self.waitResponse()

            self.moveToDefaultPosition()
            self.send_command()

            # Place on board
            time.sleep(2)

            self.followJointTrajectoryTest(x=float(self.boardPositions[int(coordinate[2])][0]), y=float(self.boardPositions[int(coordinate[2])][1]))
            self.send_command()

            self.waitForResponse = True
            self.pubGripper.publish("RELEASE")
            self.waitResponse()

            self.moveToDefaultPosition()
            self.send_command()

            time.sleep(4)

            self.pubBrinkPlacement.publish("done")

    def publishBrickPlacment(self, data):
        self.pubBrinkPlacement.publish(data)

    def invkin(self, xyz):
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
        D = (math.pow(r, 2) + math.pow(s, 2) - math.pow(a2, 2) - math.pow(d4, 2)) / (2. * a2 * d4)

        # Calulate Q2 Q3
        q3 = math.atan2(-math.sqrt(1 - math.pow(D, 2)), D)
        q2 = math.atan2(s, r) - math.atan2(d4 * math.sin(q3), a2 + d4 * math.cos(q3))

        q4 = 0

        print q1
        print q2
        print q3
        print q4
        return q1, q2 - math.pi / 2, q3, q4

    def followJointTrajectoryTest(self,x=0,y=0):
        self.N_JOINTS = 4
        self.client = actionlib.SimpleActionClient("/arm_controller/follow_joint_trajectory",
                                                   FollowJointTrajectoryAction)

        self.joint_positions = []
        self.names = ["joint1",
                      "joint2",
                      "joint3",
                      "joint4"
                      ]
        # the list of xyz points we want to plan
        newX, newY = self.coordinateconverter(x,y)

        xyz_positions = [[newX, newY, 0.13],[newX, newY, 0.023]]

        # initial duration
        dur = rospy.Duration(1)

        for p in xyz_positions:
        # construct a list of joint positions by calling invkin for each xyz point
            jtp = JointTrajectoryPoint(positions=self.invkin(p), velocities=[0.5] * self.N_JOINTS, time_from_start=dur)
            dur += rospy.Duration(2)
            self.joint_positions.append(jtp)

        self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
        self.goal = FollowJointTrajectoryGoal(trajectory=self.jt, goal_time_tolerance=dur + rospy.Duration(2))

    def moveToDefaultPosition(self):
        self.N_JOINTS = 4
        self.client = actionlib.SimpleActionClient("/arm_controller/follow_joint_trajectory",
                                                   FollowJointTrajectoryAction)

        self.joint_positions = []
        self.names = ["joint1",
                      "joint2",
                      "joint3",
                      "joint4"
                      ]
        # initial duration
        dur = rospy.Duration(2)

        # construct a list of joint positions by calling invkin for each xyz point
        jtp = JointTrajectoryPoint(positions=self.invkin(self.DEFAULT_POS), velocities=[0.5] * self.N_JOINTS,
                                   time_from_start=dur)
        dur += rospy.Duration(2)
        self.joint_positions.append(jtp)

        self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
        self.goal = FollowJointTrajectoryGoal(trajectory=self.jt, goal_time_tolerance=dur + rospy.Duration(2))

    def send_command(self):
        self.client.wait_for_server()
        self.client.send_goal(self.goal)
        self.client.wait_for_result()

    def coordinateconverter(self,x, y):
        self.convertConstant = 0.001139

        xOffset = 300.00
        yOffset = 384.00

        newX = -(y - yOffset) * self.convertConstant
        newY = -(x - xOffset) * self.convertConstant

        return newX, newY

    def waitResponse(self):
        while self.waitForResponse:
            time.sleep(1)

if __name__ == '__main__':

    # Always load crossNballsLib first
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    rospy.init_node('ArmControllerNode', anonymous=False)
    ArmController = ArmControllerNode()
    time.sleep(1)

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass