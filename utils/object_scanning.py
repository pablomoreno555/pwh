def get_objects(controller):

    # Function to scan for objects from the current position of the robot from 4 different orientations
    def scan_objects():
        event = controller.step(action='Pass')
        for obj in event.metadata['objects']:
            if obj['visible'] and obj['objectType'] not in objects_detected:
                objects_detected.append(obj['objectType'])

        event = controller.step(action='RotateRight', degrees=90)
        for obj in event.metadata['objects']:
            if obj['visible'] and obj['objectType'] not in objects_detected:
                objects_detected.append(obj['objectType'])

        event = controller.step(action='RotateRight', degrees=90)
        for obj in event.metadata['objects']:
            if obj['visible'] and obj['objectType'] not in objects_detected:
                objects_detected.append(obj['objectType'])

        event = controller.step(action='RotateRight', degrees=90)
        for obj in event.metadata['objects']:
            if obj['visible'] and obj['objectType'] not in objects_detected:
                objects_detected.append(obj['objectType'])

    # List to store all the detected objects in the environment
    objects_detected = []

    # Do a first scan from the initial position of the robot
    scan_objects()

    # Get the coordinates of the scene bounds: the 4 corners of the scene
    event = controller.step(action='Pass')
    points = event.metadata['sceneBounds']['cornerPoints']
    corners = [points[2], points[3], points[6], points[7]]

    # Express the corner coordinates into a list of dictionaries
    corners_positions = []
    for i in range(len(corners)):
        corners_positions.append({'x': corners[i][0], 'y': corners[i][1], 'z': corners[i][2]})

    # Go to each of the 4 corners and scan for objects there
    for corner in corners_positions:
        # navigation.navigate_to(controller, corner)
        controller.step(action="Teleport", position=corner)
        scan_objects()

    return objects_detected