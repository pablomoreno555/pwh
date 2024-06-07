# **Adaptive Task Planning in Home Assistant Robots: Integrating Language and Vision Models for Scene Understanding**

Pablo Moreno Moreno - IMAI Laboratory - Keio University.

**Abstract:** Recent works have shown how the reasoning capabilities of Large Language Models (LLMs) can be applied to robot task planning. These models encode a wealth of semantic knowledge about the world that could be very useful for robots aiming to act upon high-level, temporally extended instructions expressed in natural language. However, the lack of real-world experience of LLMs makes it difficult to leverage them for decision making within a concrete robot. Specially, in dynamic household environments, where the scene may change during execution and the robot might need to replan its future actions. This research aims to propose a framework that can handle unexpected situations that the robot may encounter while executing the initial plan. To achieve this, the proposal lies in autonomously understanding the scene by incorporating a Vision Question Answering (VQA) module to determine why a certain step failed to be properly executed and how to recover from that situation.

## Setup

Create a conda environment (or virtualenv) with Python 3.10:
```
conda create -n adaptive-task-planning python==3.10
```

Install dependencies:
```
pip install -r requirements.txt -v
```

## OpenAI API Key
The code relies on the OpenAI API. Create an API Key at https://platform.openai.com/.

Then create an environment variable named 'OPENAI_API_KEY' and assign it your OpenAI Key.

## Running Script
Run the following command to execute the program, replacing 'FloorPlanX' with the AI2-THOR floor plan ID you want to use (e.g. 'FloorPlan1', 'FloorPlan202', etc.).

Refer to https://ai2thor.allenai.org/demo for the layout of the various AI2-THOR floor plans.
```
python run.py FloorPlanX
```

After the AI2-THOR scene has been loaded, the program will prompt you to enter a task. Type the desired instruction and press enter.

Refer to ```test/Experiments.xlsx``` for some examples of instructions that may be given to the system.

After pressing enter, a plan will be generated by the LLM and a new window will pop up, pausing the simulation. Upon closing this window, the robot will begin to execute the plan in the environment.

At this point, the situation may lead to two different scenarios:

### A) First plan successfully executed by the robot.

If the robot is able to successfully execute all the steps of the plan, after completing the last step the system will prompt you to enter a new task.

### B) First plan failed to be properly executed.

If the robot encounters an issue while executing the initial plan, the simulation will stop and the VQA module will be queried to get the reason why the current step failed to be properly executed. After identifying the reason that caused the failure of the initial plan, the system will respond in one of two possible alternatives:

**B1) A new plan is automatically generated by the LLM.** If, considering the set of actions that this particular robot can perform, there is an alternative way to accomplish the given instruction, a new plan will be generated by the LLM. A new window will pop up and, upon closing it, the robot will begin to execute the new plan in the environment. At this point, the situation may again lead to the previous two different scenarios (A or B).

**B2) The system asks the user for further guidance.** If the limited set of skills that this particular robot can perform do not allow it to accomplish the given instruction after the challenge faced, the system will report the specific problem that prevented the robot from achieving the instruction. A new window will pop up and, upon closing it, the system will ask the user for further guidance. At this point, the user may either guide the robot to accomplish the previous instruction or prompt it to perform a different task.

The program will continuously prompt the user for new instructions. To finish its execution, type 'q', instead of entering a new instruction, and press enter.
