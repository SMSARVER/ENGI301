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

    debug = False
    
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    #img = cv.imread(frame, 1)
    
    #img = cv.imread('assets/board2g.png', 1)#cv.imread(frame, 1) #imports color version of image
    #img = cv.imread('assets/temp1.jpg', 1)
    img = frame
    cv.imwrite("assets/1cap.jpg", img)
    
    if (debug):
        cimg = img.copy() #image copies for drawing circles in later steps
        cimgB = img.copy()
        cimgR = img.copy()
        cimgG = img.copy()
        cimgR2 = img.copy()
   
    #gray = cv.imread('assets/board2g.png', 0) # frame #imports B&W version of image
    #gray = cv.imread('assets/temp1.jpg', 0)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    hsvBlue = cv.cvtColor(img, cv.COLOR_BGR2HSV) #converts image to HSV
    hsvRed = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    if (debug):
        strip = cv.imread('assets/strip.png', 1) #used for testing hsv values
        striphsv = cv.cvtColor(strip, cv.COLOR_BGR2HSV)
        #print("2nd test")
    
    blur = cv.medianBlur(gray, 5)
    if (debug):
        cv.imwrite('assets/gray.jpg', blur)
    #print("gray.jpg")
    
    
    '''create red and blue masks'''
    lightBlue = (100, 255*0.7, 255*0.25) #color range for blue and red
    darkBlue = (130, 255*1, 255*1)
    lightGreen = (30, 255*0.3, 255*0.2) #color range for green
    darkGreen = (90, 255*1, 255*1)
    blueMask = cv.inRange(hsvBlue, lightBlue, darkBlue) #a selection of the pixels in the image that fall within the range of HSV values
    #blueMask = cv.medianBlur(blueMask, 5)
    blueMask = cv.GaussianBlur(blueMask, (5,5),0) #blurs the mask to work better with HoughCircles
    redMask = cv.inRange(hsvRed, lightBlue, darkBlue)
    redMask = cv.GaussianBlur(redMask, (5,5),0)
    greenMask = cv.inRange(hsvBlue, lightGreen, darkGreen)
    greenMask = cv.GaussianBlur(greenMask, (5,5),0)
    
    if (debug):
        cv.imwrite('assets/blueMask.jpg', blueMask)
        cv.imwrite('assets/redMask.jpg', redMask)
        cv.imwrite('assets/greenMask.jpg', greenMask)
        #print("blue/red/greenMask.jpg")
        #print(redMask)
    '''find all circles on image''' #no longer using this
    minDist = int(blur.shape[1]/10) #adjust depending on how much of the image frame the board fills (currently assumes mostly filled)
    minRadius = int((blur.shape[1]/10)/2)
    maxRadius = int((blur.shape[1]/8)/2)
    if (debug):
        allcircles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 2, minDist, param1=150, param2=25, minRadius=15, maxRadius=maxRadius)
        #print(allcircles)
        if (debug):
            for i in allcircles[0,:]:
                # draw the outer circle
                cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv.circle(cimg,(i[0],i[1]),1,(0,0,255),3)
            cv.imwrite('assets/allcircles.jpg', cimg)
            #print("allcircles.jpg")
    

    '''find the red circles in allcircles''' #no longer using this!
    if (debug):
        #print("\nNEW RED CIRCLES\n")
        redCircleList = [[0,0,0]]
        for i in allcircles[0,:]:
            #print(hsvBlue[ int(i[0]):int(i[0]+1), int(i[1]):int(i[1]+1) ])
            #isRed = cv.inRange(hsvRed[ int(i[0]):int(i[0]+1), int(i[1]):int(i[1]+1) ], lightBlue, darkBlue) # Not working at all
            #print(isRed)
            #print(i)
            #print(i[0])
            #print(redMask[int(i[0])])
            
            #print(redMask[int(i[1])][int(i[0])])
            
            if (redMask[int(i[1])][int(i[0])] > 0):
                #redCircleList = [redCircleList,i]
                #redCircleList = np.append(redCircleList, i, axis=0)
                
                cv.circle(cimgR2,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimgR2,(i[0],i[1]),1,(0,0,255),3)
        #print("new red circle list")
        #print(redCircleList)
        
        
        cv.imwrite('assets/redcircles2.jpg', cimgR2) 
        #print("redcircles2.jpg")
    
    

    '''find all blue circles seperatly'''
    blueblur = cv.bitwise_and(blur, blur, mask=blueMask) #selects the pixels of the blured B&W image that are also blue
    if (debug):
        cv.imwrite('assets/blueblur.jpg', blueblur)
        #print("blueblur.jpg")
    bluecircles = cv.HoughCircles(blueblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=70, param2=30, minRadius=0, maxRadius=maxRadius) #generates list with [x,y,radius] of each circle
    if (debug):
        #print(bluecircles)
        try:
            for i in bluecircles[0,:]: #draws blue circles directly onto image coppy
                # draw the outer circle in green
                cv.circle(cimgB,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle in red
                cv.circle(cimgB,(i[0],i[1]),1,(0,0,255),3)
            cv.imwrite('assets/bluecircles.jpg', cimgB) #NEED to make new image copy
            #print("bluecircles.jpg")
        except:
            pass
    
    '''find all red circles sperately'''
    redblur = cv.bitwise_and(blur, blur, mask=redMask) #(blueMask+redMask)
    if (debug):
        cv.imwrite('assets/redblur.jpg', redblur)
        #print("redblur.jpg")
    redcircles = cv.HoughCircles(redblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=70, param2=70, minRadius=0, maxRadius=maxRadius)
    if (debug):
        #print(redcircles)
        try:
            for i in redcircles[0,:]:
                # draw the outer circle
                cv.circle(cimgR,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv.circle(cimgR,(i[0],i[1]),1,(0,0,255),3)
            cv.imwrite('assets/redcircles.jpg', cimgR) #NEED to make new image copy
            #print("redcircles.jpg")
        except:
            pass
    
    '''find all green circles sperately'''
    greenblur = cv.bitwise_and(blur, blur, mask=greenMask) #(blueMask+redMask)
    if (debug):
        cv.imwrite('assets/greenblur.jpg', greenblur)
        #print("greenblur.jpg")
    greencircles = cv.HoughCircles(greenblur, cv.HOUGH_GRADIENT, 2.5, minDist, param1=35, param2=20, minRadius=0, maxRadius=maxRadius)
    if (debug):
        #print(greencircles)
        for i in greencircles[0,:]:
            # draw the outer circle
            cv.circle(cimgG,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(cimgG,(i[0],i[1]),1,(0,0,255),3)
        cv.imwrite('assets/greencircles.jpg', cimgG) #NEED to make new image copy
        #print("greencircles.jpg")
    
    #print(hsvRed[100,100])
    

    '''generate board from locations of red green and blue circles'''
    allCirclesAdded = [[0,0,0]] # this makes the need to do a +1
    #check to see if 42 circles found
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
    #add the circle lists together # done in previous step now
        #allCirclesAdded = greencircles[0][:].append(redcircles[0][:]).append(bluecircles[0][:]) #WHY do we get the dtype=float32????
    if (debug):
        pass#print("\nall circles list:")
        #print(allCirclesAdded)
    #sort circle lists by y and then by x
        ##allCirclesAdded = sorted(allCirclesAdded, key=lambda k: [k[1], k[0]])
        #print("\nsorting...")
        #allCirclesAdded = np.array(allCirclesAdded).sort()
    allCirclesAdded = allCirclesAdded[allCirclesAdded[:,1].argsort()] #1 for sorting y column #https://thispointer.com/sorting-2d-numpy-array-by-column-or-row-in-python/
    
    #allCirclesAdded[1:7] = allCirclesAdded[1:7][allCirclesAdded[1:7][:,0].argsort()] #- this works for sorting the first 7 items
    for i in range(0,6): #sorts each range of 7 circles by their x value
        allCirclesAdded[(1+7*i):(7*(i+1)+1)] = allCirclesAdded[(1+7*i):(7*(i+1)+1)][allCirclesAdded[(1+7*i):(7*(i+1)+1)][:,0].argsort()] #0 for sorting x column
        # 1:8, 8:15, 15:22, 22:29, 29:36, 36:43 sort these ranges based on x
        
    if (debug):
        pass#print("sorted x and y")
        #print(allCirclesAdded)
    #create 6x7 array of zeroes
    board = np.full((6, 7), 3) #generates board of 3's to be replaced
    #go down list of circles, set (i,j) element of array equal to the 3rd element of the circle in the list
    for i in range(0,6): #6 rows of y values 
        for j in range(0,7): #7 columns of x values
            board[i,j] = allCirclesAdded[i*7 + j + 1][2] #replaces x,y value of board with the right color value
            #i: 0 7
    if (debug):
        pass#print(board)
    
    board = np.flip(board, 0) #flips board to be compatable with main.py
    
    return board
    
    #print("\nDONE!")
    
#Test Code:
#readBoard()