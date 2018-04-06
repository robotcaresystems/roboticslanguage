#!/bin/bash

# setup the environment
source /opt/ros/kinetic/setup.bash

# install pip
curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
rm get-pip.py

# install the catkin tools
pip install catkin_tools

# install the Robotics Language
pip install -e .

# create the catkin workspace
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin init
catkin build

# set the development path
mkdir -p ~/.rol
echo "globals:\n  deploy: /root/catkin_ws/src/deploy" > ~/.rol/parameters.yaml

# compile the example
rol /RoL/RoboticsLanguage/Examples/helloworld.rol -c

# source the new code to be able to launch
source ~/catkin_ws/devel/setup.bash

cd /RoL
