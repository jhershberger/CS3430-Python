from __future__ import division
import argparse 
import cv2 
import sys 
import os 
import fnmatch 
import re

ap = argparse.ArgumentParser() 
ap.add_argument('-id', '--idir', required = True, help = 'Path to image') 
args = vars(ap.parse_args())

## a function you may want to use in debugging
def display_image_pix(image, h, w):
  image_pix = list(image)
  for r in xrange(h):
    for c in xrange(w):
      print list(image_pix[r][c]), ' ',
    print
		
## luminosity conversion
def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
    return rcoeff*rgb[0]+gcoeff*rgb[1]+bcoeff*rgb[2]

def compute_avrg_luminosity(imagepath):
    image = cv2.imread(imagepath)
    (h, w, num_channels) = image.shape
    image_pix = list(image)
    sum_luminosity = 0
    num_pixels = 0
	
    # compute the luminosity of each pixel in the image
    for row in xrange(h):
      for col in xrange(w):
		num_pixels += 1
		sum_luminosity += luminosity(list(image_pix[row][col]))
	
    return sum_luminosity / num_pixels

def gen_avrg_lumin_for_dir(imgdir, filepat):
  images = [file for file in os.listdir(imgdir) if fnmatch.fnmatch(file, filepat)]
  for img in images:
	yield (str(img), compute_avrg_luminosity(imgdir + '/' + str(img)))
  
  
	
## run ghe generator and output into STDOUT
for fp, lum_avrg in gen_avrg_lumin_for_dir(args['idir'], r'*.png'):
  sys.stdout.write(fp + '\t'  + str(lum_avrg) + '\n')
  sys.stdout.flush()
