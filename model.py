import torch.nn as nn

class SimpleLSTMModel(nn.Module):
    def __init__(self, vocab_size, hidden_size=128):
        super().__init__()
        self.lstm = nn.LSTM(input_size=vocab_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden  # Return output and hidden state
