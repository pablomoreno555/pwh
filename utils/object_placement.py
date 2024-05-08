def place_objects(controller):

    # ### FloorPlan16:

    # Put the mug inside the fridge, so that the robot cannot find it
    # controller.step(action='TeleportObject', objectId='Mug|-00.82|+00.84|+01.60', x=-0.90171217918396, y=0.9, z=-0.3445412218570709, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # Move the chairs so that the dining table is not accessible by the robot
    # controller.step(action='TeleportObject', objectId='Chair|+02.76|+00.00|+03.09', x=1.7, y=0, z=3.09, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Chair|+01.62|+00.00|+04.31', x=1.55, y=0, z=3.5, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan19:

    # Take the egg out of the fridge and the tomato out of the counter and place them on the dining table
    # controller.step(action='TeleportObject', objectId='Egg|-03.11|+01.03|-01.97', x=-2.4584720134735107, y=0.9277706146240234, z=-0.5684570074081421, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Tomato|-02.16|+00.95|-03.71', x=-2.4584720134735107, y=0.9277706146240234, z=-0.5684570074081421, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # Put the pot, the pan, and the lettuce inside the garbage can
    # controller.step(action='TeleportObject', objectId='Pot|-02.84|+00.91|-03.74', x=-0.4, y=0.9, z=-0.035008691251277924, rotation=dict(x=0, y=0, z=0), forceAction=False)
    # controller.step(action='TeleportObject', objectId='Pan|-00.39|+00.97|-02.41', x=-0.4, y=0.9, z=-0.035008691251277924, rotation=dict(x=0, y=0, z=0), forceAction=True)
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.32|+00.99|-03.75', x=-0.4, y=0.9, z=-0.035008691251277924, rotation=dict(x=0, y=0, z=0), forceAction=True)

    # Disable the dining table
    # controller.step(action="DisableObject", objectId="DiningTable|-02.80|+00.00|-00.51")

    # Put the lettuce inside the fridge, where the egg was
    # controller.step(action='TeleportObject', objectId='Lettuce|-01.32|+00.99|-03.75', x=-3.1071534156799316, y=1.05, z=-1.9746423959732056, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan9:

    # Put the bowl on the dining table
    # controller.step(action='TeleportObject', objectId='Bowl|+01.47|+00.90|+01.26', x=-0.8140183687210083, y=0.7871422171592712, z=-1.2697957754135132, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan330:

    # Put the book on the top of the shelf
    # controller.step(action='TeleportObject', objectId='Book|-01.68|+01.14|-01.77', x=-1.58, y=2.21, z=-1.70, rotation=dict(x=0, y=0, z=0), forceAction=True)


    # ### FloorPlan310:

    # Turn off the desk lamp and the light switch
    # controller.step(action="ToggleObjectOff", objectId="DeskLamp|-01.67|+01.77|-02.19", forceAction=True)
    # controller.step(action="ToggleObjectOff", objectId="LightSwitch|+01.90|+01.30|-01.30", forceAction=True)

    # Move the side table
    # controller.step(action='TeleportObject', objectId='SideTable|+01.69|+00.00|-00.99', x=1.69, y=0, z=-1.5, rotation=dict(x=0, y=0, z=0), forceAction=True)

    return True