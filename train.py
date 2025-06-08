import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dataset import CustomDataset
from model import SimpleLSTMModel
from pathlib import Path


def one_hot_encode(x, vocab_size):
    return F.one_hot(x, num_classes=vocab_size).float()

import re

def generate_sample(model, char2idx, idx2char, device, allowed_chars, max_len=120, temperature=1.0):
    model.eval()
    input_ids = torch.tensor([[char2idx[' ']]], dtype=torch.long).to(device)
    hidden = None
    generated = []

    for _ in range(max_len):
        x_onehot = one_hot_encode(input_ids, len(char2idx)).to(device)
        output, hidden = model(x_onehot, hidden)
        logits = output[0, -1] / temperature
        probs = torch.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, 1).item()
        next_char = idx2char[next_id]

        if next_char in allowed_chars:
            generated.append(next_char)

        input_ids = torch.tensor([[next_id]], device=device)

    # Join and extract valid hex codes
    raw = ''.join(generated)
    colors = re.findall(r"#([0-9A-Fa-f]{6})", raw)

    # Format the first 4 into correct output
    if len(colors) >= 4:
        colors = colors[:4]
        return [f"#{c.upper()}" for c in colors]
    else:
        return []


def train():
    base_path = Path(__file__).resolve().parent
    data_file = base_path / "Data" / "data.txt"

    dataset = CustomDataset(data_file)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True, drop_last=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train.py] Using device: {device}")

    model = SimpleLSTMModel(dataset.vocab_size).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    epochs = 50
    sample = []
    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for x, y in dataloader:
            x, y = x.to(device), y.to(device)
            x_onehot = one_hot_encode(x, dataset.vocab_size)
            optimizer.zero_grad()
            output, _ = model(x_onehot)
            loss = F.cross_entropy(output.view(-1, dataset.vocab_size), y.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")

        # Generate sample text at the end of each epoch
        sample = generate_sample(model, dataset.char2idx, dataset.idx2char, device, dataset.allowed_chars, temperature=0.8)
        print(f"Sample output: {sample}")
        model.train()
    torch.save(model.state_dict(), "color_model.pth")
    return sample

if __name__ == "__main__":
    train()
