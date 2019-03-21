import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io
from ReadImage import ReadImage
from RainProperty import RainProperty
import pandas as pd
from datetime import timedelta
import argparse
from glob import glob
import time
import sys
import warnings
if not sys.warnoptions:
	warnings.simplefilter('ignore')
import logging
import datetime


parser= argparse.ArgumentParser('the input file')
parser.add_argument('-f', '--file', type=str, default='20180324144920', help='video file')
file_name= parser.parse_args().file

logging_file= file_name+'-'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.log'
logging.basicConfig(filename=logging_file, filemode= 'w', 
                    format= '%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)

def batch_cal(date, rate_store=True, V_store=False):
	videos= [s.split('\\')[-1] for s in glob(f'./{date}/*.mat')]
	print("Implementing Videos: ", videos)
	exp_date= [s.split('.')[0] for s in videos]
	start= time.time()
	df={}
	df_V= {}
	for video in videos:
		reader= ReadImage(file_dir=f'{date}',file_name= video)
		images,base_date= reader.Read()
		h,w,n= images.shape
		for i in range(n):
			curr_date= (base_date+ timedelta(seconds=1))
			print('current time: ', curr_date)
			store_date= curr_date.strftime('%Y%m%d%H%M%S')
			Para= RainProperty(mat= images[:,:,i], threshold=0.06)
			rain_intensity, V= Para.RainRate()
			df[curr_date]= rain_intensity
			df_V[store_date]= V
			base_date= curr_date
			logging.info(f'{curr_date}:    {rain_intensity}')
	excel_name= date+'-'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.xlsx'
	if rate_store:
		df= pd.DataFrame.from_dict(df, orient='index')
		df.to_excel(excel_name)
	if V_store:
		# df_V= pd.DataFrame.from_dict(df_V,orient='index')
		# df_V.to_excel(f'drop_velocity_{date}.xlsx')
		np.save(f'drop_velocity_{date}.npy',df_V)
	end=time.time()
	print("Total Elapsed time :", round(end-start,2), ' seconds')
	logging.info(f'Model Configuration:\nfocal length:    {Para.focal_len}\nexposure time:    {Para.ex_time}\
		\nfocus distance:    {Para.focus_dist}\nsensor height:    {Para.sensor_h}\nthreshold:    {Para.threshold}\
		\nTime Duration:    {len(videos)*50./60.} minutes\nElapsed time:    {round(end-start,2)} seconds\nstored file name"    {excel_name}')
	return df


def GetRainIntensity(file_name):
	reader = ReadImage(file_name=file_name+'.mat')
	images, date= reader.Read()
	h,w,n= images.shape
	df= {}
	for i in range(n):
		curr_date= (date+ timedelta(seconds=i+1)).strftime('%Y%m%d%H%M%S')
		rain_intensity= RainProperty(mat= images[:,:,i]).RainRate()
		df[curr_date]= rain_intensity
		print(curr_date)
	df= pd.DataFrame.from_dict(df, orient='index')
	df.to_excel(f'{file_name}-{time.time}.xlsx')
	return df

df= batch_cal(file_name, rate_store=True, V_store=True)

# for images, dates in reader.batch_generator():
# 	h,w,n = images.shape
# 	rain_rate=[]
# 	for i in range(n):
# 		single_rain = RainProperty(mat = images[:,:,i])
# 			# single_rain.StreakLength(images[:,:,i], graph=True)
# 		rain_rate.append(single_rain.RainRate())
# 		df[dates[n]]= single_rain.RainRate()
# 	print(f'averaged rain rate for every {batch_size} images are {round(np.asarray(rain_rate).mean(),2)} mm/h')
# print(df)
# df= pd.DataFrame.from_dict(df, orient='index')

# while True:
# 	try:
# 		images = next(reader)
		
# 		rain_rate=[]
# 		for i in range(n):
# 			single_rain = RainProperty(mat = images[:,:,i])
# 			# single_rain.StreakLength(images[:,:,i], graph=True)
# 			rain_rate.append(single_rain.RainRate())
# 		print(f'averaged rain rate for every {batch_size} images are {round(np.asarray(rain_rate).mean(),2)} mm/h')
# 	except StopIteration:
# 		break
# next(reader)
# next(reader)
# next(reader)