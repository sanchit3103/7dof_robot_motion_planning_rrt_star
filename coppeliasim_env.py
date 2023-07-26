import sim
import gym
from gym import spaces
import sys
import time
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
from dm_control.utils import rewards

class CoppeliaSim_Env(gym.Env):
    def __init__(self):

        # Connect to CoppeliaSim
        print ('Program started')
        sim.simxFinish(-1) # Close all open connections
        self.clientID = sim.simxStart('127.0.0.1',19997,True,True,5000,5)

        if self.clientID != -1:
            print ('Connected to remote API server')
        else:
            sys.exit('Connection to remote API server unsuccessful')

        # Start simulation
        sim.simxStartSimulation(self.clientID, sim.simx_opmode_oneshot)

        # Obtain all object handles
        self.getObjectHandle()


        # Initialization to obtain object positions and orientation
        self.robot_pos          = self.get_object_pos(self.bf_handle)
        self.initial_cam_pos    = self.get_object_pos(self.global_cam_handle)
        self.initial_cam_orien  = self.get_object_orien(self.global_cam_handle)
        time.sleep(0.1)

        # Initialize camera frames for global and eye cameras
        _, resolution1, image1  = sim.simxGetVisionSensorImage(self.clientID, self.global_cam_handle, 0, sim.simx_opmode_streaming)
        time.sleep(0.2)

        # Initial observation
        self.img1           = np.zeros((3,512,512), dtype = np.uint8)

    def getObjectHandle(self):

        # Object handle for Panda Base Frame
        self.bf_handle   = sim.simxGetObjectHandle(self.clientID, "./base_frame", sim.simx_opmode_blocking)[1]

        # Object handle for Hand robot joints
        self.hand_joint_handle = [0]*7
        for i in range(7):
            jointPath               = "./Franka/Franka_joint" + str(i+1)
            self.hand_joint_handle[i]    = sim.simxGetObjectHandle(self.clientID, jointPath, sim.simx_opmode_blocking)[1]

        # Object handle for Gripper Center Joint of robots
        self.hand_gripper_handle    = sim.simxGetObjectHandle(self.clientID, "./Franka/FrankaGripper_centerJoint", sim.simx_opmode_blocking)[1]

        # Object handle for Global camera
        self.global_cam_handle      = sim.simxGetObjectHandle(self.clientID, "./Cam2", sim.simx_opmode_blocking)[1]

        print(self.hand_joint_handle)

        return 0

    def get_obs(self):

        # Get camera frame of global camera
        _, resolution1, image1  = sim.simxGetVisionSensorImage(self.clientID, self.global_cam_handle, 0, sim.simx_opmode_buffer)


        image1    = np.array(image1, dtype = np.uint8)
        image1.resize([resolution1[0], resolution1[1], 3])
        image1    = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image1    = cv2.flip(image1,0)
        image1    = image1.reshape(3,512,512)
        time.sleep(0.005)

        self.img1   = image1

        return 0

    def get_object_pos(self, _handle):

        _, _pos = sim.simxGetObjectPosition(self.clientID, _handle, -1, sim.simx_opmode_buffer)

        return _pos

    def get_object_orien(self, _handle):

        _, _orien = sim.simxGetObjectOrientation(self.clientID, _handle, -1, sim.simx_opmode_buffer)

        return _orien

    def set_joint_pos(self, _handle, _pos):

        _ = sim.simxSetJointTargetPosition(self.clientID, _handle, _pos, sim.simx_opmode_streaming)
        time.sleep(0.01)

    def set_joint_vel(self, _handle, _vel):

        # Input: Object handle and Joint velocity -> Joint velocity is a scalar value
        # Sets the handle to desired velocity

        _ = sim.simxSetJointTargetVelocity(self.clientID, _handle, _vel, sim.simx_opmode_streaming)
        # time.sleep(0.003)

    def set_object_pos(self, _handle, _pos):

        _ = sim.simxSetObjectPosition(self.clientID, _handle, -1, _pos, sim.simx_opmode_oneshot)

    def set_object_orien(self, _handle, _orien):

        _ = sim.simxSetObjectOrientation(self.clientID, _handle, -1, _orien, sim.simx_opmode_oneshot)

    def reset(self):

        print('Resetting the environment')

        # Initial positions for hand and eye robots
        hand_action     = [0, -0.3, 0, -2.2, 0, 2, 0.78539816]

        for i in range(len(self.hand_joint_handle)):
            self.set_joint_pos(self.hand_joint_handle[i], hand_action[i])

        # Initial observation
        self.get_obs()

        return self.img1

    def step(self, hand_action):

        # assert(self.action_space.contains(action))

        # Set the joints to velocities as per the action received
        # for i in range(len(self.hand_joint_Handle)):
        #     self.set_joint_vel(self.hand_joint_Handle[i], hand_action[i])
        #     self.set_joint_vel(self.eye_joint_Handle[i], eye_action[i])

        # Set the joints to positions as per the action received
        for i in range(len(self.hand_joint_handle)):
            # print(hand_action[i])
            self.set_joint_pos(self.hand_joint_handle[i], hand_action[i])

        # Get griper position
        # self.grip_pos       = self.get_object_pos(self.gripper_Handle)

        # Updated observation and reward computation
        self.get_obs()

        return self.img1

    def restart_simulation(self):

        # Start simulation
        sim.simxStartSimulation(self.clientID, sim.simx_opmode_oneshot)

        # Set the initial position of the red sphere
        self.set_object_pos(self.sph_Handle, self.target_pos)

        # Reset iteration counter
        self.iter_counter       = 0

    def stop_simulation(self):

        # Stop the running simulation
        sim.simxStopSimulation(self.clientID, sim.simx_opmode_oneshot)

        # Wait until the updated status is received
        is_running = True
        while is_running:
            error_code, ping_time = sim.simxGetPingTime(self.clientID)
            error_code, server_state = sim.simxGetInMessageInfo(self.clientID, sim.simx_headeroffset_server_state)
            is_running = server_state & 1
