# Imports
import torch
import torch.nn as nn

# Device used for the neural network
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Recurrent neural network integration
class RNN(nn.Module):
    # Intitalizes the recurrent neural network
    def __init__(self, input_size, hidden_size, n_layers, n_traffic):
        super(RNN, self).__init__()
        self.n_layers = n_layers
        self.hidden_size = hidden_size

        self.lstm = nn.LSTM(input_size, hidden_size, n_layers, batch_first=False)
        # Parameter x of shape (seq_len, batch, hidden_size)
        self.fc = nn.Linear(hidden_size, n_traffic)
        self.softmax = nn.LogSoftmax(dim = 1)

    # Fowards data to the neural network
    def forward(self, x):
        # Initial hidden & cell state
        h0 = torch.zeros(self.n_layers, x.size(1), self.hidden_size).to(device)
        c0 = torch.zeros(self.n_layers, x.size(1), self.hidden_size).to(device)

        # Output of shape (seq_len, batch, n_directions * hidden_size)
        out, _ = self.lstm(x, (h0,c0))
        
        # Only last time step
        out = out[-1, :, :]
        
        out = self.fc(out)
        out = self.softmax(out)

        return out


# Hyper parameters
input_size = 7
n_traffic = 10
hidden_size = 128
n_layers = 1