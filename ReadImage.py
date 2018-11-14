import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io



class ReadImage:
	'''This class aids in reading images with the shape (h, w, n) and generate a iterator.'''
	def __init__(self, file_dir=os.getcwd(), file_name='detected_rain.mat', batch_size=10):
		self.file_dir = file_dir
		self.file_name = file_name
		self.batch_size = batch_size
		self.video = None
		self.n = 0

	def Read(self):
		# this reads a video by (h,w,n)
		os.chdir(self.file_dir)
		self.video = scipy.io.loadmat(self.file_name)['R']

	def __next__(self):
		h,w = self.video.shape[:2]
		images = np.zeros((h,w,self.batch_size))
		for i in range(self.batch_size):
			images[:,:,i] = self.video[:,:,i]
			self.n+=1
		if self.n>self.batch_size:
			raise StopIteration
		else:
			return images