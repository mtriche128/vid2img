#!/usr/bin/python

# author: Matthew Triche
# brief : converts frames within a video to a series of image files

# -----------------------------------------------------------------------------
# import modules

import cv2
import cv2.cv as cv
import argparse
import sys
import time

# -----------------------------------------------------------------------------
# define main function

def main():

	# ----- parse arguments -----
	
	parse = argparse.ArgumentParser(description="Video to image converter.")
	parse.add_argument("video_file", help="input video file name")
	parse.add_argument("output_dir", help="output directory for images")
	parse.add_argument("-i", dest='skip_int', type=int, default=1, help="frame skip interval, only every i'th frame is written to disk")
	parse.add_argument("-o", dest='img_name', default="image", help="base string used in the file name for output images")

	args = parse.parse_args()
	video_file = args.video_file
	output_dir = args.output_dir
	skip_int   = int(args.skip_int)
	img_name   = args.img_name
	
	# ----- ouput run parameters -----
	
	print("Video File   : %s" % video_file)
	print("Skip Interval: %s" % skip_int)
	print("Output Name  : %s" % img_name)
	
	# ----- open video -----
	
	cap = cv2.VideoCapture(video_file)
	
	if not(cap.isOpened()):
		print("Failed to open video!")
		exit(1)
	
	# ----- get camera properties -----

	total_frames = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
	frame_width  = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
	frame_height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

	print("Total Frames : %i" % total_frames)
	print("Resolution   : %ix%i" % (frame_width,frame_height))
	
	# ----- read frames -----
	
	frame_index = 0
	fail_count  = 0
	write_count = 0
		
	while(frame_index < total_frames):
		
		# make sure the video is still open (sanity check)
		if not(cap.isOpened()):
			print("\r\nVideo closed unexpectedly!")
			break
		
		retval, frame = cap.read() # read next frame
		
		# check if the frame was read successfully
		if not(retval):
			# the frame wasn't successfully read, increment the fail count
			fail_count += 1

		else:
			# the frame was successfully read, check if it should be skipped or written to an image
			if (frame_index % skip_int) == 0:
				cv2.imwrite(output_dir + "/" + img_name + "%0.6i.jpg" % write_count, frame)
				write_count += 1
		
		frame_index += 1
		sys.stdout.write("fames read: %6i, failed reads: %6i        \r" % (frame_index,fail_count))
		
	print("\r\ndone")
	
# -----------------------------------------------------------------------------
# run script

if __name__ == '__main__':
	main()
