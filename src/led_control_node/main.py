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
            control_msg : Led_Control = control_subscriber.get()
            color = RGBWColor(control_msg.red, control_msg.green, control_msg.blue, control_msg.white)



            if control_msg.control_mode == Led_Control.SET_LED:
                leds.setLEDControlMode(LEDControlMode.Static)
                leds.setLEDColor(LEDColor(color, 0, control_msg.number_leds))
            else:
                animation = LEDAnimation(0, control_msg.brightness, control_msg.speed,
                                         control_msg.number_leds, color, control_msg.animation)

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
