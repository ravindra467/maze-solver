# Maze Solver
Maze Solver is a Python program that uses Breadth-First-Search algorithm to solve a maze. The program utilizes OpenCV library for image processing and visualization.

## Requirements
- Python 3
- OpenCV (cv2)
- Numpy
- Colorsys
- Tkinter

## Usage
- Run the program using a command line python main.py
- Select an image using the file dialog
- Click on the image to set the start point (it will be marked with a red dot)
- Click on the image again to set the end point (it will be marked with a yellow dot)
- The shortest path will be marked with cyan dots

## Example
![Maze Demo](https://github.com/ravindra467/maze-solver/blob/main/demo.gif)

## Features
- Solve maze using Breadth-First-Search algorithm
- Visualize the solution path using colors
- Select starting and ending points of the maze using mouse clicks

## Limitations
- The script only works on grayscale images
- The pathfinding algorithm may not always find the optimal path due to the nature of BFS
- The script may be slow on large images

## Contributions
Feel free to fork the project and submit pull requests.

## License
This project is licensed under the MIT License.
