#Justin Hershberger
#A01381222
#Python 2.7

import argparse
import cv2
import numpy
import math
import sys
import os
import fnmatch

def line_deg_angle(x1, y1, x2, y2):
	dx = x2-x1 
	dy = y2-y1 
	return math.degrees(math.atan2(dy, dx))
	
#method to detect the presence of horizontal lanes
def detect_horizontal_lane(lines):
	hline_count = 0;
	
	for ln in lines:
		for x1,x2,y1,y2 in list(ln):
			#get the degree of each line 
			deg = line_deg_angle(x1,x2,y1,y2)
			#it is a horizontal lane if the degree of the line is 0 or 180
			if (deg >= -15 and deg <= 15)  or (deg >= 165 and deg <= 195):
				#increase the horizontal line count
				hline_count += 1
		
	#if there are at least 2 horizontal lines, we have a lane
	if hline_count >= 2:
		return True;
		#return hline_count / 2;
	

	
def detect_vertical_lane(lines):
	vline_count = 0;
	
	for ln in lines:
		for x1,x2,y1,y2 in list(ln):
			#get the degree of each line 
			deg = line_deg_angle(x1,x2,y1,y2)
			#it is a vertical lane if the degree of the line is 90 or 270
			if (deg >= 75 and deg <= 105)  or (deg >= 255 and deg <= 285):
				#increase the horizontal line count
				vline_count += 1
		
	#if there are at least 2 vertical lines, we have a lane
	if vline_count >= 2:
		return True;
		#return vline_count / 2;
		
def detect_lane_cross(lines, img_h, img_w):
	#create a dictionary to store keys and values
	hline_count = 0
	vline_count = 0
	
	#in order to have a lane cross, we need at least two lanes
	#one horizontal and one vertical.
	if detect_horizontal_lane(lines) and detect_vertical_lane(lines):
		for ln in lines:
			for x1,x2,y1,y2 in list(ln):
				#get the degree of each line 
				deg = line_deg_angle(x1,x2,y1,y2)
				#print 'deg:', deg
				#it is a horizontal lane if the degree of the line is 0 or 180
				if (deg >= -15 and deg <= 15)  or (deg >= 165 and deg <= 195):
					#get the length of the line
					hline_count += 1
					width = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
					#if the length is less than the image's width then the lane ends
						
				if (deg >= 75 and deg <= 105)  or (deg >= -102 and deg <= -75):
					height = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
					vline_count += 1
	else:
		return False
		
	if (vline_count >= 2 and hline_count >= 2):
		return True
	else:
		return False
		

#this is the detect lane end method, it will detect a lane end by checking if the length of the lane 
#is less than either the width, height of the image.
def detect_lane_end(lines, img_h, img_w):
	#check if there is a lane
	if detect_horizontal_lane(lines) or detect_vertical_lane(lines):
		for ln in lines:
			for x1,x2,y1,y2 in list(ln):
				#get the degree of each line 
				deg = line_deg_angle(x1,x2,y1,y2)
				#it is a horizontal lane if the degree of the line is 0 or 180
				if (deg >= -15 and deg <= 15)  or (deg >= 165 and deg <= 195):
					#get the length of the line
					length = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
					#print 'length', length, ' width:', img_w, ' height:', img_h
					#if the length is less than the image's width then the lane ends
					if length < (img_w - 100):
					#check where the lane ending is, if it's closer to the origin or the end, return which lane it is
						if (img_w - y2) > (y2 - 0):
							return True, 'West Lane End'
						else:
							return True, 'East Lane End'
					else:
						return False, 'false'
				elif (deg >= 75 and deg <= 105)  or (deg >= -105 and deg <= -75):
					length = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
					
					#if the length of the lane is less than the height of the image, the lane ends
					if length < (img_h - 100):
						#check where the lane ending is, if it's closer to the origin or the end, return which lane it is
						if (img_h - x2) > (x2 - 0):
							return True, 'South lane end'
						else:
							return True, 'North lane end'
					else:
						return False, 'false'
	else:
		return False, 'false'
				

#this is the detect carpet method, it will return true if there are no lanes in the image
def detect_carpet(lines):
	if lines is None:
		return True
	else:
		return False

		
def classify_frame(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
	image = cv2.imread(image_path)
	gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, 150, apertureSize=3)
	lines = cv2.HoughLinesP(edges, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap)
	height,width,channel = image.shape

	#classify the image by using our methods defined above
	if detect_carpet(lines):
		print('%s\t%s' % (image_path, 'carpet'))
	elif detect_lane_cross(lines, height, width):
		print('%s\t%s' % (image_path, 'lane_cross'))
	elif detect_lane_end(lines, height, width)[0]:
		print('%s\t%s' % (image_path, detect_lane_end(lines, height, width)[1]))
	elif detect_horizontal_lane(lines):
		print('%s\t%s' % (image_path, 'hlane'))
	elif detect_vertical_lane(lines):
		print('%s\t%s' % (image_path, 'vlane'))
		
def classify_frames_in_dir(imgdir, filepat):
	for path, dirlist, filelist in os.walk(imgdir):
		for filename in fnmatch.filter(filelist, filepat):
			fp = os.path.join(path, filename)
			classify_frame(fp, 1, numpy.pi/180, 20, 5, 1)

		
		
if __name__ == '__main__':
	classify_frames_in_dir('LabToElev_Frames_001_151/', '*.png')
