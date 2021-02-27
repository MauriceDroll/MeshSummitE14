import torch

from data import *
from model import *


def traffic_from_output(output):
    traffic_idx = torch.argmax(output).item()
    return traffic_idx


FILE = "model.pth"
loaded_model = RNN(input_size, hidden_size, n_layers, n_traffic).to(device)
loaded_model.load_state_dict(torch.load(FILE, map_location=device))
loaded_model.eval()


def predivtive_traffic(weather_tensor):
    with torch.no_grad():    
        output = loaded_model(weather_tensor)
        guess = traffic_from_output(output)
    return guess