#python 2.7
#I think that the correlation between temp and luminosity is 
# that the lower the temperature, the lower the luminosity and 
# vice versa

import argparse
import cv2
import sys 
import os 
import fnmatch 
import re

ap = argparse.ArgumentParser() 
ap.add_argument('-lf', '--lum_file', required = True, help = 'Path to lum file') 
ap.add_argument('-tf', '--temp_file', required = True, help = 'Path to temp file') 
args = vars(ap.parse_args())

## define regexes 
lum_entry_pat  = r'\d*-\d*-*\d*_(\d*?)-\d*-\d*.\w*\s(\d*\.\d+)'
temp_entry_pat = r'\d*-\d*-*\d*_(\d*?)-\d*-\d*\s(\d*\.\d+)'

## define two dictionaries 
lum_tbl = {} 
tmp_tbl = {}

with open(args['lum_file']) as infile:
  for line in infile:
    m = re.match(lum_entry_pat, line)
    if m != None:
	  if m.group(1) in lum_tbl:
		lum_tbl[str(m.group(1))].append(float(m.group(2)))
	  else:
		lum_tbl[str(m.group(1))] = [float(m.group(2))]

with open(args['temp_file']) as infile:
  for line in infile:
    m = re.match(temp_entry_pat, str(line))
    if m != None:
	  if m.group(1) in tmp_tbl:
		tmp_tbl[str(m.group(1))].append(float(m.group(2)))
	  else:
		tmp_tbl[str(m.group(1))] = [float(m.group(2))]
		
## print tables and averages
sys.stdout.write('Luminosity Table' + '\n')
for h, lums in lum_tbl.items():
  sys.stdout.write(str(h) + '-->' + str(lums) + '\n')
sys.stdout.write('\n')

sys.stdout.write('Temperature Table' + '\n') 
for h, temps in tmp_tbl.items():
  sys.stdout.write(str(h) + '-->' + str(temps) + '\n')
sys.stdout.write('\n')

sys.stdout.write('Luminosity Averages' + '\n') 
for h, lums in lum_tbl.items():
  sys.stdout.write(str(h) + '-->' + str(sum(lums)/len(lums)) + '\n') 
sys.stdout.write('\n')

sys.stdout.write('Temperature Averages' + '\n') 
for h, temps in tmp_tbl.items():
  sys.stdout.write(str(h) + '-->' + str(sum(temps)/len(temps)) + '\n')
sys.stdout.flush()
