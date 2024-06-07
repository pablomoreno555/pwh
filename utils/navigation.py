import numpy as np
import heapq
import math

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


# Main function - Moves the agent to the specified goal position
def navigate_to(controller, object_position):

    # Get all the reachable positions that the robot can be at
    event = controller.step(action='GetReachablePositions')
    reachable_positions = event.metadata['actionReturn']


    # -------------- OBSTACLES PLACEMENT -------------- #


    # FloorPlan1: FRIDGE - Open the fridge to make the garbage can inaccessible to the robot
    # if round(object_position['x'], 2) == -1.93 and round(object_position['y'], 2) == -0.00 and round(object_position['z'], 2) == 2.03:
    #     controller.step(action="OpenObject", objectId="Fridge|-02.10|+00.00|+01.07", openness=1, forceAction=True)

    # FloorPlan3: PLANT - To make the cabinet inaccessible to the robot
    # if round(object_position['x'], 2) == -1.46 and round(object_position['y'], 2) == 0.78 and round(object_position['z'], 2) == -2.00:
    #     controller.step(action='TeleportObject', objectId='HousePlant|-02.03|+01.31|-00.03', x=-0.9, y=0.5, z=-1.3, rotation=dict(x=0, y=90, z=0), forceAction=True)

    # FloorPlan3: GARBAGE CAN - To make the apple inaccessible to the robot
    # if round(object_position['x'], 2) == -2.20 and round(object_position['y'], 2) == 1.35 and round(object_position['z'], 2) == -3.40:
    #     controller.step(action='TeleportObject', objectId='GarbageCan|-01.63|+00.21|+02.19', x=-0.9, y=0.25, z=-2.2, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # FloorPlan3: STOOL - To make the sink inaccessible to the robot
    # if round(object_position['x'], 2) == -1.99 and round(object_position['y'], 2) == 1.14 and round(object_position['z'], 2) == -0.98:
    #     controller.step(action='TeleportObject', objectId='Stool|+00.61|+00.22|-01.08', x=-0.9, y=0.25, z=-1, rotation=dict(x=0, y=90, z=0), forceAction=True)

    # FloorPlan7: CHAIR -  To make the dining table inaccessible to the robot
    # if round(object_position['x'], 2) == -2.66 and round(object_position['y'], 2) == 0.00 and round(object_position['z'], 2) == 3.21:
    #     controller.step(action='TeleportObject', objectId='Chair|-03.51|+00.00|+03.29', x=-2.1, y=0.02, z=2.4, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # FloorPlan16: CHAIRS -  To make the dining table inaccessible to the robot
    # if round(object_position['x'], 2) == 2.42 and round(object_position['y'], 2) == 0.00 and round(object_position['z'], 2) == 3.93:
    #     controller.step(action='TeleportObject', objectId='Chair|+02.76|+00.00|+03.09', x=1.8, y=0, z=3, rotation=dict(x=0, y=0, z=0), forceAction=True)
    #     controller.step(action='TeleportObject', objectId='Chair|+01.62|+00.00|+04.31', x=1.1, y=0, z=3.7, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # FloorPlan16: CHAIR -  To make the knife inaccessible to the robot
    # if round(object_position['x'], 2) == 3.00 and round(object_position['y'], 2) == 1.05 and round(object_position['z'], 2) == -2.04:
    #     controller.step(action='TeleportObject', objectId='Chair|+01.62|+00.00|+04.31', x=1.8, y=0.05, z=-0.9, rotation=dict(x=0, y=95, z=0), forceAction=True)

    # FloorPlan201: CHAIR - To make the book inaccessible to the robot
    # controller.step(action='TeleportObject', objectId='Chair|-01.86|+00.02|+01.04', x=-2.4, y=0.02, z=0.3, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # FloorPlan201: BOX - On the way to the side table, to make the remote control inaccessible to the robot
    # controller.step(action='TeleportObject', objectId='Box|-03.36|+00.19|+06.43', x=-3.75, y=0.75, z=0.75, rotation=dict(x=0, y=45, z=0))
    
    # FloorPlan201: PILLOW - On the way to the TV, to make the TV inaccessible to the robot
    # controller.step(action='TeleportObject', objectId='Pillow|-03.15|+00.68|+03.42', x=-4.3, y=0.75, z=3.5, rotation=dict(x=0, y=45, z=0))

    # FloorPlan204: CHAIR - To make the phone inaccessible to the robot
    # if round(object_position['x'], 2) == -0.20 and round(object_position['y'], 2) == 0.69 and round(object_position['z'], 2) == 5.37:
    #     controller.step(action='TeleportObject', objectId='Chair|-00.49|+00.01|+04.45', x=-1.1, y=0.01, z=4.6, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # FloorPlan214: ARMCHAIR - To make the TV inaccessible to the robot
    # if round(object_position['x'], 2) == -0.75 and round(object_position['y'], 2) == 1.66 and round(object_position['z'], 2) == 3.94:
    #     controller.step(action='TeleportObject', objectId='ArmChair|-04.45|+00.02|+06.45', x=-1.3, y=0.05, z=3.8, rotation=dict(x=0, y=180, z=0), forceAction=True)

    # FloorPlan309: ARMCHAIR - To make the light switch inaccessible to the robot
    # if round(object_position['x'], 2) == -0.16 and round(object_position['y'], 2) == 1.28 and round(object_position['z'], 2) == 4.00:
    #     controller.step(action='TeleportObject', objectId='ArmChair|-00.95|+00.05|+03.58', x=-0.5, y=0.05, z=3.58, rotation=dict(x=0, y=180, z=0), forceAction=True)

    # FloorPlan310: GARBAGE CAN - To make the drawer inaccessible to the robot
    # if round(object_position['x'], 2) == 1.62 and round(object_position['y'], 2) == 0.17 and round(object_position['z'], 2) == -0.99:
    #     controller.step(action='TeleportObject', objectId='GarbageCan|+00.13|-00.03|-02.15', x=1.3, y=0.3, z=-0.9, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # -------------- END OBSTACLES PLACEMENT -------------- #


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
            if pos != other and euclidean_distance(pos, other) <= 0.26:  # Connectivity threshold
                graph[pos].append(other)

    # Find path using the A* algorithm
    path = astar_pathfinding(start_position, goal_position, graph)

    # If the path is empty
    if not path:
        print("No path found. Possible reasons: start and goal are the same or no path exists between them")

    # Get the starting position of the agent
    agent_position = controller.last_event.metadata['agent']['position']

    # Navigate through the path
    for waypoint in path:
        agent_position = position_to_tuple(controller.last_event.metadata['agent']['position'])
        ideal_rotation = direction_to_next(agent_position, waypoint)
        rotate_agent_towards(ideal_rotation, controller)
        event = controller.step(action="Teleport", position=dict(x=waypoint[0], y=waypoint[1], z=waypoint[2]), horizon=0)

        if controller.last_event.metadata["lastActionSuccess"]:
            new_agent_position = controller.last_event.metadata['agent']['position']
            print(f"Moved to: {new_agent_position}")
        else:
            return False

    return True