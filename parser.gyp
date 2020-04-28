#!/usr/bin/env python

import os, sys, getopt
import csv
from os import path

def main(argv):
    inputfolder = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifolder=","ofile="])
    except getopt.GetoptError:
        print ("test.py -i <input folder path> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("test.py -i <input folder path> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            if not path.exists(arg):
                print ("The input folder %s does not exist!" % arg)
                sys.exit()
            inputfolder = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    print ("Input folder is ", inputfolder)
    print ("Output file is ", outputfile)

    with open (outputfile, 'w', newline='') as f_save:
        #csv_writer = csv.writer(f_save, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['timeline', 'FPS', 'Average resolution', 'Video Type']
        csv_writer = csv.DictWriter(f_save, fieldnames=fieldnames)
        csv_writer.writeheader()

        # setup variables
        final_frame_width = 0
        final_fps = 0
        total_seconds = 1
        video_type = "N/A"
        # Search all files that file name starting with libva
        for root, dirs, files in os.walk(inputfolder):
            for file in files:
                if file.startswith("libva"):
                    print(os.path.join(root, file))
                    f = open(os.path.join(root, file), 'r')
                    previous_timeline = 0
                    fps_counter = 1
                    acc_frame_width = 0
                    while True:
                        # Avoid running out of memory, read file by 8M chunk
                        lines = f.readlines(8*1024*1024)
                        if not lines:
                            break

                        for line in lines:
                            # The format is [xxx][xxxx]yyyyyy
                            x = line.split("[")
                            # Length of the array == 3 is what we need
                            if len(x) == 3:
                                timeline = x[1].split("]")[0]
                                data = x[2].split("]")[1]
                                # Video type starts with --VAPictureXXX\n
                                if "--VAPicture" in data:
                                    video_type = data.split('--')[1].strip('\n')
                                if "frame_width" in data:
                                    # Ingore fraction
                                    current_timeline = int(timeline.split('.')[0])
                                    if previous_timeline != current_timeline:
                                        # this is a new frame, we should reset the count
                                        # and calcualate the FPS
                                        previous_timeline = current_timeline
                                        csv_writer.writerow({"timeline": current_timeline, "FPS" : fps_counter, "Average resolution" : acc_frame_width/fps_counter, "Video Type": video_type})
                                        
                                        final_fps += fps_counter
                                        final_frame_width += acc_frame_width/fps_counter
                                        total_seconds += 1
                                        # counter reset
                                        fps_counter = 1
                                        # accumlated frame width reset
                                        acc_frame_width = int(data.split("=")[1])
                                    else:
                                        fps_counter += 1
                                        acc_frame_width += int(data.split("=")[1])
                f.close()
        print ("Total seconds: ", total_seconds)
        print ("Average FPS: ", final_fps/total_seconds)
        print ("Average frame width: ", final_frame_width/total_seconds)

                            
if __name__ == "__main__":
    main(sys.argv[1:])
