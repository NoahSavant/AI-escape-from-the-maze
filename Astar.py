import math

#Algorithm
class Map:
    def __init__(self, vir_map, start, goal):
        self.height = len(vir_map)
        self.width = len(vir_map[0])
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.start = start
        self.goal = goal
        for x in range(self.height):
            for y in range(self.width):
                self.map[x][y] = 0 if vir_map[x][y] == 1 or vir_map[x][y] == 3 else 1

    def Expands(self, node):
        pos = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        expands = []
        height_range = range(self.height)
        width_range = range(self.width)
        for p in pos:
            x = node.pos[0] + p[0]
            y = node.pos[1] + p[1]
            if x in height_range and y in width_range and self.map[x][y] != 1:
                expands.append(Node((x,y), node, 1))
        return expands


class Node:
    def __init__(self, position, parent=None, step=0):
        self.pos = position
        self.parent = parent
        if parent:
            self.g = parent.g + step
        else:
            self.g = 0
        self.h = 0
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.pos == other.pos

    def set_f(self, goal):
        self.h = math.sqrt((self.pos[0] - goal[0])**2 + (self.pos[1] - goal[1])**2)
        self.f = self.g + self.h

def Min(list):
    min_item = list[0]
    for item in list:
        if item.f < min_item.f:
            min_item = item
    return min_item


def replace(list, node):
    for item in list:
        if item == node and item.f > node.f:
            list.remove(item)
            list.append(node)


def solution(node):
    solutions = []
    current_node = node
    while current_node.parent:
        solutions.append(current_node.pos)
        current_node = current_node.parent
    return solutions[::-1]


def A_Star_Search(vir_map, start_pos, end_pos):
    map = Map(vir_map, start_pos, end_pos)
    start = Node(map.start)
    start.set_f(map.goal)
    frontier = [start]
    explored = []
    while len(frontier) > 0:
        current_node = Min(frontier)
        frontier.remove(current_node)
        if current_node.pos == map.goal:
            return solution(current_node)
        explored.append(current_node)
        for child in map.Expands(current_node):
            child.set_f(map.goal)
            if child not in frontier and child not in explored:
                frontier.append(child)
            else:
                replace(frontier, child)
