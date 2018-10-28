import astar
import message

class ARA:
    @staticmethod
    def search_map(map, heuristic, time_limit, epsilon=5.0, message_queue=None):
        delta_epsilon = 0.5
        # Run path finding
        search_result = astar.AStar.search_map(map, heuristic, epsilon, message_queue)
        _, correct_path = astar.AStar.parse_result(*search_result, message_queue)
        path_len = len(correct_path)
        # Get running time
        run_time = astar.AStar.search_map.time_elapsed
        if message_queue != None:
            message_queue.put_nowait(message.Message(action="ARA_INFO", param=(epsilon, path_len, run_time)))
        # Check if time_limit is satisfied or not
        limit_satisfied = run_time < time_limit
        path_found = search_result[2]
        best_epsilon = epsilon
        best_runtime = run_time

        while run_time < time_limit and epsilon > 1.0 and delta_epsilon >= 0.001 and path_found:
            # Search with temporary epsilon
            temp_epsilon = epsilon - delta_epsilon
            # If decreasing epsilon make it smaller than 1.0
            # decrease delta epsilon
            # and continue
            if temp_epsilon < 1.0:
                delta_epsilon /= 2.0
                continue

            search_result = astar.AStar.search_map(map, heuristic, temp_epsilon, message_queue)
            _, temp_correct_path = astar.AStar.parse_result(*search_result, message_queue)
            temp_path_len = len(temp_correct_path)
            path_found = search_result[2]
            # Get running time
            temp_time = astar.AStar.search_map.time_elapsed
            if message_queue != None:
                msg = message.Message(action="ARA_INFO")
                msg.param = (temp_epsilon, temp_path_len, temp_time)
                message_queue.put_nowait(msg)

            # If temporary running time is acceptable
            # update run_time and epsilon
            if temp_time < time_limit and temp_epsilon >= 1.0:
                run_time = temp_time
                epsilon = temp_epsilon
                # If path length is shorter
                # this epsilon is better
                if len(temp_correct_path) < len(correct_path):
                    best_epsilon = epsilon
                    correct_path = temp_correct_path
                    best_runtime = run_time
            # Else
            # decrease delta epsilon
            else:
                delta_epsilon /= 2.0
        
        if message_queue != None:
            message_queue.put_nowait(message.Message(action="ARA_UNLOCK"))
        return best_runtime, best_epsilon, (limit_satisfied and path_found)