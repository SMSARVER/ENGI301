# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
UnixEdge Software Platform - Read Gauge
------------------------------------------------------------------------------
Authors:   Frank Inselbuch (inselbuch [at] unixedge.com)
           Erik Welsh (welsh [at] unixedge.com)
License:   Copyright 2016, UnixEdge. All rights reserved.
           Distributed under the UnixEdge license (LICENSE)
------------------------------------------------------------------------------
Read a gauge from image


Command line:
    read_gauge.py -i <image_file> 


Description:
    This script will load an image from the image_file and process the image
to determine the angle of the dial of the gauge.  If successful, the script
will output the angle.  

------------------------------------------------------------------------------
Known Issues:
  1) Can measure between [0, pi]; cannot tell difference between [0, pi] and
     [pi, 2pi].  Need to use atan2(y,x) but have to get a point first
  2) process_image() should be split into multiple sub functions

"""
import cv2
import numpy as np
import time


#-----------------------------------------------------------------------------
# Function Definitions
#-----------------------------------------------------------------------------
def process_image(image_file, image_name, debug=False, verbose=False):
    ret_val = None
    
    if (verbose):
        print('Processing Image file:  {0}'.format(image_file))        
        start_time = time.time()
    
    img = cv2.imread(image_file)
    
    # Convert image to Grayscale
    if (True):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if (debug):
            print('Convert Grayscale image')
            cv2.imwrite('{0}_01_gray.png'.format(image_name), gray)
    else:
        gray = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    
 
    # Blur image to reduce background noise
    if (True):
        blur = cv2.medianBlur(gray, 5)
        
        if (debug):
            print('Bluring image')
            cv2.imwrite('{0}_02_blur.png'.format(image_name), blur)
    else:
        blur = gray

    
    # Detect Hough Circle to isolate the gague face
    if (True):
        candidate_circles = []
        minDist           = blur.shape[0] / 4
        minRadius         = blur.shape[0] / 3
        maxRadius         = blur.shape[0]
    
        # cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]])         
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 2, minDist,
                                   param1=200, param2=100, 
                                   minRadius=int(minRadius), maxRadius=int(maxRadius))

        if circles is not None:
            circles = np.uint16(np.around(circles))
        
            for i in circles[0,:]:
                # Check circle is completely within picture
                #     NOTE:  Upper left corner is (0,0)
                radius = int(i[2])
                north  = int(i[1]) - radius
                east   = int(i[0]) + radius
                south  = int(i[1]) + radius
                west   = int(i[0]) - radius
                y_max  = blur.shape[0]
                x_max  = blur.shape[1]

                if ((north > 0) and (east < x_max) and (south < y_max) and (west > 0)):
                    # Append to candidate circle list
                    candidate_circles.append((i[0], i[1], i[2]))
                    
                    # draw the outer circle
                    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    
                    # draw the center of the circle
                    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
            
            if (len(candidate_circles) == 1):
                # Crop Image
                #     NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
                circle = (candidate_circles[0][0], candidate_circles[0][1], candidate_circles[0][2])
                
                radius = int(circle[2])
                north  = int(circle[1]) - radius
                west   = int(circle[0]) - radius
                size   = ((2 * radius), (2 * radius))

                crop   = blur[north:(north + (2 * radius)), west:(west + (2 * radius))]
                img    = img[north:(north + (2 * radius)), west:(west + (2 * radius))]
                
                if (debug):
                    cv2.imwrite('{0}_03_02_crop.png'.format(image_name), crop)
                              
                mask   = np.zeros(size, dtype=np.int8)
                mask   = cv2.circle(mask, (radius, radius), radius, 1, thickness=-1)
                face   = cv2.bitwise_and(crop, crop, mask=mask)

                # Update circle to new cropped image
                circle = (radius, radius, radius)
                
                if (debug):
                    cv2.imwrite('{0}_03_03_mask.png'.format(image_name), face)
            else:
                print("    WARNING: Found {0} candiate circles.".format(len(candidate_circles)))
            
            if (debug):
                print('Hough Circles image')
                cv2.imwrite('{0}_03_01_houghcircles.png'.format(image_name), img)            
        else:
            print("    WARNING: No circles detected")
            exit(0)
    else:
        face   = blur
        circle = None


    # Threshold the image to B&W
    if (True):
        # ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        thresh = cv2.adaptiveThreshold(face, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
        
        if (debug):
            print('Threshold image')
            cv2.imwrite('{0}_04_th.png'.format(image_name), thresh)
    else:
        thresh = face
    

    # Perform edge detection
    if (True):
        # img = cv2.Canny(img, 100, 200)
        edges = cv2.Canny(thresh, 150, 300, apertureSize=5)
        
        if (debug):
            print('Edges image')
            cv2.imwrite('{0}_05_edge.png'.format(image_name), edges)
    else:
        edges = thresh
    
    
    # Get the Hough Lines to identify the pointer
    if (True):
        if (circle is not None):
            minLineLength = circle[2] / 3
        else:
            minLineLength = edges.shape[0] / 3
            
        maxLineGap    = 7
        threshold     = 100
        
        # print("{0}  {1}  {2}".format(threshold, minLineLength, maxLineGap))
        
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=threshold, 
                                minLineLength=minLineLength, maxLineGap=maxLineGap)
        
        candidate_lines = []

        if lines is not None:
            thresh_lines    = img.copy()
            
            # if (circle is not None):
                # print(circle)
            
            for line in lines:
                # print(line)
                
                for x1, y1, x2, y2 in line:

                    if circle is not None:
                        import math
                        threshold = 20

                        # Formulas:
                        #   - For two points, slope is s = (y1 - y2) / (x1 - x2)
                        #   - Using point-slope for a line is:  (-m)x + y + ((m * x1) - y1) = 0
                        #     - a = (-m)
                        #     - b = 1
                        #     - c = (m * x1) - y1
                        #   - For line ax + by + c = 0, distance to point (m, n) is
                        #         abs((a * m) + (b * n) + c)/sqrt(a**2 + b**2)
                        rise      = float(y2 - y1)
                        run       = float(x2 - x1)
                        
                        if (run != 0):
                            slope     = float(rise / run)
                            c         = (slope * x1) - y1    
                            dist      = abs((-slope * circle[0]) + (circle[1]) + c) / math.sqrt(slope**2 + 1)
                        else:
                            slope     = None
                            c         = None
                            dist      = abs(x1 - circle[0])
                        
                        # print("{0}  {1}  {2}  {3}  {4}".format(rise, run, slope, c, dist))
                        
                        if (dist < threshold):
                            cv2.line(thresh_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            candidate_lines.append((x1, y1, x2, y2, slope, c, dist))
                        
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
 
            if (debug):
                cv2.imwrite('{0}_06_th_houghlines.png'.format(image_name), thresh_lines)
        else:
            print("    WARNING:  No lines found")
    
        if (debug):
            print('Hough Lines image')
            cv2.imwrite('{0}_06_all_houghlines.png'.format(image_name), img)
        

    # Detect if picture has any red / orange objects to highlight
    if (len(candidate_lines) == 0):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        red_lower = cv2.inRange(hsv, (  0, 100, 100), ( 10, 255, 255))
        red_upper = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
        
        red = cv2.addWeighted(red_lower, 1.0, red_upper, 1.0, 0.0)
        
        if (debug):
            print('Detect Red objects')
            cv2.imwrite('{0}_07_00_red.png'.format(image_name), red)
        
        if (circle is not None):
            minLineLength = circle[2] / 3
        else:
            minLineLength = edges.shape[0] / 3
            
        maxLineGap    = 7
        threshold     = 100
        
        lines = cv2.HoughLinesP(red, rho=1, theta=np.pi/180, threshold=threshold, 
                                minLineLength=minLineLength, maxLineGap=maxLineGap)
        
        if lines is not None:
            candidate_lines  = []
            thresh_lines = img.copy()
            
            for line in lines:
                for x1, y1, x2, y2 in line:
                    if circle is not None:
                        import math
                        threshold = 20

                        # Formulas:
                        #   - For two points, slope is s = (y1 - y2) / (x1 - x2)
                        #   - Using point-slope for a line is:  (-m)x + y + ((m * x1) - y1) = 0
                        #     - a = (-m)
                        #     - b = 1
                        #     - c = (m * x1) - y1
                        #   - For line ax + by + c = 0, distance to point (m, n) is
                        #         abs((a * m) + (b * n) + c)/sqrt(a**2 + b**2)
                        rise      = float(y2 - y1)
                        run       = float(x2 - x1)
                        
                        if (run != 0):
                            slope     = float(rise / run)
                            c         = (slope * x1) - y1    
                            dist      = abs((-slope * circle[0]) + (circle[1]) + c) / math.sqrt(slope**2 + 1)
                        else:
                            slope     = None
                            c         = None
                            dist      = abs(x1 - circle[0])
                        
                        if (dist < threshold):
                            cv2.line(thresh_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            candidate_lines.append((x1, y1, x2, y2, slope, c, dist))
                        
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if (debug):
                cv2.imwrite('{0}_07_01_th_houghlines.png'.format(image_name), thresh_lines)
        else:
            print("    WARNING:  No lines found")
    
        if (debug):
            print('Hough Lines image')
            cv2.imwrite('{0}_07_02_all_houghlines.png'.format(image_name), img)
    else:
        red = None
    
    
    # Calculate the pointer angle
    if (len(candidate_lines) > 0):
        avg_slope = 0.0
        avg_c     = 0.0
        
        for line in candidate_lines:
            if line[4] is not None:
                avg_slope += line[4]
            if line[5] is not None:
                avg_c     += line[5]

        avg_slope = avg_slope / len(candidate_lines)
        avg_c = (avg_c / len(candidate_lines))
        
        import math
        
        angle = math.atan(avg_slope)
        angle_degrees = math.degrees(angle) + 90

        if (verbose):
            print("    Gauge Angle     = {0:10.2f} degrees".format(angle_degrees))
        
        ret_val = angle_degrees
    else:
        print("    ERROR:  Cannot read gauge.")

    if (verbose):
        total_time = time.time() - start_time
        print("    Processing Time = {0:10.2f} seconds".format(total_time))

    return ret_val
# End def
        

def usage(exit_level=None):
    import sys
    
    print("Usage:  read_gauge.py -i <image_file>")
    
    if exit_level is not None:
        sys.exit(exit_level)
# End def


#-----------------------------------------------------------------------------
# Main Function
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import os
    import getopt

    print("test")
    image_file = None
    debug      = False
    verbose    = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hdvi:", 
                                   ["help", "debug", "verbose", "ifile="])
    except getopt.GetoptError:
        usage(exit_level=2)
 
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(exit_level=0)
        elif opt in ("-d", "--debug"):
            debug      = True
        elif opt in ("-v", "--verbose"):
            verbose    = True
        elif opt in ("-i", "--ifile"):
            image_file = arg

    if image_file is not None:
    
        (path, filename) = os.path.split(image_file)
        (name, ext)      = os.path.splitext(filename)
        
        angle = process_image(image_file, name, debug, verbose)
        
        print(angle)    
    else:
        usage(exit_level=0)

# End main
