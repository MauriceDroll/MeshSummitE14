import torch

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from data import *
from model import *


#data_traffic = traffic_data["Richtung A nach B"]
#data_weather = weather_data[76131]

def traffic_from_output(output):
    traffic_idx = torch.argmax(output).item()
    return traffic_idx


FILE = "model.pth"
loaded_model = RNN(input_size, hidden_size, n_layers, n_traffic).to(device)
loaded_model.load_state_dict(torch.load(FILE, map_location=device))
loaded_model.eval()

# keep track of correct guesses in a confusion matrix
confusion = torch.zeros(n_traffic, n_traffic)

with torch.no_grad():
    n_correct = 0
    n_samples = 0
    
    for i in range(100):
        weather_tensor, zeitpunkt = weather_to_tensor(data_weather, 1, 7)
        traffic_tensor = traffic_to_tensor(data_traffic, zeitpunkt)
        output = loaded_model(weather_tensor)

        guess = traffic_from_output(output)
        n_samples += 1

        if guess == traffic_tensor.item():
            n_correct += 1
            correct = "✓"
        else:
            correct = "✗ (%s)" % traffic_tensor.item()

        confusion[traffic_tensor.item()][guess] += 1
        #print(guess, correct)

# normalize by dividing every row by its sum
for i in range(n_traffic):
    confusion[i] = confusion[i] / confusion[i].sum()

acc = 100.0 * n_correct / n_samples
print(f"\naccuracy = {acc:.2f} %\n")

# set up plot
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(confusion.numpy())
fig.colorbar(cax)

all_traffic = [0,1,2,3,4,5,6,7,8,9]

# set up axes
ax.set_xticklabels([''] + all_traffic, rotation=90)
ax.set_yticklabels([''] + all_traffic)

# force label at every tick
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

# sphinx_gallery_thumbnail_number = 2
plt.show()