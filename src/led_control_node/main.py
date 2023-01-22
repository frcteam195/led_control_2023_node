#!/usr/bin/env python3

import rospy
from threading import Thread

from frc_robot_utilities_py_node.frc_robot_utilities_py import *
from frc_robot_utilities_py_node.RobotStatusHelperPy import RobotStatusHelperPy, Alliance, RobotMode, BufferedROSMsgHandlerPy
from ck_ros_msgs_node.msg import Led_Control
from ck_utilities_py_node.led import LEDColor, LEDControlMode, LEDStrip, LEDStripType, RGBWColor, LEDAnimation, AnimationType, Direction

def ros_func():
    control_subscriber = BufferedROSMsgHandlerPy(Led_Control)
    control_subscriber.register_for_updates("LedControl")

    test_timer = 0

    rate = rospy.Rate(20)

    rospy.loginfo("LED")
    test_strip = LEDStrip(0, LEDStripType.RGBW)
    red = LEDColor(RGBWColor(R=255), 0, 8)
    green = LEDColor(RGBWColor(G=255), 0, 8)
    blue = LEDColor(RGBWColor(B=255), 0, 8)

    test_strip.setLEDControlMode(LEDControlMode.Animated)
    test_strip.setLEDAnimations([LEDAnimation(0, 1, 1, 8, RGBWColor(200, 50, 255, 100), AnimationType.Rainbow, Direction.Forward, 0, 0)])



    while not rospy.is_shutdown():

        # if control_subscriber.get() is not None:
        #     if control_subscriber.get().control_mode == Led_Control.SET_LED:
        #         test_strip.setLEDControlMode(LEDControlMode.Static)
        #         test_strip.setLEDColor(LEDColor(RGBWColor(control_subscriber.get().red, control_subscriber.get().green, control_subscriber.get().blue, control_subscriber.get().white), 0, control_subscriber.get().number_leds))
                
        #     else:
        #         #Animate Code
        pass
            

        # Set LEDs as a Test Every 5 Seconds or so...
            
        #if test_timer > 100:
            #test_strip.setLEDControlMode(LEDControlMode.Static)
            #test_strip.setLEDColor(green)
            #test_timer = 0
            
        #test_timer -= 1

        rate.sleep()


def ros_main(node_name):
    rospy.init_node(node_name)
    register_for_robot_updates()

    t1 = Thread(target=ros_func)
    t1.start()

    rospy.spin()

    t1.join(5)