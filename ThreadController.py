#!/usr/bin/env python3

#importing all threads
from ExtractFrames import *
from ConvertToGrayScale import *
from DisplayFrames import *
import threading

lock = threading.Lock()
list1 = [] #list to convert to grayscale_
list2 = [] #list to display

#init and start threads

semaphore1 = threading.Semaphore(0)
semaphore2 = threading.Semaphore(10)
semaphore3 = threading.Semaphore(0)
semaphore4 = threading.Semaphore(10)
extractThread = ExtractFrames(lock, semaphore1, semaphore2, list1)
ConvertToGrayScale = GrayScaleThread(lock, semaphore1, semaphore2, semaphore3, semaphore4, list1, list2)
DisplayThread = displayFrames(lock, semaphore3, semaphore4, list2)
extractThread.start()
ConvertToGrayScale.start()
DisplayThread.start()
