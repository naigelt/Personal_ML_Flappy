import socket

# Server connection details
HOST = '127.0.0.1'  # The local machine's IP
PORT = 8080         # The port used by the C++ game server

# Create a socket connection to the C++ server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def reset_game():
    """
    Sends a reset command to the C++ server and retrieves the initial state of the game.
    """
    # Send a "reset" message to the C++ server (you may need to implement this on the server side)
    s.sendall(b'reset')

    # Receive the initial game state from the C++ server
    data = s.recv(1024).decode('utf-8')
    data_split = data.split()

    bird_y = float(data_split[0])
    pipe_x = float(data_split[1])
    pipe_gap_y = float(data_split[2])
    score = int(data_split[3])  # You can ignore the score if you don't need it yet

    # Return the initial state (bird_y, pipe_x, pipe_gap_y) as a list
    return [bird_y, pipe_x, pipe_gap_y]

def step(action):
    """
    Sends the selected action to the C++ server and receives the next state, reward, and whether the game is done.
    
    :param action: The action taken by the agent (1 for flap, 0 for no flap).
    :return: next_state, reward, done (boolean indicating if the game is over).
    """
    # Send the action to the C++ server: "ping" for flap or "no_ping" for no flap
    action_message = 'ping' if action == 1 else 'no_ping'
    s.sendall(action_message.encode())

    # Receive the game state and reward from the C++ server
    data = s.recv(1024).decode('utf-8')
    data_split = data.split()

    bird_y = float(data_split[0])
    pipe_x = float(data_split[1])
    pipe_gap_y = float(data_split[2])
    score = int(data_split[3])  # Can be used for debugging or learning purposes
    reward = int(data_split[4])

    # Determine if the game is over based on the reward (game over could be signaled by reward = -100)
    done = reward == -100

    # Return the next state, reward, and done status
    next_state = [bird_y, pipe_x, pipe_gap_y]
    return next_state, reward, done

