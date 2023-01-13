import os
import cv2 as cv
import numpy as np
import colorsys
import threading
from tkinter import filedialog
from tkinter import Tk
import tkinter.messagebox

class Point(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        pass

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    pass


def onMouse(event, x, y, flags, params):

    global col, start, end, point_count
    s = 2
    if event == cv.EVENT_LBUTTONUP:
        if point_count == 0:
            col = cv.rectangle(col, (x-s, y-s), (x+s, y+s), color=(0, 0, 255), thickness= -1)
            start = Point(x, y)
            print(f'start: {start.x}, {start.y}')
            point_count += 1
            pass
        elif point_count == 1:
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(255, 255, 0), thickness=-1)
            end = Point(x, y)
            print(f'end: {end.x}, {end.y}')
            point_count += 1
            pass


def bfs(st, en):
    global col, h, w, directions
    col_const = 100
    count = 0

    found = False
    queue = []
    visited = [[0 for j in range(w)]for i in range(h)]
    parent = [[Point() for j in range(w)]for i in range(h)]

    queue.append(st)
    visited[st.y][st.x] = 1

    while len(queue) > 0:
        parent_point = queue.pop(0) 
        count +=1


        if count%100 == 0:
            display_image = col.copy()
            display_image = cv.resize(display_image, (800, 800))
            cv.imshow('image', display_image)
            cv.waitKey(1)

        for direction in directions:

            daughter_cell = parent_point + direction
            x = daughter_cell.x
            y = daughter_cell.y
            if daughter_cell.x>0 and daughter_cell.y>0 and daughter_cell.y<h and daughter_cell.x<w:
                if visited[daughter_cell.y][daughter_cell.x] == 0 and (col[daughter_cell.y][daughter_cell.x][0] != 255 or
                    col[daughter_cell.y][daughter_cell.x][1] != 255 or
                    col[daughter_cell.y][daughter_cell.x][2] != 255):

                    queue.append(daughter_cell)
                    visited[y][x] = visited[parent_point.y][parent_point.x] + 1

                    col[y][x] = list(reversed([255 * i for i in
                        colorsys.hsv_to_rgb(
                            visited[y][x] / col_const, 100, 100)]))
                    parent[y][x] = parent_point

                    if daughter_cell == en:
                        print('end')
                        found = True
                        del queue[:]
    path = []
    c = 0
    if found:
        point = en
        while point!=st:
            path.append(point)
            point = parent[point.y][point.x]
        path.append(point)
        for p in path:
            cv.rectangle(col, (p.x-1, p.y-1), (p.x+1, p.y+1), (0, 255, 255, 100), -1)


            if(c % 15 == 0):
                display_image = col.copy()
                display_image = cv.resize(display_image, (800, 800))
                cv.imshow('image', display_image)
                cv.waitKey(1)
            c+=1
        print('found')
        display_image = col.copy()
        display_image = cv.resize(display_image, (800, 800))
        cv.imshow('image', display_image)
        cv.waitKey(0)

    else:
        print('not found')

def sorter(queue, en):
    index = []
    for cell in queue:
        cell_distance_from_death = (cell.x - en.x)**2 + (cell.y - en.y)**2
        index.append(cell_distance_from_death)
        pass
    index = reversed(index)
    return ([x for _, x in sorted(zip(index, queue))])


root = Tk()
root.withdraw()

response = tkinter.messagebox.askquestion("Upload Image", "Please upload an image of CLOSED MAZE in .jpg or .jpeg or .png format only OR To use default image click on 'No' ")

if response=='yes':

    file_path = filedialog.askopenfilename()
    _, file_extension = os.path.splitext(file_path)

    supported_formats = ['.jpg', '.jpeg', '.png']


    try:
        # Open the image file using the file path
        if file_extension.lower() not in supported_formats:
            raise ValueError(f"Error: unsupported file format {file_extension}, supported formats are .jpg and .jpeg and .png")

        point_count = 0
        start  = Point()
        end = Point()
        directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
        size = 512
        img = cv.imread(file_path, 0)
        img = cv.resize(img, (size, size))
        ret, thresh = cv.threshold(img, 150, 255, cv.THRESH_BINARY_INV)
        thresh = cv.resize(thresh, (size, size))
        col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
        h, w, d = col.shape

        cv.namedWindow('image')
        cv.setMouseCallback('image', onMouse)
        while True:
            cv.imshow('image', col)
            k = cv.waitKey(100)
            if point_count == 2:
                break
        pass

        # now we have the start and end points
        bfs(start, end)
        cv.destroyAllWindows()
    except ValueError as e:
        tkinter.messagebox.showerror("Error", e)
    except FileNotFoundError as e:
        tkinter.messagebox.showerror("Error", "File not Found")

else:
    file_path = '12345.jpg'
    try:
        point_count = 0
        start  = Point()
        end = Point()
        directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
        size = 512
        img = cv.imread(file_path, 0)
        img = cv.resize(img, (size, size))
        ret, thresh = cv.threshold(img, 150, 255, cv.THRESH_BINARY_INV)
        thresh = cv.resize(thresh, (size, size))
        col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
        h, w, d = col.shape

        cv.namedWindow('image')
        cv.setMouseCallback('image', onMouse)
        while True:
            cv.imshow('image', col)
            k = cv.waitKey(100)
            if point_count == 2:
                break
        pass

        # now we have the start and end points
        bfs(start, end)
        cv.destroyAllWindows()

    except FileNotFoundError as e:
        tkinter.messagebox.showerror("Error", "Default image not found.")
