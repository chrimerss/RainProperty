import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io


from ReadImage import ReadImage
from RainProperty import RainProperty

reader = ReadImage()
reader.Read()
while True:
	try:
		images = next(reader)
		h,w,n = images.shape
		rain_rate=[]
		for i in range(n):
			single_rain = RainProperty(mat = images[:,:,i])
			# single_rain.StreakLength(images[:,:,i], graph=True)
			rain_rate.append(single_rain.RainRate())
		print(f'averaged rain rate for every 10 images are {round(np.asarray(rain_rate).mean(),2)} mm/h')
	except StopIteration:
		break
# next(reader)
# next(reader)
# next(reader)
