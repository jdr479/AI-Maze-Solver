import time
import math
import numpy as np
import graphmaker
import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

MAZE_WIDTH = 20
MAZE_HEIGHT = 20


# Defines edge between two points by clicking on two points in the maze
def define_points():
   # Initialize variables
   points = []
   clicks = 2

   # Allows user to click two times and create a node at each
   # Point that they clicked
   while len(points) < clicks:
       points = np.asarray(plt.ginput(clicks, timeout=-1))

   return points


# Converts the points from the 'define_points' function into
# A usable data structure (writes them to a text file)
def record_points():
   # Initialize variables and open file
   point_label = 1
   file = open("maze.txt", "w")
   point_array = []
   total_distance = 0
   distance_x = 0
   distance_y = 0
   maze_index = 1
   index = 0

   while maze_index < MAZE_WIDTH * MAZE_HEIGHT:
       # Get the points from the user
       points = define_points()

       # Write the labels for these points to the text file
       file.write("(" + str(point_label) + ", " + str(point_label + 1) + ", ")

       # Convert the points from floats to integers
       index = 0
       while index < len(points):
           points[index][0] = int(points[index][0])
           points[index][1] = int(points[index][1])

           index += 1

       # Calculate the distance between the two points
       distance_x = points[0][0] - points[1][0]
       distance_y = points[0][1] - points[1][1]
       total_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
       total_distance = int(total_distance)

       # Write the distance and the coordinates of the two points
       file.write(str(total_distance) + ", ")
       file.write("[" + str(points[0][0]).replace('.0', '') + ", " + str(points[0][1]).replace('.0', '') + "], ")
       file.write("[" + str(points[1][0]).replace('.0', '') + ", " + str(points[1][1]).replace('.0', '') + "])\n")

       # Increment the label and the index
       point_label += 1
       maze_index += 1

   # Close the file
   file.close()


# Initialize pyplot
plt.figure()
plt.xlim(0, 500)
plt.ylim(0, 500)

# Load image into pyplot
img = mpimg.imread('maze-vector-image-2.jpg')
imgplot = plt.imshow(img)

# Get the points from the user
record_points()


# A SearchNode class w/ two fields for a node label
# And value for path cost
class SearchNode:
   def __init__(self, label, value):
       self.label = label
       self.value = value


# Create a map based off the points created from the maze image file
def load_map(start_node, end_nodes, map_file):
   # Initialize and load up the graph visualizer
   x = graphviz.GraphViz()
   x.loadGraphFromFile(map_file)
   x.plot()
   x.markStart('1')
   x.markGoal('400')
   x.exploreNode('1', ['2', '1'])


def create_map_list(map_file):
   map = []
   outer_map_iterator = 0
   inner_map_iterator = 0
   map_size = 0

   # Open map file
   map_reader = open(map_file, "r")

   # Store each line in the map file into a list; store list length
   map = map_reader.readlines()
   map_size = len(map)

   # Eliminate all unnecessary characters in the list (i.e. "(", ",", " ")
   while outer_map_iterator < map_size:
       map[outer_map_iterator] = map[outer_map_iterator].split()
       inner_map_iterator = 0
       while inner_map_iterator < len(map[outer_map_iterator]):
           map[outer_map_iterator][inner_map_iterator] \
               = map[outer_map_iterator][inner_map_iterator].replace("(", "")
           map[outer_map_iterator][inner_map_iterator] \
               = map[outer_map_iterator][inner_map_iterator].replace(",", "")
           map[outer_map_iterator][inner_map_iterator] \
               = map[outer_map_iterator][inner_map_iterator].replace("'", "")
           map[outer_map_iterator][inner_map_iterator] \
               = map[outer_map_iterator][inner_map_iterator].replace("[", "")
           map[outer_map_iterator][inner_map_iterator] \
               = map[outer_map_iterator][inner_map_iterator].replace("]", "")
           inner_map_iterator += 1
       outer_map_iterator += 1

   return map


# Conducts a breadth first search algorithm, highlighting
# The edges it visits as it moves across the maze
def breadth_first_search(map_file, parent_node, goal_node):
   # Initialize variables
   local_frontier = []
   child_nodes = []
   found_node = SearchNode('', 0)
   index = 1

   # Print statement showing the current node being explored
   print("Exploring node " + parent_node.label)

   # If the current node is the goal node, return the goal node
   if parent_node.label == goal_node.label:
       print("FOUND THE END!")
       return parent_node

   # Add the current node to the frontier and find its children
   local_frontier.append(parent_node)
   child_nodes = find_children(map_file, parent_node)
   child_nodes += child_nodes

   # If no children were found, print a statement saying this and return
   # An empty goal node
   if len(local_frontier) == 0:
       print("No new children found")
       return goal_node

   # Add the children to the frontier
   for child in child_nodes:
       local_frontier.append(child)

   # If any of the children are the goal node, print this and
   # Set the found node to whatever the current node is in this loop
   for node in local_frontier:
       if node.label == goal_node.label:
           print("FOUND THE END!")
           found_node = node

   # Recursively go through all the nodes in the frontier, calling this
   # Method and repeating the process again
   while index < len(local_frontier) and found_node.label != goal_node.label:
       print("Inserting new children: [" + child_nodes + "]")
       found_node = breadth_first_search(map_file, local_frontier[index], goal_node)
       index += 1

   return found_node


# Finds the children for a given parent node
def find_children(map_file, parent_node):
   # Initialize variables
   map = []
   child_nodes = []
   child_nodes_length = 0
   outer_map_iterator = 0
   inner_map_iterator = 0
   map_size = 0

   map = create_map_list(map_file)
   map_size = len(map)

   # Find all of the parent node's children and insert
   # Them into the list of child nodes
   while outer_map_iterator < map_size:
       if map[outer_map_iterator][0] == parent_node.label:
           child_nodes += [(map[outer_map_iterator][1], map[outer_map_iterator][2])]
       elif map[outer_map_iterator][1] == parent_node.label:
           child_nodes += [(map[outer_map_iterator][0], map[outer_map_iterator][2])]
       outer_map_iterator += 1

   # Sort the list of child nodes
   child_nodes.sort()

   child_nodes_length = len(child_nodes)
   outer_map_iterator = 0

   # Convert the goal nodes into a structure that is more optimal for our purposes
   while outer_map_iterator < child_nodes_length:
       child_nodes[outer_map_iterator] = SearchNode(child_nodes[outer_map_iterator][0], child_nodes[outer_map_iterator][1])
       outer_map_iterator += 1

   return child_nodes


# Load the maze in a graph visualizer
load_map("A", "B", "new_maze.txt")

# Prints the results from the breadth first search function
print(breadth_first_search("new_maze.txt", SearchNode('1', 0), SearchNode('50', 0)))
