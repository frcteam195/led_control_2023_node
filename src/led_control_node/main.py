#!/usr/bin/env python3

import rospy
from threading import Thread

from frc_robot_utilities_py_node.frc_robot_utilities_py import *
from frc_robot_utilities_py_node.RobotStatusHelperPy import BufferedROSMsgHandlerPy
from ck_ros_msgs_node.msg import Led_Control
from ck_utilities_py_node.led import LEDColor, LEDControlMode, LEDStrip, LEDStripType, RGBWColor, LEDAnimation, AnimationType, Direction


def ros_func():
    control_subscriber = BufferedROSMsgHandlerPy(Led_Control)
    control_subscriber.register_for_updates("LedControl")

    rate = rospy.Rate(20)

    leds = LEDStrip(0, LEDStripType.RGBW)

    while not rospy.is_shutdown():

        if control_subscriber.get() is not None:

            color = RGBWColor(control_subscriber.get().red, control_subscriber.get().green, control_subscriber.get().blue, control_subscriber.get().white)

            if control_subscriber.get().control_mode == Led_Control.SET_LED:
                leds.setLEDControlMode(LEDControlMode.Static)
                leds.setLEDColor(LEDColor(color, 0, control_subscriber.get().number_leds))
            else:
                animation = LEDAnimation(0, control_subscriber.get().brightness, control_subscriber.get().speed,
                                         control_subscriber.get().number_leds, color, control_subscriber.get().animation)

                leds.setLEDControlMode(LEDControlMode.Animated)
                leds.setLEDAnimations([animation])

        rate.sleep()


def ros_main(node_name):
    rospy.init_node(node_name)
    register_for_robot_updates()

    t1 = Thread(target=ros_func)
    t1.start()

    rospy.spin()

    t1.join(5)
