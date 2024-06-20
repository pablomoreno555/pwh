# Function to check if the specified object is in the agent's field of view. If so, it returns its position
def is_object_visible(controller, object_id):
    for obj in controller.last_event.metadata['objects']:
        if obj['objectId'] == object_id and obj['visible']:
            return obj['position']
    return None

# Main function - Finds the specified object in the environment
def find_object(controller, object_id):

    # If the object is found, its position will be stored in this variable
    object_position = None

    # Define the 4 horizon angles through which the orientation of the agent's camera will iterate
    # -30: slightly up, 0: neutral, 30: slightly down, 60: far down
    horizon_angles = [0, -30, 30, 60] 
    agent_rotations = 0

    # Try to find the object by checking from all the 4 possible agent's rotations AND all the 4 previous camera angles
    while agent_rotations < 4 and object_position == None:
        for angle in horizon_angles:

            # Adjust the camera angle
            controller.step(action="Teleport", horizon=angle)

            # Check if the object is now visible
            object_position = is_object_visible(controller, object_id)

            # If so, return its position
            if object_position != None:
                return object_position

        # If the object hasn't been found with this agent's rotation, rotate the agent 90 degrees
        if object_position == None:
            controller.step(action='RotateRight', degrees=90)
            agent_rotations += 1

    # If the object is not found after checking all possible combinations of agent's rotations AND camera angles, return None
    return object_position