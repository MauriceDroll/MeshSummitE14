# imports
import math
import random

import torch
import torch.nn as nn

import matplotlib as mpl
import matplotlib.pyplot as plt

from model import *
from data import *

# Trains the network with the specified data
def train(weather_tensor, traffic_tensor):
    output = model(weather_tensor)
    loss = criterion(output, traffic_tensor)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    return output, loss.item()

def traffic_from_output(output):
    traffic_idx = torch.argmax(output).item()

    return traffic_idx


learning_rate = 0.0001

# Initialize neural network   
model = RNN(input_size, hidden_size, n_layers, n_traffic).to(device)

# Loss and optimizer
criterion = nn.NLLLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

current_loss = 0
all_losses = []

print_every = 5000
plot_every = 1000
n_iters = 500000

#def timeSince(since):
    #now = time.time()
    #s = now - since
    #m = math.floor(s / 60)
    #s -= m * 60
    #return '%dm %ds' % (m, s)

#start = time.time()

# Iterate over weather and traffic data
for i in range(1, n_iters + 1):
    # Character, file, character_tensor, file_tensor = random_training_example(character_files, all_characters)
    weather_tensor, zeitpunkt = weather_to_tensor(data_weather, 1, 7)
    traffic_tensor = traffic_to_tensor(data_traffic, zeitpunkt) 
    output, loss = train(weather_tensor.to(device), traffic_tensor.to(device))
    current_loss += loss
    
    # Print iter number, loss, name and guess
    if i % print_every == 0:
        guess = traffic_from_output(output)
        correct = '✓' if guess == traffic_tensor.item() else '✗ (%s)' % traffic_tensor.item()
        #print('%d %d%% (%s) %.4f %s / %s %s' % (i, i / n_iters * 100, timeSince(start), loss, file, guess, correct))
        print('%d %d%% %.4f %s / %s %s' % (i, i / n_iters * 100, loss, file, guess, correct))

    # Add current loss avg to list of losses
    if i % plot_every == 0:
        all_losses.append(current_loss / plot_every)
        current_loss = 0

# Create figure
mpl.style.use("seaborn-whitegrid")
plt.figure(figsize=(12,6))
# Create plot
plt.plot(all_losses)
# Add title and labels
plt.title("LOSS-function", fontsize=20)
plt.xlabel("iterations", fontsize=15)
plt.ylabel("loss", fontsize=15)

# Show plot
plt.show()


FILE = "model.pth"
#torch.save(model.state_dict(), FILE)