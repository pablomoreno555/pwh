# **Adaptive Task Planning in Home Assistant Robots: Integrating Language and Vision Models for Scene Understanding**

Pablo Moreno Moreno - IMAI Laboratory - Keio University.

**Abstract:** Recent works have shown how the reasoning capabilities of Large Language Models (LLMs) can be applied to robot task planning. These models encode a wealth of semantic knowledge about the world that could be very useful for robots aiming to act upon high-level, temporally extended instructions expressed in natural language. However, the lack of real-world experience of LLMs makes it difficult to leverage them for decision making within a concrete robot. Specially, in dynamic household environments, where the scene may change during execution and the robot might need to replan its future actions. This research aims to propose a framework that can handle unexpected situations that the robot may encounter while executing the initial plan. To achieve this, the proposal lies in autonomously understanding the scene by incorporating a Vision Question Answering (VQA) module to determine why a certain step failed to be properly executed and how to recover from that situation.

## Setup

Create a conda environment (or virtualenv) with Python 3.10:
```
conda create -n task-planning-llm python==3.10
```

Install dependencies:
```
pip install -r requirements.txt
```

## OpenAI API Key
The code relies on OpenAI API. Create an API Key at https://platform.openai.com/.

Then create an environment variable named 'OPENAI_API_KEY' and assign it your OpenAI Key.

## Running Script
Run the following command to execute the main Python program:
```
python main.py
```

Refer to https://ai2thor.allenai.org/demo for the layout of various AI2Thor floor plans.

