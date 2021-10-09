import math
import logging
import cv2
import cvzone

import numpy as np
import time
import ShapeModule
import HandTrackerModule
from ShapeModule import GameShape

###############################################
wCam, hCam = 640, 480

default_color = (255, 0, 255)
selected_color = (0, 255, 0)
space_between_shapes = 20
close_fingers_factor = 35

shape_list = []

# Hand landmarks
wrist = 0
thumb_tip, thump_ip, thumb_mcp, thumb_cmc = 4, 3, 2, 1
index_tip, middle_tip, ring_tip, pinky_tip = 8, 12, 16, 20
index_dip, middle_dip, ring_dip, pinky_dip = 7, 11, 15, 19
index_pip, middle_pip, ring_pip, pinky_pip = 6, 10, 14, 18
index_mcp, middle_mcp, ring_mcp, pinky_mcp = 5, 9, 13, 17

tip_list = [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]


###############################################

def show_fps(pTime, img):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
    return pTime


# This function will get the shape dimensions for drawing
def get_shape_dimensions(imgh, imgw):
    max_width = imgw - 4 * space_between_shapes  # max width space available for shapes
    max_height = imgh - 4 * space_between_shapes  # max height space available for shape
    shape_height = int(max_height / 3)  # optimal shape height
    shape_width = int(max_width / 3)  # optimal shape width
    print("square height = " + str(shape_height) + " square width " + str(shape_width))
    return shape_height, shape_width


def get_coordinates(shape_height, shape_width, imgw, imgh, space_between_shapes):
    # The loop will fill a list of initial coordinates
    coordinate_list = []
    for i in range(space_between_shapes, imgw - shape_width, shape_width + space_between_shapes):
        for j in range(space_between_shapes, imgh - shape_height, shape_height + space_between_shapes):
            coordinate_list.append((i, j, i + shape_width, j + shape_height))
    return coordinate_list


# This method will draw the shapes using the given coordinates
# example : [(sx,ex,sy,ey),(sx,....]
# Bounding box [x, y, w, h]
# Start x, start y, end x, end y positions
def draw_shapes(image, coordinates, color):
    for coordinate in coordinates:
        print(coordinate)
        cv2.rectangle(image, (coordinate[0], coordinate[1]), (coordinate[2], coordinate[3]), color, cv2.FILLED)
        cvzone.cornerRect(image,
                          (coordinate[0], coordinate[1], coordinate[2] - coordinate[0], coordinate[3] - coordinate[1]),
                          20, rt=0)


# This method will initialize the shape list given the coordinates
def init_shape_objects(coordinate_list):
    for i, item in enumerate(coordinate_list):
        shape_list.append(GameShape(i, (item[0], item[1]), (item[2], item[3])))


# This method will get the most recent coordinates of the shapes
def get_updated_coordinates():
    clist = []
    for item in shape_list:
        clist.append((item.start_p[0], item.start_p[1], item.end_p[0], item.end_p[1]))
    return clist


# A method to check of 2 given points are close to each other
def close_points(p1, p2):
    dist = math.dist((p1[1], p1[2]), (p2[1], p2[2]))
    if dist < close_fingers_factor:
        return True
    else:
        return False


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = HandTrackerModule.HandDetector()

    cx, cy, w, h = 100, 100, 200, 200  # center point of the rectangle, width and height

    # Read initially to get various dimensions
    success, img = cap.read()
    imgh, imgw = img.shape[0], img.shape[1]  # Image height and width

    shape_height, shape_width = get_shape_dimensions(imgh, imgw)  # Get the optimal shape dimensions
    coordinate_list = get_coordinates(shape_height, shape_width, imgw, imgh,
                                      space_between_shapes)  # Initial coordinates locations
    init_shape_objects(coordinate_list)  # Initialized list of shape objects
    dragging = False
    while True:
        # Read image
        success, img = cap.read()

        # Flip image horizontally
        img = cv2.flip(img, 1)

        # Copy image into overlay
        overlay = img.copy()

        # Get the coordinate list where to draw the shapes
        clist = get_updated_coordinates()

        # Draw the shapes
        draw_shapes(overlay, clist, (255, 0, 255))

        # Find the hands in the image
        img = detector.findHands(img, True)

        # Get the list of the various landmarks (landmark = points on the hands)
        lmList = detector.findPosition(img)

        if lmList:  # If there is a list of landmarks available
            cursor = lmList[index_tip]  # Use the index tip as a cursor
            cursor_x, cursor_y = cursor[1], cursor[2]  # x and y of index tip
            if close_points(cursor, lmList[thumb_tip]):
                for item in shape_list:
                    # Check if the index tip is inside one of the shapes
                    # Shapes id's are arranged like:
                    # 0  3  6
                    # 1  4  7
                    # 2  5  8

                    if item.is_point_in_area((cursor_x, cursor_y)):
                        # Update the position of the shape according to the cursor
                        item.update_position(cursor)

        # Transparency stuff
        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle over the image
        image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        cv2.imshow("Image", image_new)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
