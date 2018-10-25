import threading
import heuristic
import astar

class AStarThread(threading.Thread):
    def __init__(self, map=None, heuristic=heuristic.Heuristic.euclidian_distance, epsilon=1.0, message_queue=None):
        threading.Thread.__init__(self)
        self.started = False
        self.finished = False
        self.result = None
        self.map = map
        self.heuristic = heuristic
        self.epsilon = epsilon
        self.message_queue = message_queue

    def run(self):
        self.started = True
        if self.map == None:
            self.finished = True
            return
        raw_res = astar.AStar.search_map(self.map, self.heuristic, self.epsilon, self.message_queue)
        self.result = astar.AStar.parse_result(*raw_res, message_queue=self.message_queue)
        self.finished = True