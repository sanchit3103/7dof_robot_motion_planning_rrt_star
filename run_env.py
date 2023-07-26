import torch
import gym
import numpy as np
import cv2
import faulthandler
import time
from pathlib import Path
from coppeliasim_env import CoppeliaSim_Env

faulthandler.enable()

directory           = Path.cwd()
record_dir          = directory / "record"
record_dir.mkdir(exist_ok=True)

# Initialize environment
env                             = CoppeliaSim_Env()
global_cam_obs                  = env.reset()

# Initialize Camera recordings
resolution1                      = (512, 512)
global_cam_record               = cv2.VideoWriter(str(record_dir) + '/' + 'vid_05' + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, resolution1)

# Save Image and write it to VideoWriter
global_cam_img                  = np.array(global_cam_obs, dtype = np.uint8)

global_cam_img.resize([resolution1[0], resolution1[1], 3])

time.sleep(5)

# Load the actions for both the robots
xs              = np.load("path05.npy")
hand_action     = [0, -0.3, 0, -2.2, 0, 2, 0.78539816]
global_cam_obs  = env.step(hand_action)

global_cam_img  = np.array(global_cam_obs, dtype = np.uint8)
global_cam_img.resize([resolution1[0], resolution1[1], 3])

# Repeat the initial 2 frames, just as a delayed start
for i in range(2):
    global_cam_record.write(global_cam_img)

for i in range(xs.shape[0]):
    print(i)

    hand_action                     = xs[i] * np.pi / 180
    # print(hand_action)

    global_cam_obs                  = env.step(hand_action)

    global_cam_img                  = np.array(global_cam_obs, dtype = np.uint8)
    global_cam_img.resize([resolution1[0], resolution1[1], 3])

    global_cam_record.write(global_cam_img)
    time.sleep(0.1)

time.sleep(1)
hand_action                     = xs[-1]
global_cam_obs                  = env.step(hand_action)

global_cam_img                  = np.array(global_cam_obs, dtype = np.uint8)
global_cam_img.resize([resolution1[0], resolution1[1], 3])

for i in range(10):
    global_cam_record.write(global_cam_img)

global_cam_record.release()

# Stop simulation and close log file once training is completed
env.stop_simulation()
