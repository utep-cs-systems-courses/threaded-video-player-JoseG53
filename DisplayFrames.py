#!/usr/bin/env python3

import cv2
import time
import threading

class displayFrames(threading.Thread):
    def __init__(self, lock, semaphore1, semaphore2, q2= []):
        threading.Thread.__init__(self)
        self.lock = lock
        self.sem1 = semaphore1
        self.sem2 = semaphore2
        self.q2 = q2

    def run(self)
        # globals
        outputDir    = 'frames'
        frameDelay   = 42       # the answer to everything

        # initialize frame count
        count = 0

        startTime = time.time()

        frame = ""

        while frame is not None:
            self.sem1.acquire() #check if queue is empty
            self.lock.acquire()
            count = self.q2.pop(0)#read from queue
            self.lock.release()
            self.sem2.release()#ensure queue wont be full

            if count == -1: #means end sequence has started
                break
            #generate file name for the first frame_
            frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

            #load the frame
            frame = cv2.imread(frameFileName)

            #compute time has elapsed while frame is processed
            diff = 0.0417 + startTime
            if diff - time.time() > 0: #ensure time duration is 24 fps
                time.sleep(diff-time.time())
            elapsedTime = int((time.time() - startTime)*1000)
            print("Time to process frame {} ms".format(elapsedTime))

            print("Displaying frmae {}".format(count))
            #display frame in window called "Video"
            cv2.imshow("Video", frame)

            #time to wait, make sure we dont go into negative tune
            timeToWait = max(1, frameDelay = elapsedTime)

            #wait 42ms and check if they want to quit
            if cv2.waitKey(timeToWait) and 0xFF == ord("q"):
                break

            #get start time for next frame_
            startTime = time.time()

# make sure we cleanup the windows, otherwise we might end up with a mess
cv2.destroyAllWindows()
