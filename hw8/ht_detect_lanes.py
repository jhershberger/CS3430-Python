## Python 2.7
## Justin Hershberger
## The angle bounds that worked best for me are between -45 deg to 135 deg 
## I found that the lower the num_votes, min_len, max_gap, the more false positives 
## In analyzing the data, I found that the more precise I try to get with detection,
## the less likely I was to detect a lane. This means that in order to have success 
## in detection, we need to allow for more chances of false positives. I'm sure there are 
## bounds that allow for the most precise detection but I don't think it is a perfect detection
## but with great minds pursuing a solution, we will one day find a near perfect solution
## until then, I will be slightly hesitant towards autonomous vehicles.
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

## >>> line_deg_angle(1, 1, 5, 5)
##45.0
##>>> line_deg_angle(0, 5, 5, 0)
##-45.0

def unit_test_01(x1, y1, x2, y2):
	print line_deg_angle(x1, y1, x2, y2)

def draw_ht_lines_in_image(image, lines, color, line_thickness):
    try:
        for ln in lines:
            x1, y1, x2, y2 = ln[0]
            cv2.line(image, (x1, y1), (x2, y2), color, line_thickness)
    except Exception as e:
        print str(e)

def display_lines_and_angles(lines):
    try:
        for ln in lines:
            x1, y1, x2, y2 = ln
            print (x1, y1, x2, y2), line_deg_angle(x1, y1, x2, y2)
    except Exception as e:
        print str(e)

def display_ht_lines_and_angles(lines):
    try:
        for ln in lines:
            x1, y1, x2, y2 = ln[0]
            print (x1, y1, x2, y2), line_deg_angle(x1, y1, x2, y2)
    except Exception as e:
        print str(e)

def is_angle_in_range(a, ang_lower, ang_upper):
	if a >= ang_lower and a <= ang_upper:
		return True
	else:
		return False

def is_left_lane_line(x1, y1, x2, y2, ang_lower, ang_upper):
	deg = line_deg_angle(x1,y1,x2,y2)
	in_range = is_angle_in_range(deg, ang_lower, ang_upper)
	return in_range

def is_right_lane_line(x1, y1, x2, y2, ang_lower, ang_upper):
	deg = line_deg_angle(x1,y1,x2,y2)
	in_range = is_angle_in_range(deg, ang_lower, ang_upper)
	return in_range

def display_ht_lanes_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    image = cv2.imread(image_path) ## read the image
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ## grayscale
    edges = cv2.Canny(gray, 50, 150, apertureSize=3) ## detect edges
    lines = cv2.HoughLinesP(edges, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap) ## detect hough lines
    print 'Detected lines and angles:'
    display_ht_lines_and_angles(lines)
    draw_ht_lines_in_image(image, lines, (255, 0, 0), 2)
    cv2.imshow('Gray',  gray)
    cv2.imshow('Edges', edges)
    cv2.imshow('Lines in Image', image)
    cv2.waitKey(0)

def unit_test_02(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    display_ht_lanes_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap)

def filter_left_lane_lines(lines, ang_lower=-45, ang_upper=45):
	return [(x1,x2,y1,y2) for l in lines for x1,x2,y1,y2 in list(l) if is_left_lane_line(x1,x2,y1,y2, ang_lower, ang_upper)]

def filter_right_lane_lines(lines, ang_lower=45, ang_upper=135):
	return [(x1,x2,y1,y2) for l in lines for x1,x2,y1,y2 in list(l) if is_right_lane_line(x1,x2,y1,y2, ang_lower, ang_upper)]

## most common value for rho_accuracy is 1
## most common value for theta_accuracy is numpy.pi/180.
def plot_ht_lanes_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    image = cv2.imread(image_path) ## read the image
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ## grayscale
    edges = cv2.Canny(gray, 50, 150, apertureSize=3) ## detect edges
    lines = cv2.HoughLinesP(edges, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap) ## detect hough lines
    display_lines_and_angles(lines)
    cv2.imshow('Gray',  gray)
    cv2.imshow('Edges', edges)
    ll_lines = filter_left_lane_lines(lines)
    rl_lines = filter_right_lane_lines(lines)
    draw_lines_in_image(image, ll_lines, (255, 0, 0), 2)
    draw_lines_in_image(image, rl_lines, (0, 0, 255), 2)
    print 'detected', len(ll_lines), 'left lanes'
    print 'detected', len(rl_lines), 'right lanes'
    cv2.imshow('Lanes in Image', image)
    cv2.waitKey(0)

def detect_ht_lanes_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    image = cv2.imread(image_path) ## read the image
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ## grayscale
    edges = cv2.Canny(gray, 50, 150, apertureSize=3) ## detect edges
    lines = cv2.HoughLinesP(edges, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap) ## detect hough lines
    ll_lines = filter_left_lane_lines(lines)
    rl_lines = filter_right_lane_lines(lines)
    draw_lines_in_image(image, ll_lines, (255, 0, 0), 2)
    draw_lines_in_image(image, rl_lines, (0, 0, 255), 2)
    cv2.imwrite(image_path[:-4] + '_lanes' + image_path[-4:], image)
    return (len(ll_lines), len(rl_lines))

def unit_test_03(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    ll, rl = detect_ht_lanes_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap)
    print 'number of left lanes:', ll
    print 'number of right lanes:', rl
    
def find_ll_rl_lanes_in_images_in_dir(imgdir, filepat, rho_acc, th_acc, num_votes, min_len, max_gap):
	images = [file for file in os.listdir(imgdir) if fnmatch.fnmatch(file, filepat)]
	for img in images:
		yield (img, detect_ht_lanes_in_image(imgdir + '/' + img, rho_acc, th_acc, num_votes, min_len, max_gap))


def unit_test_04(imgdir, filepat, rho_acc, th_acc, num_votes, min_len, max_gap):
	for fp, ll_rl in find_ll_rl_lanes_in_images_in_dir(imgdir, filepat, 1, numpy.pi/180, num_votes, min_len, max_gap):
		print fp, ll_rl[0], ll_rl[1]
	   
def draw_lines_in_image(image, lines, color, line_thickness):
    try:
        for ln in lines:
            x1, y1, x2, y2 = ln
            cv2.line(image, (x1, y1), (x2, y2), color, line_thickness)
    except Exception as e:
        print str(e)
		
def display_lines_and_angles(lines):
    try:
        for ln in lines:
            x1, y1, x2, y2 = list(ln)
            print (x1, y1, x2, y2), line_deg_angle(x1, y1, x2, y2)
    except Exception as e:
        print str(e)
    
if __name__ == '__main__':
    #unit_test_01(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    #plot_ht_lanes_in_image(sys.argv[1], 1, numpy.pi/180, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    #unit_test_02(sys.argv[1], int(sys.argv[2]), numpy.pi/180, int(sys.argv[3]))
    #unit_test_03(sys.argv[1], 1, numpy.pi/180, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    unit_test_04(sys.argv[1], sys.argv[2], 1, numpy.pi/180, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    #numpy_opencv_ht_test(sys.argv[1])






