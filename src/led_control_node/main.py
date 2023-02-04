import rospy
from threading import Thread

from frc_robot_utilities_py_node.BufferedROSMsgHandlerPy import BufferedROSMsgHandlerPy
from ck_ros_msgs_node.msg import Led_Control
from ck_utilities_py_node.led import AnimationType, LEDAnimation, LEDColor, LEDControlMode, LEDStrip, LEDStripType, RGBWColor


class LedControlNode():
    """
    The LED Control Node.
    """

    def __init__(self) -> None:

        self.animation_map = {
            Led_Control.COLOR_FLOW: AnimationType.ColorFlow,
            Led_Control.FIRE: AnimationType.Fire,
            Led_Control.LARSON: AnimationType.Larson,
            Led_Control.RAINBOW: AnimationType.Rainbow,
            Led_Control.RGB_FADE: AnimationType.RGBFade,
            Led_Control.SINGLE_FADE: AnimationType.SingleFade,
            Led_Control.TWINKLE: AnimationType.Twinkle,
            Led_Control.TWINKLE_OFF: AnimationType.TwinkleOff,
            Led_Control.STROBE: AnimationType.Strobe
        }

        self.control_subscriber = BufferedROSMsgHandlerPy(Led_Control)
        self.control_subscriber.register_for_updates("LedControl")

        self.leds = LEDStrip(0, LEDStripType.RGBW)

        loop_thread = Thread(target=self.loop)
        loop_thread.start()

        rospy.spin()

        loop_thread.join(5)

    def loop(self) -> None:
        """
        Periodic function for the LED Control Node.
        """
        rate = rospy.Rate(20)

        while not rospy.is_shutdown():

            if self.control_subscriber.get() is not None:
                control_message: Led_Control = self.control_subscriber.get()

                color = RGBWColor(control_message.red,
                                  control_message.green,
                                  control_message.blue,
                                  control_message.white)

                if control_message.control_mode == Led_Control.SET_LED:
                    self.leds.setLEDControlMode(LEDControlMode.Static)
                    self.leds.setLEDColor(LEDColor(color, 0, control_message.number_leds))
                else:
                    animation = LEDAnimation(0, control_message.brightness,
                                             control_message.speed,
                                             control_message.number_leds,
                                             color,
                                             self.animation_map[control_message.animation])

                    self.leds.setLEDControlMode(LEDControlMode.Animated)
                    self.leds.setLEDAnimations([animation])

            rate.sleep()
