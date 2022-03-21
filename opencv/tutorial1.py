import cv2
import random

img = cv2.imread('assets/board1.jpg', -1)
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
'''img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite('assets/new_board1.jpg', img)'''

#cv2.imshow('Image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

'''for i in range(100):
    for j in range(img.shape[1]): #loops through all columns
        img[i][j] = [random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)]
        
        
cv2.imwrite('assets/new_board2.jpg', img)'''

