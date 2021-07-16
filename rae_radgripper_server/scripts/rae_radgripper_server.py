#! /usr/bin/env python3

import rospy

from raerospy_radgripper.RadialGripperServer import RadialGripperServer

if __name__ == "__main__":
    rospy.init_node('rae_radialgripper_server')
    RadialGripperServer()
    rospy.spin()