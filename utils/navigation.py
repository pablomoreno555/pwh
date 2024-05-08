import heapq
import math
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the Euclidean distance between two points using tuples
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2)

# A* pathfinding algorithm
def astar_pathfinding(start_pos, goal_pos, graph):
    open_set = []
    heapq.heappush(open_set, (euclidean_distance(start_pos, goal_pos), 0, start_pos))
    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start_pos] = 0

    while open_set:
        _, current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal_pos:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            return path[::-1]  # Return reversed path

        for neighbor in graph[current_node]:
            tentative_g_score = current_cost + euclidean_distance(current_node, neighbor)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + euclidean_distance(neighbor, goal_pos)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return []

# Convert position dictionaries to tuples to use as graph keys
def position_to_tuple(position):
    return (position['x'], position['y'], position['z'])

# Function to determine the direction to the next waypoint
def direction_to_next(agent_position, next_waypoint):
    agent_x, _, agent_z = agent_position
    waypoint_x, _, waypoint_z = next_waypoint
    dx = waypoint_x - agent_x
    dz = waypoint_z - agent_z
    angle = math.degrees(math.atan2(dx, dz))
    return angle if angle >= 0 else angle + 360

# Function to rotate the agent towards the next waypoint
rotate_step_degrees = 90
def rotate_agent_towards(ideal_rotation, controller):
    current_rotation = controller.last_event.metadata['agent']['rotation']['y']
    rotation_difference = ideal_rotation - current_rotation
    rotation_difference = (rotation_difference + 180) % 360 - 180  # Normalize to [-180, 180]

    if rotation_difference > 0:
        steps = int(rotation_difference / rotate_step_degrees)
        for _ in range(steps):
            controller.step(action="RotateRight")
    else:
        steps = abs(int(rotation_difference / rotate_step_degrees))
        for _ in range(steps):
            controller.step(action="RotateLeft")


# Main function - Moves the agent to the specified goal position in the specified ai2thor environment
def navigate_to(controller, object_position):

    # Get all the reachable positions that the robot can be at
    event = controller.step(action='GetReachablePositions')
    reachable_positions = event.metadata['actionReturn']

    # -------------- OBSTACLES -------------- #

    # BOX / PILLOW - Useful positions to put the box/pillow in FloorPlan201 - 'Box|-03.36|+00.19|+06.43'
    # - On the way to the small table (to pick up the remote control): x=-3.75, y=0.75, z=0.75,
    # - On the way to the TV / TvStand (to turn on the TV / pick up the tissue box): x=-4.0, y=0.75, z=3.5,
    # event = controller.step(action='TeleportObject', objectId='Pillow|-03.15|+00.68|+03.42', x=-4.3, y=0.75, z=3.5, rotation=dict(x=0, y=45, z=0))

    # CHAIRS - FloorPlan16
    # if round(object_position['x'], 2) == 2.42 and round(object_position['y'], 2) == 0.00 and round(object_position['z'], 2) == 3.93:
    #     controller.step(action='TeleportObject', objectId='Chair|+02.76|+00.00|+03.09', x=1.35, y=0, z=3.09, rotation=dict(x=0, y=0, z=0), forceAction=True)
    #     controller.step(action='TeleportObject', objectId='Chair|+01.62|+00.00|+04.31', x=1.1, y=0, z=3.8, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # -------------- END OBSTACLES -------------- #

    # Find the closest reachable position to the object. This will be the goal position
    goal_position = min(reachable_positions, key=lambda pos: np.linalg.norm(np.array([pos['x'], pos['y'], pos['z']]) - np.array([object_position['x'], object_position['y'], object_position['z']])))
    print(f"Closest reachable position: {goal_position}")

    # Generate a navigation graph, that is, reachable positions and their connections
    graph = {position_to_tuple(pos): [] for pos in reachable_positions}

    # Adjust start_position and goal_position to be tuples
    start_position = position_to_tuple(event.metadata['agent']['position'])
    goal_position = position_to_tuple(goal_position)

    # Create connections between nodes in the graph based on the Euclidean distance from each other
    for pos in graph.keys():
        for other in graph.keys():
            if pos != other and euclidean_distance(pos, other) <= 0.31:  # Connectivity threshold
                graph[pos].append(other)

    # Find path using the A* algorithm
    path = astar_pathfinding(start_position, goal_position, graph)

    # If the path is empty
    if not path:
        print("No path found. Possible reasons: start and goal are the same, no path exists, or graph is incorrectly constructed")

    # Get the starting position of the agent
    agent_position = controller.last_event.metadata['agent']['position']

    # Navigate through the path
    for waypoint in path:
        agent_position = position_to_tuple(controller.last_event.metadata['agent']['position'])
        ideal_rotation = direction_to_next(agent_position, waypoint)
        rotate_agent_towards(ideal_rotation, controller)
        event = controller.step(action="MoveAhead")

        if controller.last_event.metadata["lastActionSuccess"]:
            new_agent_position = controller.last_event.metadata['agent']['position']
            print(f"Moved to: {new_agent_position}")

        else:
            # print("Was not able to move")
            # print(controller.last_event)
            return False

        # Pause the simulation, displaying the robot's currenty view
        # event = controller.step(action='Pass')
        # plt.imshow(event.frame)
        # plt.show()

    # print("Navigation to the goal completed")
    return True