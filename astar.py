from math import sqrt
from copy import deepcopy
import sys
import heapq
from timeit import timeit


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Map:
    def __init__(self):
        self.size = 0
        self.map = []
        self.start = Position()
        self.end = Position()

    def read_from_file(self, file_name):
        with open(file_name, "r") as file:
            try:
                # Read all data
                data = file.read().strip().split()
                self.size = int(data[0])

                # Read start point position
                self.start.x = int(data[1])
                self.start.y = int(data[2])

                # Read end point position
                self.end.x = int(data[3])
                self.end.y = int(data[4])

                # Read map data
                data = data[5:]
                for x in range(0, self.size):
                    for y in range(0, self.size):
                        if y == 0:
                            self.map.append([])
                        block = int(data[x * self.size + y])
                        if block < 0 or block > 1:
                            raise Exception("Value in map must be either 0 or 1")
                        self.map[x].append(block)
            except Exception:
                print("Something went wrong while reading from file")
            finally:
                file.close()

    def print_map(self):
        for x in range(0, self.size):
            print(self.map[x])

    def set_start_position(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            self.start.x = x
            self.start.y = y

    def set_end_position(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            self.end.x = x
            self.end.y = y

    def is_valid(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def is_wall(self, x, y):
        return self.map[x][y] == 1


class SearchNode:
    def __init__(self, position=Position(), parent=None):
        self.position = position
        self.parent = parent


class PriorityEntry:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __lt__(self, other):
        return self.priority < other.priority


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, item, priority):
        heapq.heappush(self.queue, PriorityEntry(priority, item))

    def pop(self):
        return heapq.heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0


class Heuristic:
    @staticmethod
    def euclidian_distance(p1, p2):
        return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


class PathFinding:
    @staticmethod
    def create_map(size, default_value):
        check_map = []
        for x in range(0, size):
            for y in range(0, size):
                if y == 0:
                    check_map.append([])
                check_map[x].append(default_value)
        return check_map

    @staticmethod
    def parse_result(map, open_list, path_found):
        # Return result map with with the path from start to end
        result = -1
        correct_path = []
        if path_found:
            result = deepcopy(map.map)
            result[map.start.x][map.start.y] = "S"
            result[map.end.x][map.end.y] = "G"

            for x in range(0, map.size):
                for y in range(0, map.size):
                    if result[x][y] == 1:
                        result[x][y] = "o"
                    elif result[x][y] == 0:
                        result[x][y] = "-"

            node = open_list[-1]
            correct_path.append(node)
            node = node.parent
            while node.parent != None:
                correct_path.append(node)
                x = node.position.x
                y = node.position.y
                result[x][y] = "x"
                node = node.parent

            correct_path.append(SearchNode(map.start))
            correct_path.reverse()
        return result, correct_path

    @staticmethod
    @timeit
    def search_map(map, heuristic, epsilon=1):
        # Create a map for checking if a block is in queue
        check_map = PathFinding.create_map(map.size, -1)
        check_map[map.start.x][map.start.y] = 0

        # Run algorithm
        path_found = False
        open_list = []
        queue = PriorityQueue()
        node = SearchNode(map.start, None)
        queue.push(node, heuristic(map.start, map.end))
        while not queue.empty():
            node = queue.pop()
            node = node.data
            x = node.position.x
            y = node.position.y
            if not map.is_valid(x, y) or map.is_wall(x, y):
                break
            open_list.append(node)

            # If current node is end, stop
            if x == map.end.x and y == map.end.y:
                path_found = True
                break

            g_value = check_map[x][y] + 1
            dxdyrange = [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
            ]
            for (dx, dy) in dxdyrange:
                tempx = x + dx
                tempy = y + dy
                # Child is a wall or not valid
                if not map.is_valid(tempx, tempy) or map.is_wall(tempx, tempy):
                    continue
                # Child is already in queue and has smaller g(x)
                if check_map[tempx][tempy] != -1 and check_map[tempx][tempy] <= g_value:
                    continue

                # Otherwise, add child to queue
                check_map[tempx][tempy] = g_value
                child_pos = Position(tempx, tempy)
                f_value = g_value + heuristic(child_pos, map.end) * epsilon
                queue.push(SearchNode(child_pos, node), f_value)

        return map, open_list, path_found


class TestPathFinding:
    def __init__(self, inp="", out="", time_input="", time_output=""):
        self.input = inp
        self.output = out
        self.time_input = time_input
        self.time_output = time_output 

    @staticmethod
    def run_path_finding(map, heuristic, epsilon=1):
        result, queue, path_found = PathFinding.search_map(map, heuristic, epsilon=epsilon)
        return PathFinding.parse_result(result, queue, path_found)

    @staticmethod
    def run_path_finding_time_limited(map, heuristic, time_limit):
        depsilon = 0.5
        epsilon = 1

        _, _, _ = PathFinding.search_map(map, heuristic, epsilon=epsilon)
        while int(PathFinding.search_map.time_elapsed) < int(time_limit) and epsilon > 0 and depsilon > 0.001:
            temp_epsilon = epsilon - depsilon
            _, _, _ = PathFinding.search_map(map, heuristic, temp_epsilon)
            if int(PathFinding.search_map.time_elapsed) > int(time_limit):
                depsilon -= 0.001
            else:
                epsilon = temp_epsilon

        return epsilon

    def run_time_free(self, heuristic):
        map = Map()
        map.read_from_file(self.input)

        try:
            with open(self.output, "w") as out:
                result, path = TestPathFinding.run_path_finding(map, heuristic)
                outdata = ""
                if len(path) > 0:
                    outdata += "{}\n".format(len(path))
                    for node in path:
                        outdata += "({},{}) ".format(node.position.x, node.position.y)

                    for x in result:
                        if outdata != "":
                            outdata += "\n"
                        for y in x:
                            outdata += str(y) + " "
                else:
                    outdata = "-1"
                out.write(outdata)
        except IOError:
            print("Something went wrong while writing to {}".format(self.output))
        finally:
            out.close()

    def run_time_limited(self, heuristic):
        map = Map()
        map.read_from_file(self.input)

        time_list = []
        try:
            with open(self.time_input, "r") as inp:
                indata = inp.read().strip().split()
                for limit in indata:
                    f_limit = float(limit)
                    time_list.append(f_limit)
        except IOError:
            print("Something went wrong while reading from {}".format(self.time_input))
        finally:
            inp.close()

        try:
            with open(self.time_output, "w") as out:
                for time in time_list:
                    epsilon = self.run_path_finding_time_limited(map, heuristic, time)
                    out.write("{}\n".format(epsilon))
        except IOError:
            print("Something went wrong while writing to {}".format(self.time_output))
        finally:
            out.close()

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 5:
        raise Exception("""This program needs at least 2 arguments for input path and output path
                            Paths for time limit input and output are optional""")
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    test = TestPathFinding(input_path, output_path)
    test.run_time_free(Heuristic.euclidian_distance)
    if len(sys.argv) == 5:
        test.time_input = sys.argv[3]
        test.time_output = sys.argv[4]
        test.run_time_limited(Heuristic.euclidian_distance)