import torch
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, filepath):
        # Add '<' and '>' because your data uses <START> and <END>
        self.allowed_chars = list("#0123456789ABCDEF[], \" \t<>") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ['.', '?', '!', ':']
        raw_lines = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line.strip().upper())   # print the line as-is (strip removes trailing newline)
                raw_lines.append(line.upper().strip())  # Convert to uppercase and strip whitespace

        print(f"1{raw_lines[0]}")
        # Filter lines that contain only allowed chars
        self.lines = [line for line in raw_lines if all(c in self.allowed_chars for c in line)]
        print(f"[dataset.py] Loaded {len(self.lines)} valid lines from {filepath}")
        
        if len(self.lines) == 0:
            raise ValueError(f"No valid lines found in {filepath}. Check your data and allowed chars.")
        
        self.vocab = sorted(set(self.allowed_chars))
        self.char2idx = {c: i for i, c in enumerate(self.vocab)}
        self.idx2char = {i: c for c, i in self.char2idx.items()}
        self.vocab_size = len(self.vocab)

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        line = self.lines[idx]
        x = torch.tensor([self.char2idx[c] for c in line[:-1]], dtype=torch.long)
        y = torch.tensor([self.char2idx[c] for c in line[1:]], dtype=torch.long)
        return x, y
