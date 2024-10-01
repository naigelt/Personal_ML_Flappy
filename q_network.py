# q_network.py

import tensorflow as tf
from tensorflow.keras import layers, models

def create_q_network(input_size, output_size):
    model = models.Sequential()
    model.add(layers.Dense(128, input_dim=input_size, activation='relu'))  # First hidden layer
    model.add(layers.Dense(128, activation='relu'))  # Second hidden layer
    model.add(layers.Dense(output_size))  # Output layer: Q-values for each action
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    return model
