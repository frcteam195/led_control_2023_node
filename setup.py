## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['led_control_node'],  #packages=['led_control_node', 'led_control_node.subnode'],
    package_dir={'': 'src'})

setup(**setup_args)