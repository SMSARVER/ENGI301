# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
Octavo Systems - Read Rubik's Cube
------------------------------------------------------------------------------
Authors:   Erik Welsh (erik.welsh [at] octavosystems.com)
License:   Copyright 2017, Octavo Systems. All rights reserved.
           Distributed under the Octavo Systems license (LICENSE)
------------------------------------------------------------------------------
Read Rubik's cube

Command line:
    read_rubiks_cube.py -i <image_file> 


Description:

Class Cube:
    - Members
      - Faces: "U" (up), "D" (down), "F" (front), "B" (back), "R" (right), "L" (left)
        - Order:  U, L, F, R, B, D
    - Methods
      - print_cube()
      - create_string()
      - verify_cube()
      - rotate_cube() (forward only for now)
      - rotate_face() (back face, CW/CCW only for now)

Class Face:
    - Members
      - Cube dimension (ie 3x3)
      - Array of Tiles
        - Tile is a tuple that is (position, (color tuple))
    - Methods
      - rotate_face() (CW/CCW)


------------------------------------------------------------------------------
Known Issues:

"""
import cv2
import numpy as np
import time

#-----------------------------------------------------------------------------
# Global Variables
#-----------------------------------------------------------------------------
IMAGE_WIDTH             =  1280
IMAGE_HEIGHT            =   720

AREA_MIN                =  5000
AREA_MAX                = 10000
HIGHT_WIDTH_DIFF_MAX    = 20

DUPLICATE_OFFSET        = 10

# Ideal cube locations
# TILES                   = [(700, 375, 100, 100),
#                            (575, 375, 100, 100),
#                            (450, 375, 100, 100),
#                            (700, 250, 100, 100),
#                            (575, 250, 100, 100),
#                            (450, 250, 100, 100),
#                            (700, 125, 100, 100),
#                            (575, 125, 101, 100), 
#                            (450, 125, 100, 100)]

TILES                   = [(725, 325, 125, 125),
                           (575, 325, 125, 125),
                           (425, 325, 125, 125),
                           (725, 175, 125, 125),
                           (575, 175, 125, 125),
                           (425, 175, 125, 125),
                           (725,  25, 125, 125),
                           (575,  25, 125, 125), 
                           (425,  25, 125, 125)]

# Color letters
GREEN                   = "G"
WHITE                   = "W"
YELLOW                  = "Y"
RED                     = "R"
BLUE                    = "B"
ORANGE                  = "O"
                           
# Color values (R, G, B)
#   - Deterimined based on measurements from camera / cube
#
"""
# Speed cube w/ Black Outlines
COLORS                  = {GREEN  : ( 92, 135,  80),
                           WHITE  : (180, 174, 183),
                           YELLOW : ( 82, 180, 187),
                           RED    : ( 12,   9, 102),
                           BLUE   : (133,  75,  30),
                           ORANGE : ( 11,  37, 181)}
"""
"""
# Speed cube w/ Glossy Finish (day)
COLORS                  = {GREEN  : (115, 170, 127),  # (100, 155, 119),
                           WHITE  : (160, 166, 170),  # (155, 157, 172),
                           YELLOW : ( 63, 166, 191),  # ( 85, 165, 223),
                           RED    : (  4,   5, 144),  # (  5,   2, 155),
                           BLUE   : (143,  88,  31),  # (133,  75,  30),
                           ORANGE : (  4,  76, 178)}  # ( 11,  37, 181)}
"""
"""
# Speed cube w/ Matte Finish (TBD)
COLORS                  = {GREEN  : ( 85, 162, 127), #
                           WHITE  : (150, 150, 150), #
                           YELLOW : ( 37, 183, 190), # 
                           RED    : ( 13,   3, 134), # 
                           BLUE   : (155, 131,  82), # 
                           ORANGE : (  2,  55, 167)} # 
"""

COLOR_OFFSET            = 25
COLOR_UNKNOWN           = "X"

RED_THRESHOLD_0         = 100
RED_THRESHOLD_1         = 150
GREEN_THRESHOLD_0       = 30
GREEN_THRESHOLD_1       = 120
BLUE_THRESHOLD_0        = 30
BLUE_THRESHOLD_1        = 120


# Face rotation directions
CLOCKWISE               = "CW"
COUNTER_CLOCKWISE       = "CCW"

# Cube rotation directions
ROTATE_FORWARD          = "F"

# Face Positions
FRONT                   = 2
BACK                    = 4
LEFT                    = 1
RIGHT                   = 3
TOP                     = 0
BOTTOM                  = 5

# Face Positions
FRONT_STR               = "F"
BACK_STR                = "B"
LEFT_STR                = "L"
RIGHT_STR               = "R"
TOP_STR                 = "U"
BOTTOM_STR              = "D"


#-----------------------------------------------------------------------------
# Class Definitions
#-----------------------------------------------------------------------------
class Face(object):
    dimension = None
    tiles     = None
    
    def __init__(self, color=None, tiles=None):
        self.dimension = 3
        if color is not None:
            self.tiles     = [color, color, color,
                              color, color, color,
                              color, color, color]
        else:
            if tiles is not None:
                self.tiles = tiles
            else:
                self.tiles = [COLOR_UNKNOWN, COLOR_UNKNOWN, COLOR_UNKNOWN,
                              COLOR_UNKNOWN, COLOR_UNKNOWN, COLOR_UNKNOWN,
                              COLOR_UNKNOWN, COLOR_UNKNOWN, COLOR_UNKNOWN]
    # End def

    def get_tile(self, position):
        return self.tiles[position]
    # End def
    
    def get_tiles(self):
        return self.tiles
    # End def

    def update_tile(self, position, color):
        self.tiles[position] = color
    # End def

    def complete(self):
        ret_val = True
        
        for tile in self.tiles:
            if (tile == COLOR_UNKNOWN):
                ret_val = False
        
        return ret_val
    # End def

    def rotate_face(self, direction):
        current_face = list(self.tiles)
        
        if (direction == CLOCKWISE):
            self.tiles[0] = current_face[6]
            self.tiles[1] = current_face[3]
            self.tiles[2] = current_face[0]
            self.tiles[3] = current_face[7]
            self.tiles[4] = current_face[4]
            self.tiles[5] = current_face[1]
            self.tiles[6] = current_face[8]
            self.tiles[7] = current_face[5]
            self.tiles[8] = current_face[2]

        elif (direction == COUNTER_CLOCKWISE):
            self.tiles[0] = current_face[2]
            self.tiles[1] = current_face[5]
            self.tiles[2] = current_face[8]
            self.tiles[3] = current_face[1]
            self.tiles[4] = current_face[4]
            self.tiles[5] = current_face[7]
            self.tiles[6] = current_face[0]
            self.tiles[7] = current_face[3]
            self.tiles[8] = current_face[6]

        else:
            print("ERROR:  Unknown direction: {0}".format(direction))
    # End def
    
    def get_row_str(self, row):
        idx    = row * self.dimension
        output = " {0} {1} {2}".format(self.tiles[idx], self.tiles[idx + 1], self.tiles[idx + 2])
        return output
    # End def
    
    def print_face(self):
        for row in range(self.dimension):
            print(self.get_row_str(row))
    # End def
    
# End class


class Cube(object):
    dimension = None
    faces     = None
    
    def __init__(self, faces=None):
        self.dimension = 3
        if faces is None:
            self.faces = [Face(),  # Top    [0]
                          Face(),  # Left   [1]
                          Face(),  # Front  [2]
                          Face(),  # Right  [3]
                          Face(),  # Back   [4]
                          Face()]  # Bottom [5]
        else:
            self.faces = faces
    # End def

    def cube_complete(self):
        ret_val = True
        
        for face in self.faces:
            if not face.complete():
                ret_val = False
        
        return ret_val
    # End def
    
    def get_face(self, position):
        return self.faces[position]
    # End def
    
    def update_face(self, position, face):
        for idx, tile in enumerate(face.get_tiles()):
            current_color = self.faces[position].get_tile(idx)
            if (current_color == COLOR_UNKNOWN):
                self.faces[position].update_tile(idx, tile)
            else:
                if (current_color != tile):
                    print("WARNING: Scan of cube resulted in two diferent color values:  {0} and {1}".format(current_color, tile))
    # End def
    
    def swap_tile(self, src, dest):
        # Contains a tuple: (face number, position number)
        src_tile  = self.faces[ src[0]].get_tile( src[1])
        dest_tile = self.faces[dest[0]].get_tile(dest[1])
        
        self.faces[dest[0]].update_tile(dest[1],  src_tile)
        self.faces[ src[0]].update_tile( src[1], dest_tile)
    # End def
    
    def rotate_cube(self, direction):
        # Only supports forward direction currently
        current_faces = list(self.faces)
        
        if (direction == ROTATE_FORWARD):
            self.faces[TOP]    = current_faces[BACK]          # Back   moved to Top
            self.faces[LEFT].rotate_face(CLOCKWISE)           # Left   rotated  CW
            self.faces[FRONT]  = current_faces[TOP]           # Top    moved to Front
            self.faces[RIGHT].rotate_face(COUNTER_CLOCKWISE)  # Right  rotated  CCW
            self.faces[BACK]   = current_faces[BOTTOM]        # Bottom moved to Back
            self.faces[BOTTOM] = current_faces[FRONT]         # Front  moved to Bottom
            
            # Note:  When you move the bottom to the back, or the back to the top
            #    the face will actually rotate 180 degrees from our viewing angle
            self.faces[TOP].rotate_face(CLOCKWISE)
            self.faces[TOP].rotate_face(CLOCKWISE)
            
            self.faces[BACK].rotate_face(CLOCKWISE)
            self.faces[BACK].rotate_face(CLOCKWISE)
        else:
            print("ERROR: Direction not supported.")
        pass
    # End def
    
    def rotate_cube_face(self, position, direction):
        # Only supports back face (ie self.faces[4])
        if (position == BACK):
            if (direction == CLOCKWISE):
                # Rotate face
                self.faces[BACK].rotate_face(CLOCKWISE)
                
                # Swap tiles on the edges
                #   *** Order of operations matters; only need 3 sets of swaps
                #   Top    [0, 1, 2] -> Left   [6, 3, 0]
                #   Right  [2, 5, 8] -> Top    [0, 1, 2]
                #   Bottom [6, 7, 8] -> Right  [8, 5, 2]
                #   Left   [0, 3, 6] -> Bottom [6, 7, 8]
                self.swap_tile((TOP,    0), (LEFT,   6))
                self.swap_tile((TOP,    1), (LEFT,   3))
                self.swap_tile((TOP,    2), (LEFT,   0))
                
                self.swap_tile((RIGHT,  2), (TOP,    0))
                self.swap_tile((RIGHT,  5), (TOP,    1))
                self.swap_tile((RIGHT,  8), (TOP,    2))
                
                self.swap_tile((BOTTOM, 6), (RIGHT,  8))
                self.swap_tile((BOTTOM, 7), (RIGHT,  5))
                self.swap_tile((BOTTOM, 8), (RIGHT,  2))
                    
            elif (direction == COUNTER_CLOCKWISE):
                # Rotate face
                self.faces[BACK].rotate_face(COUNTER_CLOCKWISE)
                
                # Swap tiles on the edges
                #   *** Order of operations matters; only need 3 sets of swaps
                #   Top    [0][0, 1, 2] -> Right  [3][2, 5, 8]
                #   Left   [1][0, 3, 6] -> Top    [0][2, 1, 0]
                #   Bottom [5][6, 7, 8] -> Left   [1][0, 3, 6]
                #   Right  [3][2, 5, 8] -> Bottom [5][8, 7, 6]
                self.swap_tile((TOP,    0), (RIGHT,  2))
                self.swap_tile((TOP,    1), (RIGHT,  5))
                self.swap_tile((TOP,    2), (RIGHT,  8))
                
                self.swap_tile((LEFT,   0), (TOP,    2))
                self.swap_tile((LEFT,   3), (TOP,    1))
                self.swap_tile((LEFT,   6), (TOP,    0))
                
                self.swap_tile((BOTTOM, 6), (LEFT,   0))
                self.swap_tile((BOTTOM, 7), (LEFT,   3))
                self.swap_tile((BOTTOM, 8), (LEFT,   6))
                
            else:
                print("ERROR:  Unknown direction: {0}".format(direction))
        else:
            print("ERROR: Position not supported: {0}".format(position))
    # End def
    
    def get_color_counts(self):
        counts = {GREEN         : 0,
                  WHITE         : 0,
                  YELLOW        : 0,
                  RED           : 0,
                  BLUE          : 0,
                  ORANGE        : 0,
                  COLOR_UNKNOWN : 0}
        
        for face in self.faces:
            for tile in face.get_tiles():
                counts[tile] += 1

        return counts
    # End def
    
    def infer_side_centers(self):
        # From 4 faces, we can infer the other two faces:
        #   [W, R, Y, O] -> L = B; R = G
        #   [W, O, Y, R] -> L = G; R = B
        #   [W, B, Y, G] -> L = O; R = R
        #   [W, G, Y, B] -> L = R; R = O
        #   [B, R, G, O] -> L = Y; R = W
        #   [B, O, G, R] -> L = W; R = Y
        ret_val       = True
        inference_map = {GREEN  : {WHITE  : (RED   , ORANGE),
                                   YELLOW : (ORANGE, RED   ),
                                   RED    : (YELLOW, WHITE ),
                                   ORANGE : (WHITE , YELLOW)},
                         WHITE  : {GREEN  : (ORANGE, RED   ),
                                   RED    : (GREEN , BLUE  ),
                                   BLUE   : (RED   , ORANGE),
                                   ORANGE : (BLUE  , GREEN )},
                         YELLOW : {GREEN  : (RED   , ORANGE),
                                   RED    : (BLUE  , GREEN ),
                                   BLUE   : (ORANGE, RED   ),
                                   ORANGE : (GREEN , BLUE  )},
                         RED    : {GREEN  : (WHITE , YELLOW),
                                   WHITE  : (BLUE  , GREEN ),
                                   YELLOW : (GREEN , BLUE  ),
                                   BLUE   : (YELLOW, WHITE )},
                         BLUE   : {WHITE  : (ORANGE, RED   ),
                                   YELLOW : (RED   , ORANGE),
                                   RED    : (WHITE , YELLOW),
                                   ORANGE : (YELLOW, WHITE )},
                         ORANGE : {GREEN  : (YELLOW, WHITE ),
                                   WHITE  : (GREEN , BLUE  ),
                                   YELLOW : (BLUE  , GREEN ),
                                   BLUE   : (WHITE , YELLOW)}}
 
        t_center = self.faces[   TOP].get_tile(4)
        f_center = self.faces[ FRONT].get_tile(4)

        try:
            self.faces[  LEFT].update_tile(4, inference_map[t_center][f_center][0])
            self.faces[ RIGHT].update_tile(4, inference_map[t_center][f_center][1])
        except:
            print("ERROR: Could not infer cube sides.")
            self.print_cube()
            ret_val = False

        return ret_val
        # print("LEFT  = {0}".format(inference_map[t_center][f_center][0]))
        # print("RIGHT = {0}".format(inference_map[t_center][f_center][1]))
    # End def
    
    def infer_last_tile(self):
        counts    = self.get_color_counts()
        last_tile = None
        
        for count in counts.keys():
            if (count != COLOR_UNKNOWN):
                if (counts[count] != 9):
                    last_tile = count
        
        if ((counts[COLOR_UNKNOWN] == 1) and (last_tile is not None)):
            for face in self.faces:
                for idx, tile in enumerate(face.get_tiles()):
                    if (tile == COLOR_UNKNOWN):
                         face.update_tile(idx, last_tile)
        else:
            print("WARNING: Could not infer last tile.")
            self.print_cube()
    # End def
    
    def create_string(self):
        output = ""
        
        # Create color -> face mapping dictionary
        #   - Use center of each face to make the mapping 
        c2f_map = {self.faces[   TOP].get_tile(4) : TOP_STR,
                   self.faces[  LEFT].get_tile(4) : LEFT_STR,
                   self.faces[ FRONT].get_tile(4) : FRONT_STR,
                   self.faces[ RIGHT].get_tile(4) : RIGHT_STR,
                   self.faces[  BACK].get_tile(4) : BACK_STR,
                   self.faces[BOTTOM].get_tile(4) : BOTTOM_STR}
        
        # Print string in U->L->F->R->B->D order
        # for face in self.faces:
        #     for tile in face.get_tiles():
        #         output += c2f_map[tile]

        # Print string in U->R->F->D->L->B order for the solver
        for tile in self.faces[TOP].get_tiles():
            output += c2f_map[tile]
        for tile in self.faces[RIGHT].get_tiles():
            output += c2f_map[tile]
        for tile in self.faces[FRONT].get_tiles():
            output += c2f_map[tile]
        for tile in self.faces[BOTTOM].get_tiles():
            output += c2f_map[tile]
        for tile in self.faces[LEFT].get_tiles():
            output += c2f_map[tile]
        for tile in self.faces[BACK].get_tiles():
            output += c2f_map[tile]
        
        return output
    # End def
    
    def print_cube(self):
        space  = "  "
        output = ""
        
        # Print Top
        face    = self.faces[TOP]
        for row in range(self.dimension):
            output += space * self.dimension
            output += face.get_row_str(row) + "\n"
        
        # Print Middle
        for row in range(self.dimension):
            output += self.faces[LEFT].get_row_str(row) + self.faces[FRONT].get_row_str(row) + self.faces[RIGHT].get_row_str(row) + self.faces[BACK].get_row_str(row) + "\n"
        
        # Print Bottom
        face    = self.faces[BOTTOM]
        for row in range(self.dimension):
            output += space * self.dimension
            output += face.get_row_str(row) + "\n"
    
        print(output)
    # End def
    
    def verify_cube(self):
        ret_val = True
        
        if self.cube_complete():
            counts = self.get_color_counts()
            
            if (counts[COLOR_UNKNOWN] != 0):
                ret_val = False
            
            for count in counts.keys():
                if (count != COLOR_UNKNOWN):
                    if (counts[count] != 9):
                        ret_val = False
        else:
            ret_val = False
            
        if not ret_val:
            print("ERROR scanning cube.  Please re-scan.")
        
        return ret_val
    # End def
    
# End class


#-----------------------------------------------------------------------------
# Function Definitions
#-----------------------------------------------------------------------------
def capture_image(camera, width, height, debug=False, verbose=False):    
    # Set image capture size
    #   camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
    #   camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Capture image
    ret, frame = camera.read()

    # Return image or None    
    if (ret):
        return frame
    else:
        return None
# End def


def match_color(color, verbose=False):
    ret_val = COLOR_UNKNOWN

    # Check color based on thresholds
    if ((abs(color[0] - color[1]) < 35) and (abs(color[0] - color[2]) < 35) and 
        (abs(color[1] - color[2]) < 35)):
        ret_val = WHITE
            
    elif ((color[0] <  30) and (color[2] > 100)):
        if (color[1] <  25):
            ret_val = RED
        elif (color[1] < 100):
            ret_val = ORANGE
        elif (color[2] > 140):
            ret_val = YELLOW

    elif ((color[0] < 100) and (color[1] > 100) and (color[2] > 140)):
        ret_val = YELLOW

    elif ((color[0] < 120) and (color[1] > 100) and (color[2] < 140)):
        ret_val = GREEN
    
    elif ((color[0] > 100) and (color[1] < 140) and (color[2] < 100)):
        ret_val = BLUE
    
    
    """
    # Check color based on thresholds
    if ((color[0] > 100) and (color[1] > 100) and (color[2] > 100)):
        ret_val = WHITE
    
    if ((color[0] < 100) and (color[1] > 100) and (color[2] > 100)):
        ret_val = YELLOW
    
    if ((color[0] <  30) and (color[1] <  30) and (color[2] > 100)):
        ret_val = RED
    
    if ((color[0] <  30) and (color[1] < 100) and (color[2] > 100)):
        ret_val = ORANGE
    
    if ((color[0] < 120) and (color[1] > 100) and (color[2] >  80)):
        ret_val = GREEN
    
    if ((color[0] > 100) and (color[1] < 140) and (color[2] < 100)):
        ret_val = BLUE
    """
    """
    # Check color based on thresholds
    #   NOTE:  This method can have issues if there is any marks on the cube
    #       Could add special case for WHITE center
    if (color[0] < BLUE_THRESHOLD_0):
        if (color[1] < GREEN_THRESHOLD_0):
            ret_val = RED
        elif (color[1] > GREEN_THRESHOLD_1):
            ret_val = YELLOW
        else:
            ret_val = ORANGE
    elif(color[0] > BLUE_THRESHOLD_1):
        if (color[2] < RED_THRESHOLD_0):
            ret_val = BLUE
        else:
            ret_val = WHITE
    else:
        if (color[2] < RED_THRESHOLD_1):
            ret_val = GREEN
        else:
            ret_val = YELLOW
    """
    """
    # This method is not that reliable as lighting conditions / cubes change 
    #
    # Check each color for a match
    for c in COLORS.keys():
        if ((color[0] > (COLORS[c][0] - COLOR_OFFSET)) and
            (color[0] < (COLORS[c][0] + COLOR_OFFSET)) and
            (color[1] > (COLORS[c][1] - COLOR_OFFSET)) and 
            (color[1] < (COLORS[c][1] + COLOR_OFFSET)) and
            (color[2] > (COLORS[c][2] - COLOR_OFFSET)) and 
            (color[2] < (COLORS[c][2] + COLOR_OFFSET))):
            return c
    """
        
    # Print color choice
    if (verbose):
        print("Color {0}: {1}, {2}, {3}".format(ret_val, color[0], color[1], color[2]))    
    
    return ret_val
# End def


def show_cube_alignment(image):
    # Update image
    for tile in TILES:
        (x,y,w,h) = (tile[0], tile[1], tile[2], tile[3])
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)                
   
    print('Cube Alignment')
    cv2.imwrite('cube_alignment.png', image)
# End def


def process_cube_image(image, debug=False, verbose=False):
    # Performance monitor
    if (verbose):
        print('Processing Image')
        start_time = time.time()


    # Write original image
    if (debug):
        print('Write original image')
        cv2.imwrite('cube_01_orig.png', image)

        
    # Convert image to Grayscale
    if (False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if (debug):
            print('Convert Grayscale image')
            cv2.imwrite('cube_02_gray.png', gray)
    else:
        gray = image


    # Blur image to reduce background noise
    if (False):
        blur = cv2.GaussianBlur(gray, (7, 7), 1.5, 1.5)
        
        if (debug):
            print('Bluring image')
            cv2.imwrite('cube_03_blur.png', blur)
    else:
        blur = gray


    # Perform edge detection
    if (False):
        edges = cv2.Canny(blur, 0, 30, 3)
        
        if (debug):
            print('Edges image')
            cv2.imwrite('cube_04_edge.png', edges)
    else:
        edges = blur


    # Perform edge dilation
    if (False):
        kernel = np.ones((2,2), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)        
        
        if (debug):
            print('Dilated Edges image')
            cv2.imwrite('cube_05_dilated.png', dilated)
    else:
        dilated = edges
        
    
    # Find contours
    if (False):
        squares = []
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Test each contour
        for contour in contours:
            area = cv2.contourArea(contour)
            if ((area > AREA_MIN) and (area < AREA_MAX)):
                x, y, w, h = cv2.boundingRect(contour)
                
                # Contour must be a square
                if (abs(w - h) < HIGHT_WIDTH_DIFF_MAX):                
                    squares.append((x, y, w, h))

        # Remove duplicates rectangles
        tiles  = []
        offset = DUPLICATE_OFFSET
        
        for square in squares:
            append = True
            
            for tile in tiles:
                if ((square[0] >= (tile[0] - offset)) and 
                    (square[0] <= (tile[0] + offset)) and
                    (square[1] >= (tile[1] - offset)) and
                    (square[1] <= (tile[1] + offset))):
                    append = False
            
            if (append):
                tiles.append(square)

        if (debug):
            # Update image
            for tile in tiles:
                (x,y,w,h) = (tile[0], tile[1], tile[2], tile[3])
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)                
                print("{0} {1} {2} {3}".format(x, y, w, h))
            
            print('Countours image')
            cv2.imwrite('cube_06_tiles.png', image)
    else:
        tiles = []
    
    
    # Stop of no squares are found
    if (len(tiles) != 9):
        if (verbose):
            print("WARNING:  Could not process image correctly. Using ideal locations.")
            
        if (debug):
            print(tiles)

        # Continue with ideal tiles        
        tiles = TILES


    # Sort the squares
    #   - There can be some slop in the squares so we need to get common x and y
    #     so we can properly sort the cubes
    if (True):
        max_width  = max(tiles, key=lambda item: item[2])[2]
        max_height = max(tiles, key=lambda item: item[3])[3]
        nearest    = max_height * 1.2                  # Might have issues

        sorted_tiles = sorted(tiles, key=lambda r: (int(nearest * round(float(r[1])/nearest)) * max_width + r[0]))
    else:
        sorted_tiles = tiles
    
    if (debug):
        print(sorted_tiles)


    # Find color of squares
    #   - Crop squares so there are no problems
    results = []
    
    for idx, result in enumerate(sorted_tiles):
        (x,y,w,h) = (result[0], result[1], result[2], result[3])

        # Use inner 1/4 of cube for color measurement        
        x1_crop = int(x + w/4)
        y1_crop = int(y + h/4)
        x2_crop = int(x1_crop + w/2)
        y2_crop = int(y1_crop + h/2)
        roi     = image[y1_crop:y2_crop, x1_crop:x2_crop]

        # Get color
        color = cv2.mean(roi)
        c     = match_color(color, verbose)

        # Add to Face
        results.append(c)
        
        if (debug):
            cv2.imwrite('cube_07_{0}_roi.png'.format(idx), roi)


    if (verbose):
        total_time = time.time() - start_time
        print("    Processing Time = {0:10.2f} seconds".format(total_time))
    
    return results

# End def


def calibrate_color(camera, debug=False, verbose=False):
    tiles   = TILES
    image   = capture_image(camera, IMAGE_WIDTH, IMAGE_HEIGHT, debug, verbose)

    # Find color of squares
    #   - Crop squares so there are no problems
    r = []
    g = []
    b = []
    
    for idx, tile in enumerate(tiles):
        (x,y,w,h) = (tile[0], tile[1], tile[2], tile[3])

        # Use inner 1/4 of cube for color measurement        
        x1_crop = int(x + w/4)
        y1_crop = int(y + h/4)
        x2_crop = int(x1_crop + w/2)
        y2_crop = int(y1_crop + h/2)
        roi     = image[y1_crop:y2_crop, x1_crop:x2_crop]

        # Get color
        color = cv2.mean(roi)

        # Add to results
        r.append(color[0])
        g.append(color[1])
        b.append(color[2])
        
    # Generate single RGB value
    r_min = min(r)
    r_max = max(r)
    r_val = int(r_min + ((r_max - r_min) / 2))
    
    g_min = min(g)
    g_max = max(g)
    g_val = int(g_min + ((g_max - g_min) / 2))

    b_min = min(b)
    b_max = max(b)
    b_val = int(b_min + ((b_max - b_min) / 2))
    
    print("Color: ({0}, {1}, {2})".format(r_val, g_val, b_val))

    return (r_val, g_val, b_val)
# End def


def init_face(cube, camera, debug=False, verbose=False):
    image   = capture_image(camera, IMAGE_WIDTH, IMAGE_HEIGHT, debug, verbose)

    results = process_cube_image(image, debug, verbose)

    cube.update_face(FRONT, Face(tiles=results)) 
# End def    



def init_cube(debug=False, verbose=False):
    cube   = None
    repeat = True
    camera = cv2.VideoCapture(0)

    if (verbose):
        print("Initialize Cube")

    while repeat:
        cube = Cube()
        
        # Move sequence to cover all faces
        if (verbose):
            cube.print_cube()
        
        # Step 1
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 2
        move_arms()
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 3
        move_arms()
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 4
        move_arms()
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
    
        # Infer centers of the sides at this point
        cube.infer_side_centers()
    
        if (verbose):
            cube.print_cube()
            
        # Step 5
        move_arms()
        cube.rotate_cube_face(BACK, CLOCKWISE)
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 6
        move_arms()
        cube.rotate_cube(ROTATE_FORWARD)
        cube.rotate_cube_face(BACK, COUNTER_CLOCKWISE)
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 7
        move_arms()
        cube.rotate_cube_face(BACK, COUNTER_CLOCKWISE)
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
    
        # Step 8
        move_arms()
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        if (verbose):
            cube.print_cube()
        
        # Step 9
        move_arms()
        cube.rotate_cube_face(BACK, CLOCKWISE)
        cube.rotate_cube(ROTATE_FORWARD)
        init_face(cube, camera, debug, verbose)
        
        # Infer last tile
        cube.infer_last_tile()
        
        if (verbose):
            cube.print_cube()
    
        if cube.verify_cube():
            repeat = False
        else:
            # Pause to reset cube
            move_arms()
            
    # End while
        
    # Create cube output string
    output = cube.create_string()
        
    if (verbose):
        print("Cube String:  {0}".format(output))

    # Release camera
    camera.release()            
    
    return output
# End def


def move_arms():
    # DUMMY FUNCTION - Will be expanded 
    # Wait for key proess
    try:
        input("Press Enter to continue...")
    except:
        pass
    
# End def


def usage(exit_level=None):
    import sys
    
    print("Usage:  read_rubiks_cube.py [hdva]")
    
    if exit_level is not None:
        sys.exit(exit_level)
# End def


#-----------------------------------------------------------------------------
# Main Function
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import getopt

    debug      = False
    verbose    = False
    align      = False
    calibrate  = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hdvac", 
                                   ["help", "debug", "verbose", "align", "calibrate"])
    except getopt.GetoptError:
        usage(exit_level=2)
 
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(exit_level=0)
        elif opt in ("-d", "--debug"):
            debug      = True
        elif opt in ("-v", "--verbose"):
            verbose    = True
        elif opt in ("-a", "--align"):
            align      = True
        elif opt in ("-c", "--calibrate"):
            calibrate  = True


    if (align):
        print("Showing cube alignment")
        camera = cv2.VideoCapture(0)
        image = capture_image(camera, IMAGE_WIDTH, IMAGE_HEIGHT, debug, verbose)
        show_cube_alignment(image)
        camera.release()
    elif (calibrate):
        print("Color calibration")
        camera = cv2.VideoCapture(0)
        color = calibrate_color(camera, debug, verbose)
        camera.release()
    else:
        cube_str = init_cube(debug, verbose)            
        print(cube_str)

            
            
    """
    g_face = Face(color=GREEN)
    w_face = Face(color=WHITE)
    y_face = Face(color=YELLOW)
    r_face = Face(color=RED)
    b_face = Face(color=BLUE)
    o_face = Face(color=ORANGE)
    
    faces  = [w_face, g_face, r_face, b_face, o_face, y_face]

    cube = Cube(faces)
    
    # Move sequence to cover all faces
    print("Cube Move sequence")
    
    # set last tile to unknown
    cube.get_face(LEFT ).update_tile(3, COLOR_UNKNOWN)
    
    # set left / right centers to unknown
    cube.get_face(LEFT ).update_tile(4, COLOR_UNKNOWN)
    cube.get_face(RIGHT).update_tile(4, COLOR_UNKNOWN)
    
    
    # Step 1
    cube.print_cube()

    # Step 2
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Step 3
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Step 4
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Infer centers of the sides at this point
    cube.infer_side_centers()
        
    # Step 5
    cube.rotate_cube_face(BACK, CLOCKWISE)
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Step 6
    cube.rotate_cube(ROTATE_FORWARD)
    cube.rotate_cube_face(BACK, COUNTER_CLOCKWISE)
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Step 7
    cube.rotate_cube_face(BACK, COUNTER_CLOCKWISE)
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()

    # Step 8
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()
    
    # Step 9
    cube.rotate_cube_face(BACK, CLOCKWISE)
    cube.rotate_cube(ROTATE_FORWARD)
    cube.print_cube()
    
    # Infer last tile
    cube.infer_last_tile()
    cube.print_cube()

    print(cube.create_string())



    """     
    """
    # Get camera
    camera = cv2.VideoCapture(0)

    print("Capture Image")
    image = capture_image(camera, IMAGE_WIDTH, IMAGE_HEIGHT, debug, verbose)
    
    if (align):
        print("Showing cube alignment")
        show_cube_alignment(image)
    else:
        print("Process Image")
        results = process_cube_image(image, debug, verbose)
        
        print(results)
        
        print("Results:")
        output = ""
        for result in results:
            if ((result[0] % 3) == 0):
                output += "| "
            
            if type(result[1]) is tuple:
                output += "({:>3},".format(int(result[1][0]))
                output += " {:>3},".format(int(result[1][1]))
                output += " {:>3}) ".format(int(result[1][2]))
            else:
                output += "{0} ".format(result[1])
            
            if ((result[0] % 3) == 2):
                output += "|\n"
        print(output)        

    # Release camera
    camera.release()            
    """

# End main
