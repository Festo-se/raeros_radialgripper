import rae_radgripper_messages.msg
from rae_radgripper_messages.srv import calibrate, grasp
from raepy import RadialGripper
import rospy
import actionlib

gripper = RadialGripper()

class RadialGripperServer(object):
    def __init__(self):
        self._action_name = "~GripperMoveAction"
        self._feedback = rae_radgripper_messages.msg.GraspActionFeedback().feedback
        self._result = rae_radgripper_messages.msg.GraspActionResult().result
        self._gripper_action = actionlib.SimpleActionServer(self._action_name, rae_radgripper_messages.msg.GraspAction, execute_cb=self.execute_move_gripper, auto_start=False)
        self._gripper_action.start()

        self._calibration_service_name = "~GripperCalibration"
        self._calibration_service = rospy.Service(self._calibration_service_name, calibrate, self.calibration_request_handler)
        rospy.loginfo("%s: initialized" % self._action_name)

        rospy.Service("~Grasp", grasp, self.grasp_service_request)
        rospy.loginfo("%s: initialized" % "~Grasp")

    def execute_move_gripper(self, goal):
        rospy.loginfo("%s: launched" % self._action_name)
        self._goal_position = goal.position
        gripper.to(self._goal_position, current=goal.current, cb=self._move_feedback_cb)
        self._result.done = True
        self._gripper_action.set_succeeded(self._result)
        rospy.loginfo('%s: Succeeded' % self._action_name)


    def _move_feedback_cb(self, initial_angle, goal_angle, actual_angle):
        # preempting routine
        if self._gripper_action.is_preempt_requested():
            rospy.loginfo('%s: Preempted' % self._action_name)
            self._gripper_action.set_preempted()
            return False

        self._feedback.percentage = self._calculate_percentage(initial_angle, goal_angle, actual_angle)
        self._gripper_action.publish_feedback(self._feedback)
        rospy.loginfo('%s: Executing, Gripper Move to Position %f is at %i ' , self._action_name, self._goal_position, self._feedback.percentage)
        return True


    def calibration_request_handler(self,req):
        gripper.calibrate()
        rospy.loginfo("{0}: Grasping Calibration done".format(self._calibration_service_name))
        return True

    def _calculate_percentage(self,initial, goal, actual):
        return int((1-(abs(goal - actual)/abs(initial-goal))) * 100)+1

    def grasp_service_request(self,req):
        gripper.grasp(speed=req.speed,current=req.current)
        return True

