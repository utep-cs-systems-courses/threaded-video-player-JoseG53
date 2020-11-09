#!/usr/bin/env python3

import cv2
import os
import threading
import time

class ExtractFrames(threading.Thread):
    def __init__(self, lock, semaphore1, semaphore2, q1= []):
        threading.Thread.__init__(self)
        self.lock = lock
        self.sem1 = semaphore1
        self.sem2 = semaphore2
        self.q1 = q1

    def run(self):
        # globals
        outputDir    = 'frames'
        clipFileName = 'clip.mp4'
        # initialize frame count
        count = 0

        # open the video clip
        vidcap = cv2.VideoCapture(clipFileName)

        # create the output directory if it doesn't exist
        if not os.path.exists(outputDir):
          print(f"Output directory {outputDir} didn't exist, creating")
          os.makedirs(outputDir)

        # read one frame
        success,image = vidcap.read()

        print(f'Reading frame {count} {success}')
        while success:
          # write the current frame out as a jpeg image
          cv2.imwrite("{}/frame_{:04d}.jpg".format(outputDir, count), image)
          success,image = vidcap.read()
          print(f'Reading frame {count}')
          self.sem2.acquire()#ensures queue wont be full
          self.lock.acquire()
          self.q1.append(count)#adds frame to queue
          self.lock.release()
          self.sem1.release()#signals queue population
          count += 1
        self.q1.append(-1)#starts end sequence
        self.sem1.release()
        self.sem2.acquire()
