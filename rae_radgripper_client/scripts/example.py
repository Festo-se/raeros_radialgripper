#! /usr/bin/env python3


from raerospy_radgripper_client.RadialgripperClient import RadialgripperClient
import time
import rospy

if __name__ == "__main__":
    r = RadialgripperClient()
    r.calibrate()
    time.sleep(1)
    r.to(0.1)
    time.sleep(1)
    r.grasp()
    time.sleep(1)
    r.to(0.2)