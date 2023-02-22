import numpy as np
import cv2

# Reading template and image
Temp = cv2.imread('Template1.jpeg')
Image = cv2.imread('Test2.jpeg')

# Getting Template center
TempH, TempW, TempCh = Temp.shape
center = (TempW/2, TempH/2)
# Getting Image size
ImageH, ImageW, ImageCH = Image.shape

# Min match value
Cmax_val = 0

#Rotate template 360 by intervals of 2 and scale template from 0.5 to 3
for scale in range(5,31):
    print(TempW*scale*0.1,TempH*scale*0.1)
    TempH = int(TempH*scale*0.1)
    TempW = int(TempW*scale*0.1)
    print(TempW,TempH)
    if (TempH > ImageH or TempW > ImageW):
        break 
    for angle in range(1,181):

        #Function to both scale and rotate image
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle*2, scale=scale*0.1)
        rotated_Temp = cv2.warpAffine(src=Temp, M=rotate_matrix, dsize=(TempW, TempH))

        #Template matching function using cv2.TM_CCORR_NORMED
        Output = cv2.matchTemplate(Image,rotated_Temp,4)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(Output)
    
        #Compare to find best match and store its location, width and height
        print(scale,angle,max_val)
        if max_val>Cmax_val:
            Cmax_val = max_val
            location = max_loc
            ResH, ResW, ResCH = rotated_Temp.shape
            CurTemp = rotated_Temp.copy()

print(Cmax_val)
cv2.imshow('Match1', CurTemp)

bottom_right = (location[0] + ResW, location[1] + ResH)
cv2.rectangle(Image, location, bottom_right, 255, 5)

cv2.imshow('Match', Image)
cv2.waitKey(0)
cv2.destroyAllWindows()