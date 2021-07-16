from rae_radgripper_messages.srv import calibrate, grasp
import rae_radgripper_messages.msg

import rospy
import actionlib


class RadialgripperClient(object):
    def __init__(self):
        rospy.wait_for_service("/rae_radgripper_server/GripperCalibration")
        self.calibrate = rospy.ServiceProxy("/rae_radgripper_server/GripperCalibration",calibrate)
        rospy.wait_for_service("/rae_radgripper_server/Grasp")
        self.__grasp_service = rospy.ServiceProxy("/rae_radgripper_server/Grasp",grasp)
        self.__radgripper_client = actionlib.SimpleActionClient('/rae_radgripper_server/GripperMoveAction', rae_radgripper_messages.msg.GraspAction)
        self.__radgripper_client.wait_for_server()

    def grasp(self,speed=360,current=900):
        return self.__grasp_service(speed=speed, current=current)

    def to(self,position,current=900):
        goal = rae_radgripper_messages.msg.GraspGoal(position=position,current=current)
        self.__radgripper_client.send_goal(goal)
        self.__radgripper_client.wait_for_result()
        return self.__radgripper_client.get_result()

    
