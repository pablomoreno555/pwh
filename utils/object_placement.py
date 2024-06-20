# Function to modify the position of some objects within the scene as desired at the beginning of the simulation
def place_objects(controller):

    # ### FloorPlan1:

    # # Put the toaster, kettle, and vase inside the cabinet
    # controller.step(action='TeleportObject', objectId='Toaster|-01.84|+00.90|+00.13', x=0.56, y=0.2, z=-2.29, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Kettle|+01.04|+00.90|-02.60', x=0.336, y=0.2, z=-2.29, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Vase|+01.56|+00.56|-02.50', x=0.336, y=0.2, z=-2.485, rotation=dict(x=0, y=0, z=0), forceAction=True)
    

    # ### FloorPlan3:

    # # Put the apple far back on the countertop and the tomato on the countertop
    # controller.step(action='TeleportObject', objectId='Apple|-01.75|+01.37|-01.16', x=-2.2, y=1.32, z=-3.4, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Tomato|+00.92|+01.91|+01.61', x=-1.467, y=1.35, z=0.244, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the lettuce high on a shelf and the tomato on the countertop
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.89|+01.40|-01.07', x=-1.9, y=2.5, z=-1.905, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Tomato|+00.92|+01.91|+01.61', x=-1.467, y=1.35, z=0.244, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the pot inside the microwave
    # controller.step(action='TeleportObject', objectId='Pot|-01.58|+01.31|-01.58', x=0.947, y=1.5, z=-2.0, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the lettuce on the plate
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.89|+01.40|-01.07', x=-1.47, y=1.36, z=0.24, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the lettuce in the pot
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.89|+01.40|-01.07', x=-1.58, y=1.38, z=-1.58, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan4:

    # # Put the lettuce high on a shelf, out of the robot's reach
    # controller.step(action='TeleportObject', objectId='Lettuce|-03.31|+00.97|+03.04', x=-2.5, y=2.2, z=0.17, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Remove the lettuce from the fridge (put it in the trash can)
    # controller.step(action='TeleportObject', objectId='Lettuce|-03.31|+00.97|+03.04', x=-3.6960792541503906, y=0.5, z=2.0087831020355225, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the egg, potato, and microwave on the dining table and the plate on the counter
    # controller.step(action='TeleportObject', objectId='Egg|-03.37|+01.30|+02.85', x=-0.9, y=1.1, z=2.1, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Potato|-02.66|+01.15|+00.25', x=-0.6, y=1.1, z=2.5, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Microwave|-00.37|+01.11|+00.43', x=-0.8, y=1.5, z=2.9, rotation=dict(x=0, y=180, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Plate|-01.19|+00.92|+00.40', x=-2.2, y=1.2, z=0.46, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan7:

    # # Put some objects in the microwave
    # controller.step(action='TeleportObject', objectId='Bowl|-02.04|+00.90|+00.49', x=1.38, y=1.7, z=-1.6, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Pot|-01.60|+00.90|-00.17', x=1.368, y=1.9, z=-1.55, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Cup|-01.91|+00.90|-00.02', x=1.0769, y=1.8, z=-1.5397, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the wine bottle on the countertop
    # controller.step(action='TeleportObject', objectId='WineBottle|-00.16|+00.78|+02.00', x=-1.75, y=1, z=-0.4, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the mug in the microwave
    # controller.step(action='TeleportObject', objectId='Mug|+01.67|+00.90|-01.32', x=1.15, y=1.71, z=-1.61, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan9:

    # # Put the bowl on the dining table and the garbage can next to it
    # controller.step(action='TeleportObject', objectId='Bowl|+01.47|+00.90|+01.26', x=-0.8140183687210083, y=0.7871422171592712, z=-1.2697957754135132, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='GarbageCan|-01.97|-00.03|+01.36', x=-0.5, y=0.1, z=-0.75, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the bread in the bowl and the plate next to the bowl
    # controller.step(action='TeleportObject', objectId='Bread|+01.03|+00.95|-00.52', x=1.47, y=1.2, z=1.26, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Plate|+02.21|+00.90|-00.46', x=2.1, y=0.91, z=1.26, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the plate next to the bowl and the pot on the plate
    # controller.step(action='TeleportObject', objectId='Plate|+02.21|+00.90|-00.46', x=2.1, y=0.91, z=1.26, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Pot|+00.30|+00.96|+01.35', x=2.1, y=0.96, z=1.26, rotation=dict(x=0, y=95, z=0), forceAction=True)


    # ### FloorPlan11:

    # # Put the potato on the plate and the pot on top of the fridge
    # controller.step(action='TeleportObject', objectId='Potato|+00.92|+00.94|-01.71', x=-0.111, y=1, z=-1.596, rotation=dict(x=0, y=95, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Pot|-02.38|+00.94|+00.58', x=-2.13, y=2, z=-1.45, rotation=dict(x=0, y=95, z=0), forceAction=True)

    
    # ### FloorPlan16:

    # # Put the mug inside the fridge, so that the robot cannot find it
    # controller.step(action='TeleportObject', objectId='Mug|-00.82|+00.84|+01.60', x=-0.90171217918396, y=0.9, z=-0.3445412218570709, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Remove the apple and the bowl from the dining table
    # controller.step(action='TeleportObject', objectId='Apple|+01.95|+00.87|+03.77', x=-2.94, y=1.12, z=0.16, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Bowl|+02.19|+00.83|+03.51', x=-2.54, y=1.12, z=-0.16, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the wine bottle inside the fridge, so that the robot cannot find it
    # controller.step(action='TeleportObject', objectId='WineBottle|+02.85|+01.02|-01.66', x=-0.90171217918396, y=0.9, z=-0.3445412218570709, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the toaster inside the cabinet, so that the robot cannot find it
    # controller.step(action='TeleportObject', objectId='Toaster|-01.01|+01.02|+02.24', x=2.47, y=0.5, z=-0.49, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the knife far back on the countertop
    # controller.step(action='TeleportObject', objectId='Knife|+01.72|+01.02|+01.72', x=3.05, y=1.05, z=-2.05, rotation=dict(x=0, y=95, z=0), forceAction=True)


    # ### FloorPlan19:

    # # Put the pot, the pan, and the lettuce inside the garbage can
    # controller.step(action='TeleportObject', objectId='Pot|-02.84|+00.91|-03.74', x=-0.4, y=0.9, z=-0.035, rotation=dict(x=0, y=0, z=0), forceAction=False)
    # controller.step(action='TeleportObject', objectId='Pan|-00.39|+00.97|-02.41', x=-0.4, y=0.9, z=-0.035, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.32|+00.99|-03.75', x=-0.4, y=0.9, z=-0.035, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Put the lettuce inside the fridge, on the shelf above the egg
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.32|+00.99|-03.75', x=-3.1071534156799316, y=1.75, z=-1.9746423959732056, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan201:

    # # Put the book on the small table, to make it inaccesible to the robot
    # controller.step(action='TeleportObject', objectId='Book|-01.87|+00.68|+01.17', x=-2.34, y=0.74, z=-0.05, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Turn on the TV
    # controller.step(action="ToggleObjectOn", objectId="Television|-02.36|+01.21|+06.24", forceAction=True)


    # ### FloorPlan202:

    # # Put the pillow on the coffee table
    # controller.step(action='TeleportObject', objectId='Pillow|-00.50|+00.69|+00.51', x=-1.65, y=0.5, z=2.36, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan204:

    # # Move the phone, coffee table, chair, and floorlamp
    # controller.step(action='TeleportObject', objectId='CellPhone|-02.22|+00.44|+03.81', x=-0.2, y=0.74, z=5.37, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='CoffeeTable|-01.97|+00.00|+04.19', x=-1.97, y=0.01, z=4.6, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Chair|-00.43|+00.01|+03.60', x=-0.43, y=0.01, z=4, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='FloorLamp|+00.39|00.00|+05.16', x=0.3, y=0.01, z=4.6, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan214:

    # # Put the remote control on the sofa
    # controller.step(action='TeleportObject', objectId='RemoteControl|-02.95|+00.46|+04.69', x=-2.4, y=0.6, z=0.7, rotation=dict(x=0, y=180, z=0), forceAction=True)


    # ### FloorPlan218:
    # # Put the cell phone in the drawer and the laptop on the chair
    # controller.step(action='TeleportObject', objectId='CellPhone|-05.35|+00.78|+04.42', x=0.748, y=0.7, z=4.098, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Laptop|-05.46|+00.78|+05.25', x=-0.139, y=0.5, z=6.41, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan302:

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|+00.47|+00.67|+01.35", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|+00.01|+01.32|+01.50", forceAction=True)


    # ### FloorPlan305:

    # # Put the laptop and the book on the shelf
    # controller.step(action='TeleportObject', objectId="Laptop|+01.22|+00.73|+01.34", x=1.3, y=1.4, z=1.4, rotation=dict(x=0, y=45, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId="Book|+01.14|+00.73|+01.80", x=1.2537, y=1.138859, z=0.9216, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|-00.40|+00.66|-01.67", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|+00.55|+01.16|+02.08", forceAction=True)


    # ### FloorPlan306:

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|-00.12|+00.90|-01.73", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|+03.51|+01.25|+00.17", forceAction=True)


    # ### FloorPlan307:

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|+00.05|+00.82|-02.48", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|-01.80|+01.21|+00.68", forceAction=True)


    # ### FloorPlan309:

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|+01.86|+00.58|+02.43", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|-00.16|+01.28|+04.00", forceAction=True)


    # ### FloorPlan310:

    # # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|-01.67|+01.77|-02.19", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|+01.90|+01.30|-01.30", forceAction=True)


    # ### FloorPlan330:

    # # Put the book on the top of the shelf
    # controller.step(action='TeleportObject', objectId='Book|-01.68|+01.14|-01.77', x=-1.58, y=2.21, z=-1.70, rotation=dict(x=0, y=0, z=0), forceAction=True)


    return True