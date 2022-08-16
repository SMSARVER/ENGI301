"""
--------------------------------------------------------------------------
Read Connect 4 Board
--------------------------------------------------------------------------
License:   
Copyright 2022 Samuel Sarver

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------


About:
- Captures picture of connect 4 board
- returns 6x7 numpy array of 0's (green), 1's (blue), and 2's (red)

"""

print("importing...")
import numpy as np
import cv2 as cv
print("finished importing\n") #why does importing take soooo long?

def readBoard():

    debug = False # If True, generates images illustrating process of finding pieces
    
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    img = frame
    if (True):
        cv.imwrite("assets/1cap.jpg", img)
    
    if (debug):
        cimg = img.copy() #image copies for drawing circles in later steps
        cimgB = img.copy()
        cimgR = img.copy()
        cimgG = img.copy()
        cimgR2 = img.copy()
        cimgB2 = img.copy()
        cimgG2 = img.copy()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #makes gray image from color image
    gray = cv.equalizeHist(gray) # increases contrast
    hsvBlue = cv.cvtColor(img, cv.COLOR_BGR2HSV) #converts image to HSV
    hsvRed = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    blur = cv.medianBlur(gray, 5)
    lightBlue = (100, 255*0.4, 255*0.2) #color range for blue and red
    darkBlue = (130, 255*1, 255*1)
    lightRed = (100, 255*0.3, 255*0.2) #color range for blue and red
    darkRed = (130, 255*1, 255*1)
    lightGreen = (20, 255*0.2, 255*0.2) #color range for green
    darkGreen = (95, 255*1, 255*1)
    blueMask = cv.inRange(hsvBlue, lightBlue, darkBlue) #a selection of the pixels in the image that fall within the range of HSV values
    redMask = cv.inRange(hsvRed, lightRed, darkRed)
    greenMask = cv.inRange(hsvBlue, lightGreen, darkGreen)

    if (debug):
        strip = cv.imread('assets/strip.png', 1) #used for testing hsv values
        striphsv = cv.cvtColor(strip, cv.COLOR_BGR2HSV)
        cv.imwrite('assets/gray.jpg', blur)
        cv.imwrite('assets/blueMask.jpg', blueMask)
        cv.imwrite('assets/redMask.jpg', redMask)
        cv.imwrite('assets/greenMask.jpg', greenMask)

    minDist = int(blur.shape[1]/11) #adjust depending on how much of the image frame the board fills (currently assumes mostly filled)
    minRadius = int((blur.shape[1]/10)/2)
    maxRadius = int((blur.shape[1]/8)/2)
    
    allcircles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, minDist, param1=100, param2=25, minRadius=15, maxRadius=maxRadius) # Make list with every circle found on image

    if (debug): # Create image showing location of all circles
        for i in allcircles[0,:]:
            # draw the outer circle
            cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(cimg,(i[0],i[1]),1,(0,0,255),3)
        cv.imwrite('assets/allcircles.jpg', cimg)

    allCirclesAdded2 = [[0,0,0]] #create new "emptey" list with the right format
    

    for i in allcircles[0,:]:
        circlePixelsRed = np.count_nonzero(redMask[int(i[1]-i[2]*0.5):int(i[1]+i[2]*0.5),int(i[0]-i[2]*0.5):int(i[0]+i[2]*0.5)])#np.count_nonzero(redMask[int(i[1] - i[2]/2):int(i[1] + i[2]/2)][int(i[0] - i[2]/2):int(i[0] + i[2]/2)])
        circlePixelsBlue = np.count_nonzero(blueMask[int(i[1]-i[2]*0.5):int(i[1]+i[2]*0.5),int(i[0]-i[2]*0.5):int(i[0]+i[2]*0.5)])#np.count_nonzero(redMask[int(i[1] - i[2]/2):int(i[1] + i[2]/2)][int(i[0] - i[2]/2):int(i[0] + i[2]/2)])
        circlePixelsGreen = np.count_nonzero(greenMask[int(i[1]-i[2]*0.5):int(i[1]+i[2]*0.5),int(i[0]-i[2]*0.5):int(i[0]+i[2]*0.5)])#np.count_nonzero(redMask[int(i[1] - i[2]/2):int(i[1] + i[2]/2)][int(i[0] - i[2]/2):int(i[0] + i[2]/2)])

        if (circlePixelsRed > 0): #(redMask[int(i[1])][int(i[0])] > 0):#
            if (debug):
                cv.circle(cimgR2,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgR2,(i[0],i[1]),1,(0,0,255),3)
            i[2] = 1 #human spaces
            allCirclesAdded2 = np.append(allCirclesAdded2, [i], axis=0)
            
        elif (circlePixelsBlue > 0): #(redMask[int(i[1])][int(i[0])] > 0):#
            if (debug):
                cv.circle(cimgB2,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgB2,(i[0],i[1]),1,(0,0,255),3)
            i[2] = 2 #robot spaces
            allCirclesAdded2 = np.append(allCirclesAdded2, [i], axis=0)
            
        elif (circlePixelsGreen > 0):#(redMask[int(i[1])][int(i[0])] > 0):#
            if (debug):
                cv.circle(cimgG2,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgG2,(i[0],i[1]),1,(0,0,255),3)
            i[2] = 0 #emptey spaces
            allCirclesAdded2 = np.append(allCirclesAdded2, [i], axis=0)
    
    if (debug):
        cv.imwrite('assets/redcircles2.jpg', cimgR2) 
        cv.imwrite('assets/bluecircles2.jpg', cimgB2) 
        cv.imwrite('assets/greencircles2.jpg', cimgG2) 
       
       ''' Separate method for finding circles'''
        '''find all blue circles seperatly'''
        blueblur = cv.bitwise_and(blur, blur, mask=blueMask) #selects the pixels of the blured B&W image that are also blue
        cv.imwrite('assets/blueblur.jpg', blueblur)
        bluecircles = cv.HoughCircles(blueblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=70, param2=30, minRadius=0, maxRadius=maxRadius) #generates list with [x,y,radius] of each circle
        try:
            for i in bluecircles[0,:]:
                cv.circle(cimgB,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgB,(i[0],i[1]),1,(0,0,255),3)
            cv.imwrite('assets/bluecircles.jpg', cimgB) 
        except:
            pass
        
        '''find all red circles sperately'''
        redblur = cv.bitwise_and(blur, blur, mask=redMask) #(blueMask+redMask)
        cv.imwrite('assets/redblur.jpg', redblur)
        redcircles = cv.HoughCircles(redblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=70, param2=70, minRadius=0, maxRadius=maxRadius)
        try:
            for i in redcircles[0,:]:
                cv.circle(cimgR,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgR,(i[0],i[1]),1,(0,0,255),3)
            cv.imwrite('assets/redcircles.jpg', cimgR) #NEED to make new image copy
        except:
            pass
        
        '''find all green circles sperately'''
        greenblur = cv.bitwise_and(blur, blur, mask=greenMask) #(blueMask+redMask)
        cv.imwrite('assets/greenblur.jpg', greenblur)
        greencircles = cv.HoughCircles(greenblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=35, param2=20, minRadius=0, maxRadius=maxRadius)
        for i in greencircles[0,:]:
            # draw the outer circle
            cv.circle(cimgG,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(cimgG,(i[0],i[1]),1,(0,0,255),3)
        cv.imwrite('assets/greencircles.jpg', cimgG) #NEED to make new image copy

    '''generate board from locations of red green and blue circles'''
    #allCirclesAdded = [[0,0,0]] # this makes the need to do a +1
    allCirclesAdded = allCirclesAdded2
    allCirclesAdded = allCirclesAdded[allCirclesAdded[:,1].argsort()] #1 for sorting y column #https://thispointer.com/sorting-2d-numpy-array-by-column-or-row-in-python/
    #allCirclesAdded[1:7] = allCirclesAdded[1:7][allCirclesAdded[1:7][:,0].argsort()] #- this works for sorting the first 7 items
    for i in range(0,6): #sorts each range of 7 circles by their x value
        allCirclesAdded[(1+7*i):(7*(i+1)+1)] = allCirclesAdded[(1+7*i):(7*(i+1)+1)][allCirclesAdded[(1+7*i):(7*(i+1)+1)][:,0].argsort()] #0 for sorting x column
        # 1:8, 8:15, 15:22, 22:29, 29:36, 36:43 sort these ranges based on x
    board = np.full((6, 7), 3) #generates board of 3's to be replaced
    #go down list of circles, set (i,j) element of array equal to the 3rd element of the circle in the list
    for i in range(0,6): #6 rows of y values 
        for j in range(0,7): #7 columns of x values
            board[i,j] = allCirclesAdded[i*7 + j + 1][2] #replaces x,y value of board with the right color value
    if (debug):
        print(board)
    board = np.flip(board, 0) #flips board to be compatable with main.py
    return board
    
#Test Code:
if __name__ == "__main__":
    readBoard()  

'''

    #add the circle lists together # done in previous step now
    #allCirclesAdded = greencircles[0][:].append(redcircles[0][:]).append(bluecircles[0][:]) #WHY do we get the dtype=float32????
    #print("\nall circles list:")
    #print(allCirclesAdded)
    #sort circle lists by y and then by x
    ##allCirclesAdded = sorted(allCirclesAdded, key=lambda k: [k[1], k[0]])
    #print("\nsorting...")
    #allCirclesAdded = np.array(allCirclesAdded).sort()


if (debug):
        pass#print(len(greencircles[0][:])+len(redcircles[0][:])+len(bluecircles[0][:])) #should equal 42 if all circles found (r,g,b)
    #replace the third element of green circles with 0, red circles with 1, blue circles with 2 (previously the radius)
    for i in range(0, len(greencircles[0][:])):
        greencircles[0][i][2] = 0 #emptey spaces #replaces radius with piece color value
        allCirclesAdded = np.append(allCirclesAdded, [greencircles[0][i]], axis=0) #adds circle to list of allCirclesAdded
    try:
        for i in range(0, len(redcircles[0][:])):
            redcircles[0][i][2] = 1 #robot spaces
            allCirclesAdded = np.append(allCirclesAdded, [redcircles[0][i]], axis=0)
    except:
        pass
    try:
        for i in range(0, len(bluecircles[0][:])):
            bluecircles[0][i][2] = 2 #human spaces
            allCirclesAdded = np.append(allCirclesAdded, [bluecircles[0][i]], axis=0)
    except:
        pass
    
    
'''