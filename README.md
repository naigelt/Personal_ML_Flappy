All commands in this instruction are for windows, for Linux user I dont Chat-gpt if u dont know ;)
I suggest u open 2 terminals one for running python commmands and one for c++, Helps alot when when manually stopping one of the processes.
Manual stop command is CTRL + C

also in the main.cpp file u can change these to set the goals for the agent to hit.
```
# Goal: pass at least 10 pipes consistently
goal_pipes = 10
required_consistency = 5  # The number of consecutive episodes with pipes passed >= goal_pipes
consistent_count = 0  # Counter to track consistency```

Step 1: Clone or Download the Repository
You can clone the GitHub repository that contains the project code or download the project files as a ZIP.

Option 1: Clone the repository using Git:

Open Git Bash or the Command Prompt.

Navigate to the folder where you'd like to clone the repository.

Run the following command (replace your-repo-url with the actual GitHub URL of the project):
git commands:
````git clone your-repo-url
cd your-repo-folder```

Option 2: Download as a ZIP:

Go to the GitHub repository in your browser.
Click on the Code button and choose Download ZIP.
Extract the ZIP file to a directory on your machine.
Open a terminal or command prompt in the extracted folder.

You'll need MinGW-w64 to compile and run the C++ server that hosts the Flappy Bird game.

Download and install MinGW-w64:
Go to the MinGW-w64 website: MinGW-w64 Downloads.
Follow the installation instructions on the website for your platform.
After installation, add MinGW to your system’s PATH (this allows you to use g++ from the command line).
Go to Control Panel > System > Advanced System Settings > Environment Variables.
In System Variables, select Path and click Edit.
Add the path to the bin folder inside your MinGW-w64 installation (for example, C:\mingw64\bin).
Verify that MinGW is installed by running this command in your terminal:
```g++ --version```

Step 4: Install Python and Set Up a Virtual Environment
You’ll need Python 3.7 or higher to run the DQN agent. It's recommended to set up a virtual environment for the project.

Install Python:(If not installed already) ofc
Download and install Python from the official website: Python Downloads.
During installation, make sure to check the box that says Add Python to PATH.
Verify Python Installation: Open a terminal and run:
```python --version```

Create a Virtual Environment: In the project folder, create and activate a virtual environment:
```python -m venv myenv````

Activate the Virtual Environment (For windows) i dont know the command for linux google helps:
```myenv\Scripts\activate```
Upgrade pip (optional but recommended):
```python -m pip install --upgrade pip```

Step 5: Install Required Python Libraries
Once the virtual environment is activated, install the necessary Python libraries:
TensorFlow and Keras:
```pip install tensorflow```

Other dependencies (e.g., numpy, etc.): Install additional dependencies required by the DQN agent:
```pip install numpy```

Step 6: Run the Flappy Bird Game Server (C++ Program)
Start the Flappy Bird game server, which acts as the environment for the agent.

In the terminal, run the compiled Flappy Bird executable
```./flappy_bird.exe```
The terminal will output something like "Waiting for Python script connection...".

Step 7: Run the DQN Agent
Now that the Flappy Bird game server is running, you can run the Python DQN agent.

Navigate to the project directory in a new terminal or command prompt (make sure the virtual environment is activated).

Run the main.py file:
```python main.py```

The agent will connect to the C++ server, receive the game state, and begin learning by interacting with the game.

Step 8: Monitor Training
The agent will run multiple episodes of the game, training itself to pass pipes without crashing.
You will see output in the terminal showing the current episode, the number of pipes passed, and whether the agent met its goal.
You can stop the servers by using the command CTRL + C in the terminal
