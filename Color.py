import cv2
import numpy as np
import easygui
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import argparse  # for finding contours centers
import imutils


def nothing(x):
    pass


def redraw_frame(frame_1, blur_1, path_1, l_h, l_s, l_v, u_h, u_s, u_v):
    # prepare mask with lower and upper bounds
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(blur_1, l_b, u_b)
    res_contours = frame_1.copy()

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    frame_area = frame_1.shape[0]*frame_1.shape[1]
    # find contour and display text with area in %
    #global contours
    global contour_check
    for contour in contours:
        contour_check = contour

        contour_area = cv2.contourArea(contour)
        if contour_area > frame_area*0.01:
            cv2.drawContours(res_contours, contour, -1, (0, 255, 0), 2)
            # draw the contour and center of the shape on the image
            M = cv2.moments(contour)
            if M["m00"] != 0 and M["m01"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(res_contours, (cX, cY), 7, (0, 255, 0), -1)
                cv2.putText(res_contours, str(int(contour_area*100/frame_area)), (cX - 20, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # check mouse-click to be inside a contour
        #for k in range(len(files_path)):

    cv2.imshow(str(path_1), res_contours)
    return


def get_hsv_values():
    global l_h, l_s, l_v, u_h, u_s, u_v
    l_h = cv2.getTrackbarPos("L_Hue", "Tracking")
    u_h = cv2.getTrackbarPos("U_Hue", "Tracking")
    l_s = cv2.getTrackbarPos("L_Saturation", "Tracking")
    u_s = cv2.getTrackbarPos("U_Saturation", "Tracking")
    l_v = cv2.getTrackbarPos("L_Value", "Tracking")
    u_v = cv2.getTrackbarPos("U_Value", "Tracking")
    return l_h, l_s, l_v, u_h, u_s, u_v


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # opencv mix shape of an image
        x,y = y, x
        hsv_click = cv2.medianBlur(hsv[i], 5)
        # set track positions to HSV of clicked point on blurred hsv frame

        print(hsv_click[x, y][0]+30)
        print(hsv_click[x, y][0])

        if hsv_click[x, y][0] - 30 > 0:
            cv2.setTrackbarPos("L_Hue", "Tracking", hsv_click[x, y][0]-30)
        else:
            cv2.setTrackbarPos("L_Hue", "Tracking", 0)
        if hsv_click[x, y][0] + 30 < 180:
            cv2.setTrackbarPos("U_Hue", "Tracking", hsv_click[x, y][0]+30)
        else:
            cv2.setTrackbarPos("U_Hue", "Tracking", 180)

        if hsv_click[x, y][1] - 50 > 0:
            cv2.setTrackbarPos("L_Saturation", "Tracking", hsv_click[x, y][1]-50)
        else:
            cv2.setTrackbarPos("L_Saturation", "Tracking", 0)
        if hsv_click[x, y][1] + 50 < 255:
            cv2.setTrackbarPos("U_Saturation", "Tracking", hsv_click[x, y][1]+50)
        else:
            cv2.setTrackbarPos("U_Saturation", "Tracking", 255)

        if hsv_click[x, y][2] - 30 > 0:
            cv2.setTrackbarPos("L_Value", "Tracking", hsv_click[x, y][2] - 30)
        else:
            cv2.setTrackbarPos("L_Value", "Tracking", 0)
        if hsv_click[x, y][2] + 30 < 255:
            cv2.setTrackbarPos("U_Value", "Tracking", hsv_click[x, y][2]+30)
        else:
            cv2.setTrackbarPos("U_Value", "Tracking", 255)
    return


# create trackbars
cv2.namedWindow("Tracking", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("L_Hue", "Tracking", 0, 180, nothing)
cv2.createTrackbar("U_Hue", "Tracking", 180, 180, nothing)
cv2.createTrackbar("L_Saturation", "Tracking", 0, 255, nothing)
cv2.createTrackbar("U_Saturation", "Tracking", 255, 255, nothing)
cv2.createTrackbar("L_Value", "Tracking", 0, 255, nothing)
cv2.createTrackbar("U_Value", "Tracking", 255, 255, nothing)
cv2.createTrackbar("blur_value", "Tracking", 5, 50, nothing)

# upload and convert images
files_path = easygui.fileopenbox("Choose images", filetypes='*.jpg', multiple=True)
# create None frames
frame = [None]*len(files_path)
hsv = [None]*len(files_path)
blur_img = [None]*len(files_path)
frame_RGB = [None]*len(files_path)

for i, path in enumerate(files_path):
    frame[i] = cv2.imread(path)
    hsv[i] = cv2.cvtColor(frame[i], cv2.COLOR_BGR2HSV)
    blur_img[i] = cv2.medianBlur(hsv[i], 5)
    frame_RGB[i] = cv2.cvtColor(frame[i], cv2.COLOR_BGR2RGB)

# prepare initial frames
get_hsv_values()
blur_pos = cv2.getTrackbarPos("blur_value", "Tracking")
for i in range(len(files_path)):
    redraw_frame(frame[i], blur_img[i], str(files_path[i]), l_h, l_s, l_v, u_h, u_s, u_v)

# graphs to do

# active window
while True:
    # mouse click HSV value and contour
    for i in range(len(files_path)):
        cv2.setMouseCallback(str(files_path[i]), click_event)
    # check blur tracker
    if blur_pos != cv2.getTrackbarPos("blur_value", "Tracking"):
        blur_pos = cv2.getTrackbarPos("blur_value", "Tracking")
        # blur shall be odd
        blur_val = blur_pos * 2 + 3
        # redraw if blur changed
        for i in range(len(files_path)):
            blur_img[i] = cv2.medianBlur(hsv[i], blur_val)
            redraw_frame(frame[i], blur_img[i], str(files_path[i]), l_h, l_s, l_v, u_h, u_s, u_v)
    # check HSV trackers
    if l_h != cv2.getTrackbarPos("L_Hue", "Tracking") or u_h != cv2.getTrackbarPos("U_Hue", "Tracking") or l_s != cv2.getTrackbarPos("L_Saturation", "Tracking") or u_s != cv2.getTrackbarPos("U_Saturation", "Tracking") or l_v != cv2.getTrackbarPos("L_Value", "Tracking") or u_v != cv2.getTrackbarPos( "U_Value", "Tracking"):
        get_hsv_values()
        # redraw if HSV changed
        for i in range(len(files_path)):
            redraw_frame(frame[i], blur_img[i], str(files_path[i]), l_h, l_s, l_v, u_h, u_s, u_v)
    # exit on Esc key
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
