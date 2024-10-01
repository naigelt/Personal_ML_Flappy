# dqn_agent.py

import numpy as np
from q_network import create_q_network
from replay_memory import ReplayMemory

class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=64):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Epsilon decay rate
        self.epsilon_min = epsilon_min  # Minimum epsilon
        self.batch_size = batch_size
        
        # Initialize the Q-network and target Q-network
        self.q_network = create_q_network(input_size=state_size, output_size=action_size)
        self.target_q_network = create_q_network(input_size=state_size, output_size=action_size)
        
        # Initialize replay memory
        self.memory = ReplayMemory(capacity=10000)
    
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1])  # Random action (exploration)
        else:
            q_values = self.q_network.predict(np.array([state]))[0]  # Predict Q-values
            return np.argmax(q_values)  # Exploit: select action with highest Q-value
    
    def train(self):
        if len(self.memory) < self.batch_size:
            return
        
        # Sample a batch from memory
        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = np.array(states)
        next_states = np.array(next_states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        dones = np.array(dones)
        
        # Predict current Q-values using the Q-network
        q_values = self.q_network.predict(states)

        # Predict next Q-values using the target Q-network
        next_q_values = self.target_q_network.predict(next_states)
        
        for i in range(self.batch_size):
            if dones[i]:
                q_values[i][actions[i]] = rewards[i]
            else:
                q_values[i][actions[i]] = rewards[i] + self.gamma * np.max(next_q_values[i])

        # Train the Q-network
        self.q_network.fit(states, q_values, epochs=1, verbose=0)
    
    def update_target_network(self):
        # Periodically update the target network
        self.target_q_network.set_weights(self.q_network.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        # Store experience in memory
        self.memory.push((state, action, reward, next_state, done))
    
    def update_epsilon(self):
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
