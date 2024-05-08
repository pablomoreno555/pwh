from openai import OpenAI
from ai2thor.controller import Controller
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import json
import re
from PIL import Image
from utils import navigation, object_finding, object_scanning, object_placement
import base64
import requests
import time


# --------------------- AI2THOR --------------------- #


def extract_argument(step, argument_name):
    """
    Extract the value of the specified argument from the specified step string
    """
    # Scan through the string "step" looking for a JSON-like structure within it
    json_match = re.search(r'{.*}', step)
    # Ensure a JSON match was found before proceeding
    if json_match:
        # Extract the matched JSON-like string
        json_string = json_match.group(0)
        # Parse the JSON-like string to a Python dictionary
        argument_dict = json.loads(json_string)
        # Extract the value associated to the specified argument, print it, and return it
        argument_value = argument_dict.get(argument_name, f"{argument_name} argument not found")
        print(f"The {argument_name} argument is:", argument_value)
        return argument_value
    else:
        print(f"No JSON-like structure found in the string {step}")


def normalize_string(s):
    """
    Normalize the input string by removing spaces and converting to lower case
    """
    return ''.join(s.split()).lower()


def get_object_info(object):
    """
    Return the corresponding objectType and objectID of the input object string
    """
    for obj in controller.last_event.metadata['objects']:
        if normalize_string(obj['objectType']) == normalize_string(object):
            return obj['objectType'], obj['objectId']
            
            
def take_photos():
    """
    Take photos of the scene from the robot's perspective, with different camera angles
    """
    # Reset the camera angle to the neutral orientation
    controller.step(action="Teleport", horizon=0)

    # Take a photo of what the robot sees when it is standing, rotated 45 deg left, and with a camera angle of -30 deg (i.e., looking slightly up)
    event = controller.step(action='RotateLeft', degrees=45)
    event = controller.step(action="LookUp", degrees=30)
    image_data = event.frame
    img = Image.fromarray(image_data, 'RGB')
    img.save("ph1_Left-30.jpg")
    
    # Take a photo of what the robot sees when it is standing, rotated 45 deg left, and with a camera angle of 50 deg (i.e., looking far down)
    event = controller.step(action="LookDown", degrees=80)
    image_data = event.frame
    img = Image.fromarray(image_data, 'RGB')
    img.save("ph2_Left50.jpg")

    # Take a photo of what the robot sees when it is standing, rotated 45 deg right, and with a camera angle of 50 deg (i.e., looking far down)
    event = controller.step(action='RotateRight', degrees=90)
    image_data = event.frame
    img = Image.fromarray(image_data, 'RGB')
    img.save("ph3_Right50.jpg")

    # Take a photo of what the robot sees when it is standing, rotated 45 deg right, and with a camera angle of -30 deg (i.e., looking slightly up)
    event = controller.step(action="LookUp", degrees=80)
    image_data = event.frame
    img = Image.fromarray(image_data, 'RGB')
    img.save("ph4_Right-30.jpg")

    # Reset the robot's rotation and the camera angle to the neutral orientation
    controller.step(action='RotateLeft', degrees=45)
    controller.step(action="Teleport", horizon=0)

        
def execute_plan(step_list):
    """
    Execute the generated list of steps in the environment, one step per loop iteration
    """
    for step in step_list:
    
        global step_failed, grasped_object, known_positions
        print("\n", step)
        # Get the name of the action to execute in this step (e.g. "go_to", "pick_up"...)
        action = re.search(r'\d+\.\s(\w+):', step).group(1)

        if action == "find":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object we want to find
            object_type, object_id = get_object_info(object)

            # Try to find the specified object using the implemented object_finding package
            object_position = object_finding.find_object(controller, object_id)

            if object_position != None:
                print(f"{object_type} found successfully!")

                # Add the location of this object to the list of known positions
                known_positions.append({'objectId': object_id, 'position': object_position})

                # Reset the camera angle to the neutral orientation
                controller.step(action="Teleport", horizon=0)

            else:

                # Iterate over the list of known positions to check if the robot already knows the position of this object
                for item in known_positions:
                    if item['objectId'] == object_id:
                        object_position = item['position']
                
                if object_position != None:
                     print(f"{object_type} had been found found at {object_position}")

                else:
                    print(f"The robot was not able to find the {object_type}")
                    print(controller.last_event)

                    # Take photos of the scene from the robot's perspective, with different camera angles
                    take_photos()

                    # Indicate that the robot failed to execute this step
                    step_failed = step
                    break


        elif action == "go_to":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object we want to move to
            object_type, object_id = get_object_info(object)

            # Get the position of the target object from the list of known positions, obtained with the find action
            object_position = None
            for item in known_positions:
                if item['objectId'] == object_id:
                    object_position = item['position']
            
            if object_position != None:
                print(f"{object_type} position: {object_position}")

                # Move the robot to the closest reachable position to the object using the A* pathfinding algorithm implemented in the navigation package
                if navigation.navigate_to(controller, object_position):

                    # Once the robot has arrived to the object, turn around until it is visible
                    object_position = object_finding.find_object(controller, object_id)
                    if object_position != None:
                        print(f"Moved to {object_type} successfully!")

                    else:
                        print(f"The robot moved to {object_type}, but was unable to look at it")
                        print(controller.last_event)
                    
                else:
                    print(f"The robot was not able to move to {object_type}")
                    print(controller.last_event)

                    # Take photos of the scene from the robot's perspective, with different camera angles
                    take_photos()

                    # Indicate that the robot failed to execute this step
                    step_failed = step
                    break

            else:
                print(f"Error: {object_type} position not known")


        elif action == "pick_up":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object we want to pick up
            object_type, object_id = get_object_info(object)

            # Get the position of the target object from the list of known positions, obtained with the find action
            object_position = None
            for item in known_positions:
                if item['objectId'] == object_id:
                    object_position = item['position']

            # If the target object is too high, the robot can't reach it
            if object_position != None and object_position['y'] > 2.0:
                print(f"The {object_type} is out of the robot's reach")

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break

            # If the target object has previously been sliced, pick up one of the slices
            event = controller.step(action='Pass')
            for obj in event.metadata['objects']:
                if obj['objectType'] == object_type:
                    if obj['isSliced']:
                        object = object_type + "Sliced"
                        # Get the objectType and objectId of the slice
                        object_type, object_id = get_object_info(object)
                    break

            # Try to pick up the specified object
            event = controller.step(action="PickupObject", objectId=object_id, forceAction=True, manualInteract=False)

            if event.metadata['lastActionSuccess']:
                print(f"{object_type} picked up successfully!")

                # Disable the grasped object to avoid it colliding with obstacles while the robot is moving
                grasped_object = object_id
                controller.step(action="DisableObject", objectId=grasped_object)

            else:
                print(f"The robot was not able to pick up the {object_type}")
                print(controller.last_event)

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break


        elif action == "put_down_grasped_object_on":

            # Extract the value of the argument "receptacle"
            receptacle = extract_argument(step, "receptacle")

            # Get the objectType and objectId of the receptacle we want to place the grasped object on
            receptacle_type, receptacle_id = get_object_info(receptacle)

            if receptacle_type == "Sink":
                receptacle_type, receptacle_id = get_object_info("SinkBasin")

            # Enable back the grasped object, which was disabled while the robot was moving
            controller.step(action="EnableObject", objectId=grasped_object)

            # Put the object that the robot is currently holding on the specified receptacle
            event = controller.step(action="PutObject", objectId=receptacle_id, forceAction=True, placeStationary=False)

            if event.metadata['lastActionSuccess']:
                print(f"Grasped object placed on the {receptacle_type} successfully!")
                grasped_object = None

            else:
                print(f"The robot was not able to place the grasped object on the {receptacle_type}")
                print(controller.last_event)

                # Disable the grasped object so that it does not appear in the photos
                controller.step(action="DisableObject", objectId=grasped_object)

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break

        
        elif action == "toggle":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object that we want to toggle
            object_type, object_id = get_object_info(object)

            # Get the position of the target object from the list of known positions, obtained with the find action
            object_position = None
            for item in known_positions:
                if item['objectId'] == object_id:
                    object_position = item['position']

            # If the target object is too high, the robot can't reach it
            if object_position != None and object_position['y'] > 1.70:
                print(f"The {object_type} is out of the robot's reach")

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break

            else:

                if object_type == "RemoteControl":

                    # Get the objectType and objectId of the TV
                    television_type, television_id = get_object_info("television")

                    # Check if the TV is ON or OFF
                    isOn = False
                    event = controller.step(action='Pass')
                    for obj in event.metadata['objects']:
                        if obj['objectType'] == television_type:
                            if obj['isToggled']:
                                isOn = True
                            break

                    if isOn:
                        # Toggle the TV to the OFF state
                        event = controller.step(action="ToggleObjectOff", objectId=television_id)
                    else:
                        # Toggle the TV to the ON state
                        event = controller.step(action="ToggleObjectOn", objectId=television_id)

                    if event.metadata['lastActionSuccess']:
                        print(f"{television_type} toggled successfully!")

                    else:
                        print(f"The robot was not able to toggle the {television_type}")
                        print(controller.last_event)

                        # Take photos of the scene from the robot's perspective, with different camera angles
                        take_photos()

                        # Indicate that the robot failed to execute this step
                        step_failed = step
                        break

                else:

                    # Check if the object to toggle is ON or OFF
                    isOn = False
                    event = controller.step(action='Pass')
                    for obj in event.metadata['objects']:
                        if obj['objectType'] == object_type:
                            if obj['isToggled']:
                                isOn = True
                            break

                    if isOn:
                        # Toggle the specified object to the OFF state
                        event = controller.step(action="ToggleObjectOff", objectId=object_id)
                    else:
                        # Toggle the specified object to the ON state
                        event = controller.step(action="ToggleObjectOn", objectId=object_id)

                    if event.metadata['lastActionSuccess']:
                        print(f"{object_type} toggled successfully!")

                    else:
                        print(f"The robot was not able to toggle the {object_type}")
                        print(controller.last_event)

                        # Take photos of the scene from the robot's perspective, with different camera angles
                        take_photos()

                        # Indicate that the robot failed to execute this step
                        step_failed = step
                        break


        elif action == "slice":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object that we want to slice
            object_type, object_id = get_object_info(object)
                    
            # Slice the specified object
            event = controller.step(action="SliceObject", objectId=object_id)

            if event.metadata['lastActionSuccess']:
                print(f"{object_type} sliced successfully!")

            else:
                print(f"The robot was not able to slice the {object_type}")
                print(controller.last_event)

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break


        elif action == "open":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object that we want to open
            object_type, object_id = get_object_info(object)
        
            # Open the specified object
            event = controller.step(action="OpenObject", objectId=object_id, openness=1, forceAction=False)

            if event.metadata['lastActionSuccess']:
                print(f"{object_type} opened successfully!")

            else:
                print(f"The robot was not able to open the {object_type}")
                print(controller.last_event)

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break

        
        elif action == "close":

            # Extract the value of the argument "object"
            object = extract_argument(step, "object")

            # Get the objectType and objectId of the object that we want to close
            object_type, object_id = get_object_info(object)
        
            # Close the specified object
            event = controller.step(action="CloseObject", objectId=object_id, forceAction=False)

            if event.metadata['lastActionSuccess']:
                print(f"{object_type} closed successfully!")

            else:
                print(f"The robot was not able to close the {object_type}")
                print(controller.last_event)

                # Take photos of the scene from the robot's perspective, with different camera angles
                take_photos()

                # Indicate that the robot failed to execute this step
                step_failed = step
                break


        elif action == "wait":

            event = controller.step(action='Pass')

            # Extract the value of the argument "seconds"
            seconds = extract_argument(step, "seconds")

            print(f"Waiting {seconds} seconds")

            # Pause the simulation for only 5 seconds, regardless of the specified time, so that the simulation does not last too long
            time.sleep(5)


        # Pause the simulation displaying the robot's current view
        # event = controller.step(action='Pass')
        # plt.imshow(event.frame)
        # plt.show()


# --------------------- VQA --------------------- #

def add_message_to_history(speaker, message):
    """
    Add a system or LLM message to the conversation history
    """
    conversation_history.append(f"## {speaker}:\n{message}\n")


def encode_image(image_path):
    """
    Encode the images to pass to GPT4-V
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def trigger_vqa():
    """
    Manage the VQA interaction between the system and the LLM after a step has failed to be successfully executed
    """
    # Paths to the images
    image_path1 = "ph1_Left-30.jpg"
    image_path2 = "ph2_Left50.jpg"
    image_path3 = "ph3_Right50.jpg"
    image_path4 = "ph4_Right-30.jpg"

    # Get the base64 string
    base64_image1 = encode_image(image_path1)
    base64_image2 = encode_image(image_path2)
    base64_image3 = encode_image(image_path3)
    base64_image4 = encode_image(image_path4)

    # Build the headers
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
    }

    # Message to get the reason WHY the previous step failed to be properly executed
    prompt2 = f"You are an excellent assistant in analyzing images for scene understanding. Given four images that represent what the robot sees from different perspectives and orientations after failing to execute a certain action, you can identify the reason that prevented the robot from successfully executing that action. Examples of failure reasons could include obstacles or misplaced objects. Issues like invisibility in the images of the object that the robot is moving to are not valid failure reasons, since the robot must already know where the object is to be able to go to it, so you must not give this reason. From the four images provided, you must consider only those with relevant information. Your reply must be short and concise. Now while the robot was trying to achieve the given instruction by following the above plan, it failed at step '{step_failed}'. Given these images taken by the robot after being unable to '{step_failed}', please determine why the robot couldn't execute this step."
    
    add_message_to_history("System", prompt2)

    # The prompt is sent to the LLM
    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "\n".join(conversation_history)
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image1}"
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image2}"
            }
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image3}"
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image4}"
            },
            }
        ]
        }
    ],
    }

    # Get the reply from the LLM
    raw_reply = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    reply2 = raw_reply.json()['choices'][0]['message']['content']

    add_message_to_history("LLM", reply2)
    print(f"\nLLM: {reply2}")
   
    # Message to get HOW to proceed next
    prompt3 = f"You are an excellent decision maker. Given the problem identified above, the list of actions that the robot can perform, and the objects available in the scene, you can determine if there is an alternative way for the robot to still accomplish the given instruction despite the identified challenge. Your reply can only be of two different types:\nType A: If there is an alternative way to achieve the instruction by using only the actions and objects previously defined, you must reply with a new plan composed of the steps needed to accomplish it. For example, if the alternative plan to accomplish the instruction 'light up the room' were to turn on the lamp, your reply should look like:\n1. find: {{\"object\": \"Lamp\"}}\n2. go_to: {{\"object\": \"Lamp\"}}\n3. toggle: {{\"object\": \"Lamp\"}}\nAgain, your output must be limited to a list of action names with arguments: no explanations, no introductory paragraph, no concluding statement, and with every step in a new line. Type B: If the robot is unable to accomplish the given instruction by using only the actions and objects previously defined, you must ask for external help, reporting the specific problem that it is facing, in order to make it easier for it to be helped by a human.\nYou should give a reply of Type A only when there is a clear alternative way to achieve the instruction despite the identified problem. Otherwise, give a reply of Type B. Your reply must start with the characters \"A\" or \"B\", respectively. Now please perform the specified task for the case described above, in which the instruction is: '{instruction}'"

    add_message_to_history("System", prompt3)

    # The prompt is sent to the LLM
    completion = client.chat.completions.create(
        model= "gpt-4-turbo",
        messages=[{"role": "user", "content": "\n".join(conversation_history)}]
    )

    # Get the reply from the LLM
    reply3 = completion.choices[0].message.content

    add_message_to_history("LLM", reply3)
    print(f"\nLLM: {reply3}")

    return reply3


# --------------------- MAIN --------------------- #


# Get the AI2-THOR floor plan ID given as argument
if len(sys.argv) > 1:
    floor_plan_id = sys.argv[1]
    print(f"Initializing the scene {floor_plan_id} ...\n")
else:
    print("No argument provided. Please provide the AI2-THOR floor plan ID when running the script.")

# Initialize the ai2thor controller
# FloorPlan201, (FloorPlan202) / FloorPlan16, FloorPlan19, FloorPlan9 / FloorPlan330, FloorPlan310
controller = Controller(scene=floor_plan_id, gridSize=0.3, visibilityDistance=6, fieldOfView=120, width=1200, height=800)

# Randomize the materials of all the elements in the scene
# event = controller.step(action="RandomizeMaterials", useTrainMaterials=None, useValMaterials=None, useTestMaterials=None, inRoomTypes=None)
event = controller.step(action='Pass')

# Scan the environment to get the list of objects available in the scene
# object_list = object_scanning.get_objects(controller)
object_list = []
for obj in event.metadata['objects']:
    object_list.append(obj['objectType'])

# Modify the position of some objects within the scene as desired
object_placement.place_objects(controller)

# Access the OPENAI_API_KEY environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    print("The OPENAI_API_KEY environment variable is not set")

# Read the file that contains the definition of all the actions that the robot can perform
with open('utils/actions.json', 'r') as file:
    actions = file.read()

# Read the file that contains the task guidelines
with open('utils/guidelines.txt', 'r') as file:
    guidelines = file.read()

# Create a client object to be able to make requests to GPT
client = OpenAI()

# Initialize an empty list to store the conversation between the system and the LLM
conversation_history = []

# Message that contains the definition of all the actions that the robot can perform, the task guidelines, and the list of objects available in the scene
initial_msg = f"The following file contains the definition of all the actions that a certain robot can perform:\n{actions}\nThe following file contains some task guidelines:\n{guidelines}\nAnd the following list contains most of the objects available in the scene (but not necessarily all of them): {object_list}"

add_message_to_history("System", initial_msg)

# instruction = "Can you turn on the TV?"
# instruction = "Make me a coffee and bring it to the dining table."
# instruction = "Can you bring me an apple to the dining table? I think they are in the fridge."
# instruction = "Bring me the bread to the dining table."
# instruction = "Throw away the potato and the tomato"
# instruction = "Bring my book to the bed"
# instruction = "The room is dark"
# instruction = "Slice the bread and bring me a piece to the dining table"
# instruction = "Can you bring me the lettuce to the dining table? I think it is in the fridge."
# instruction = "Can you bring me my book to the sofa?"
# instruction = "Can you bring me my laptop to the coffee table?"
# instruction = "Can you bring me the tissue box to the sofa"
# instruction = "Bring me a fruit or a vegetable to the dining table."

# Ask the user for an instruction
instruction = input("How can I help you?\n\n")

# If the robot picks up an object, this variable will be set to the objectId of that object while the robot is holding it
grasped_object = None

# This list will store the position of all the objects that the robot finds during execution
known_positions = []

while instruction != 'No':

    # If a certain step of the plan fails to be properly executed, this variable will be set to the name of that step
    step_failed = None

    prompt1 = f"You are an excellent task planner. Given a high-level instruction in natural language, you can generate a plan composed of actions that a certain robot can perform in the environment. For example, if the instruction were: 'Can you bring my book to the dining table?', your output should look like:\n1. find: {{\"object\": \"Book\"}}\n2. go_to: {{\"object\": \"Book\"}}\n3. pick_up: {{\"object\": \"Book\"}}\n4. find: {{\"object\": \"DiningTable\"}}\n5. go_to: {{\"object\": \"DiningTable\"}}\n6. put_down_grasped_object_on: {{\"receptacle\": \"DiningTable\"}}\n Your output must be limited to a list of action names with arguments: no explanations, no introductory paragraph, no concluding statement, and with every step in a new line. Now using only the actions defined in the previously provided file and following the task guidelines, please generate a plan composed of steps that the robot can follow to accomplish the following instruction: '{instruction}'. You can only use the objects present in the previous list and the objects included in the instruction '{instruction}'. The names of the actions included in the plan must exactly match those in the actions file, whereas the names of the arguments must exaclty match those included in either the objects list or the instruction, not including anything that is not there."

    if grasped_object != None:
        prompt1 += f"\nNote that the robot is currently holding {grasped_object[:grasped_object.find('|')]}"

    add_message_to_history("System", prompt1)

    # The first prompt is sent to the LLM
    completion = client.chat.completions.create(
        model= "gpt-4-turbo",
        messages=[{"role": "user", "content": "\n".join(conversation_history)}]
    )

    # Get the reply from the LLM
    reply1 = completion.choices[0].message.content

    add_message_to_history("LLM", reply1)

    # Convert the plan into a list of steps
    plan = reply1
    step_list = plan.split('\n')
    print("\nPlan:")
    for step in step_list:
        print(step)

    event = controller.step(action='Pass')
    plt.imshow(event.frame)
    plt.show()

    # Try to execute all the steps in the list
    execute_plan(step_list)

    # If all the steps were able to be successfully executed
    if step_failed == None:
        print("\nInstruction accomplished!\n")

        event = controller.step(action='Pass')
        plt.imshow(event.frame)
        plt.show()

        # Ask the user for a new instruction
        instruction = input("Is there anything else I could help you with?\n\n")


    # If one of the steps failed to be properly executed
    else:

        # Begin the VQA interaction with the LLM and, ultimately, get the reply to how to proceed next (Type A or B)
        reply = trigger_vqa()

        # If the reply is of Type A...
        if reply[0] == 'A':
            lines = reply.split('\n')
            plan = '\n'.join(lines[1:])

            event = controller.step(action='Pass')
            plt.imshow(event.frame)
            plt.show()

            # Convert this plan into a list in which each element corresponds to a step of the plan
            step_list = plan.split('\n')

            # In case that a certain step of the new plan fails to be properly executed, this variable will be set to the name of that step
            step_failed = None

            # Try to execute all the steps in the list
            execute_plan(step_list)

            # If all the steps of the new plan were able to be successfully executed
            if step_failed == None:
                print("\nInstruction accomplished!\n")

                event = controller.step(action='Pass')
                plt.imshow(event.frame)
                plt.show()
            
                # Ask the user for a new instruction
                instruction = input("Is there anything else I could help you with?\n\n")


            # If one of the steps failed to be properly executed
            else:

                # Begin the VQA interaction with the LLM and, ultimately, get the reply to how to proceed next (Type A or B)
                reply = trigger_vqa()

                # If the reply is of Type A...
                if reply[0] == 'A':
                    lines = reply.split('\n')
                    plan = '\n'.join(lines[1:])

                    event = controller.step(action='Pass')
                    plt.imshow(event.frame)
                    plt.show()

                    # Convert this plan into a list in which each element corresponds to a step of the plan
                    step_list = plan.split('\n')

                    # In case that a certain step of the new plan fails to be properly executed, this variable will be set to the name of that step
                    step_failed = None

                    # Try to execute all the steps in the list
                    execute_plan(step_list)

                    # If all the steps of the new plan were able to be successfully executed
                    if step_failed == None:
                        print("\nInstruction accomplished!\n")

                        event = controller.step(action='Pass')
                        plt.imshow(event.frame)
                        plt.show()

                        # Ask the user for a new instruction
                        instruction = input("Is there anything else I could help you with?\n\n")
                    

                    # If one of the steps failed to be properly executed
                    else:

                        # Begin the VQA interaction with the LLM and, ultimately, get the reply to how to proceed next (Type A or B)
                        reply = trigger_vqa()
                        print("\nInstruction not accomplished.\n")

                        event = controller.step(action='Pass')
                        plt.imshow(event.frame)
                        plt.show()
                        
                        # Ask the user for a new instruction
                        instruction = input("Please provide further guidance or ask a new instruction\n\n")


                # If the reply is of Type B...
                else:
                    lines = reply.split('\n')
                    help_message = '\n'.join(lines[1:])

                    print("\nInstruction not accomplished.\n")
                    
                    event = controller.step(action='Pass')
                    plt.imshow(event.frame)
                    plt.show()

                    # Ask the user for a new instruction
                    instruction = input("Please provide further guidance or ask a new instruction\n\n")


        # If the reply is of Type B...
        else:
            lines = reply.split('\n')
            help_message = '\n'.join(lines[1:])

            print("\nInstruction not accomplished.\n")
            
            event = controller.step(action='Pass')
            plt.imshow(event.frame)
            plt.show()
            
            # Ask the user for a new instruction
            instruction = input("Please provide further guidance or ask a new instruction\n\n")