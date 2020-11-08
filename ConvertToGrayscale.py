#!/usr/bin/env python3

import cv2
import threading
import time

class GrayScaleThread(threading.Thread):
    def __init__(self, lock, semaphore1, semaphore2, semaphore3, semaphore4, q1=[], q2= []):
        threading.Thread.__init__(self)
        self.lock = lock
        self.sem1 = semaphore1
        self.sem2 = semaphore2
        self.sem3 = semaphore3
        self.sem4 = semaphore4
        self.q1 = q1
        self.q2 = q2

    def run(self):
        #globals
        outputDir = 'frames'

        #init frame count
        count = 0
        inputFrame = ""

        while inputFrame is not None:
            self.sem1.acquire() #check if queue is empty
            self.lock.acquire()
            count = self.q1.pop(0) #retrieves from queue
            self.lock.release()
            self.sem2.release() # ensures queue wont be full

            if count == -1:#check if end sequence has started
                self.q2.append(-1)
                self.sem3.release()
                break
            #get next frame from file
            inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

            #load the next file
            inputFrame = cv2.inread(inFileName, cv2.IMREAD_COLOR)

            print("Converting Frame {}".format(count))

            #convert the image to GrayScale
            grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

            #generate output file name
            outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

            #write outputfile
            cv2.imwrite(outFileName, grayscaleFrame)
            self.sem4.acquire()#check if q2 is full
            self.lock.acquire()
            self.q2.append(count)#recieve from q2
            self.lock.release()
            self.sem3.release()#signaling q2 wont be empty
