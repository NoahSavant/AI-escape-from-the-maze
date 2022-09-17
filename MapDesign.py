import random
import Astar


def replace(map, from_value, to_value):
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == from_value:
                map[x][y] = to_value
    return map


def around(map, pos):
    height = len(map)
    width = len(map[0])
    x_pos = [0, -1, -1, 0]
    y_pos = [-1, -1, 0, 0]
    range_x = range(pos[0] - 1 if pos[0] - 1 > 0 else 1, (pos[0] + 1 if pos[0] + 1 < height - 1 else height - 2) + 1)
    range_y = range(pos[1] - 1 if pos[1] - 1 > 0 else 1, (pos[1] + 1 if pos[1] + 1 < width - 1 else width - 2) + 1)
    for i in range(4):
        x_start = pos[0] + x_pos[i]
        y_start = pos[1] + y_pos[i]
        if x_start in range_x and y_start in range_y:
            total = 0
            for x in range(x_start, x_start + 2):
                for y in range(y_start, y_start + 2):
                    if x in range_x and y in range_y:
                        if map[x][y] == 1:
                            total = total + 1
            if total == 3:
                return True
    return False

def set_lane(map, pos):
    if map[pos[0]][pos[1]] == -2:
        return [map, False]
    elif map[pos[0]][pos[1]] == 0:
        map[pos[0]][pos[1]] = 1
    else:
        map[pos[0]][pos[1]] = 0

    height = len(map)
    width = len(map[0])
    range_x = range(pos[0] - 1 if pos[0] - 1 > 0 else 1, (pos[0] + 1 if pos[0] + 1 < height - 1 else height - 2) + 1)
    range_y = range(pos[1] - 1 if pos[1] - 1 > 0 else 1, (pos[1] + 1 if pos[1] + 1 < width - 1 else width - 2) + 1)
    for x in range_x:
        for y in range_y:
            if (x, y) != pos and map[x][y] != 1:
                map[x][y] = -2 if around(map, (x, y)) else 0
    return [map, True]

def get_lane(map):
    return replace(map, -2, 0)


def to_goal_map(map):
    height = len(map)
    width = len(map[0])
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if (x == 1 or x == height - 2 or y == 1 or y == width - 2) and map[x][y] == 1:
                if x == 1:
                    map[x - 1][y] = 3
                elif x == height - 2:
                    map[x + 1][y] = 3
                if y == 1:
                    map[x][y - 1] = 3
                elif y == width - 2:
                    map[x][y + 1] = 3
    return map


def set_goal(map, pos):
    if map[pos[0]][pos[1]] != 3:
        return False
    return True


def get_goal(map, pos):
    map = replace(map, 3, 0)
    map[pos[0]][pos[1]] = 3
    return map


def set_init(map, pos):
    if map[pos[0]][pos[1]] != 1:
        return False
    return True


def get_init(map, pos):
    map[pos[0]][pos[1]] = 2
    return map


def rand_maze(width, height, percent):
    count = int(width*height*percent/100)
    width += 2
    height += 2
    around_pos = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    rand_map = [[-2 if x == 0 or y == 0 or y == height - 1 or x == width - 1 else 0 for x in range(width)] for y in range(height)]
    x_range = range(1, height - 1)
    y_range = range(1, width - 1)
    get_pos = [(random.choice(x_range), random.choice(y_range))]
    in_map = []
    # set lane
    while count > 0 and len(get_pos) > 0:
        pos = random.choice(get_pos)
        get_pos.remove(pos)
        rand_map, valid = set_lane(rand_map, pos)
        if valid:
            in_map.append(pos)
            for x, y in around_pos:
                cur_pos = (pos[0] + x, pos[1] + y)
                if cur_pos[0] in x_range and cur_pos[1] in y_range and cur_pos not in in_map:
                    get_pos.append(cur_pos)
            count -= 1
    rand_map = get_lane(rand_map)

    # set goal
    rand_map = to_goal_map(rand_map)
    goal_list = []
    for x in range(height):
        for y in range(width):
            if (x == 0 or x == height - 1 or y == 0 or y == width - 1) and rand_map[x][y] == 3:
                goal_list.append((x, y))
    goal_pos = random.choice(goal_list)
    rand_map = get_goal(rand_map, goal_pos)

    # set start
    max = 0
    pos_list = []
    for pos in in_map:
        try:
            value = len(Astar.A_Star_Search(rand_map, pos, goal_pos))
        except TypeError:
            value = 0
        if value > max:
            max = value
            pos_list = [pos]
        elif value == max:
            pos_list.append(pos)
    return get_init(rand_map, random.choice(pos_list))

