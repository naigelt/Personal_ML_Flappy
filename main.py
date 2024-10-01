from dqn_agent import DQNAgent
from flappy_bird_communicator import reset_game, step  # Import reset_game and step

# Initialize the DQN agent
state_size = 3  # bird_y, pipe_x, pipe_gap_y
action_size = 2  # 0 = do nothing, 1 = flap
agent = DQNAgent(state_size, action_size)

# Goal: pass at least 10 pipes consistently
goal_pipes = 10
required_consistency = 5  # The number of consecutive episodes with pipes passed >= goal_pipes
consistent_count = 0  # Counter to track consistency

num_episodes = 1000
for episode in range(num_episodes):
    # Reset the game at the start of each episode and get the initial state
    state = reset_game()
    done = False
    total_reward = 0
    pipes_passed = 0  # Track how many pipes the agent has passed in the current episode

    # Run the episode
    while not done:
        # Select an action using epsilon-greedy policy
        action = agent.select_action(state)

        # Step through the game
        next_state, reward, done = step(action)

        # Track pipes passed
        if reward > 0:  # Assuming the reward is positive when the bird passes a pipe
            pipes_passed += 1

        # Debugging: Print the game state, action, reward, and pipes passed
        print(f"Episode: {episode}, State: {state}, Action: {action}, Reward: {reward}, "
              f"Next State: {next_state}, Done: {done}, Pipes Passed: {pipes_passed}")

        # Store the experience in replay memory
        agent.remember(state, action, reward, next_state, done)

        # Train the agent
        agent.train()

        # Update the state for the next step
        state = next_state
        total_reward += reward

    # End of episode - print total reward and total pipes passed for this episode
    print(f"Episode {episode} completed, Total reward: {total_reward}, Pipes Passed: {pipes_passed}")

    # Check if the agent passed enough pipes in this episode
    if pipes_passed >= goal_pipes:
        consistent_count += 1
        print(f"Episode {episode}: Agent passed {pipes_passed} pipes! Consecutive episodes: {consistent_count}")
    else:
        consistent_count = 0  # Reset if the agent doesn't meet the pipes passed goal
        print(f"Episode {episode}: Goal not met, resetting consistency count to 0")

    # Check if the agent has hit the pipes passed goal consistently for the required number of episodes
    if consistent_count >= required_consistency:
        print(f"Agent consistently passed {goal_pipes} pipes for {required_consistency} consecutive episodes!")
        break  # Stop training once the consistency goal is met

    # Update epsilon (exploration rate)
    agent.update_epsilon()

    # Periodically update the target Q-network
    if episode % 10 == 0:
        agent.update_target_network()
