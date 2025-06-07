import random
import json
from pathlib import Path
import os
file_path = r"C:/ai/Data/data.txt"

# Dictionary of professional hex colors
professional_colors = {
    "#1A1A1A": "#1A1A1A",
    "#FFFFFF": "#FFFFFF",
    "#007ACC": "#007ACC",
    "#F2F2F2": "#F2F2F2",
    "#2C3E50": "#2C3E50",
    "#ECF0F1": "#ECF0F1",
    "#3498DB": "#3498DB",
    "#BDC3C7": "#BDC3C7",
    "#0F172A": "#0F172A",
    "#E2E8F0": "#E2E8F0",
    "#2563EB": "#2563EB",
    "#F8FAFC": "#F8FAFC",
    "#1C1C1E": "#1C1C1E",
    "#EFEFF4": "#EFEFF4",
    "#007AFF": "#007AFF",
    "#8E8E93": "#8E8E93",
    "#34495E": "#34495E",
    "#95A5A6": "#95A5A6",
    "#16A085": "#16A085",
    "#27AE60": "#27AE60",
    "#2980B9": "#2980B9",
    "#8E44AD": "#8E44AD",
    "#F39C12": "#F39C12",
    "#D35400": "#D35400",
    "#C0392B": "#C0392B",
    "#7F8C8D": "#7F8C8D",
}

prompt = "Choose 3 professional colors for a website and return an array with those 3 hex colors."

# Create and write to the file
if (os.path.exists(file_path)):
    with open(file_path, "a") as f:
        for _ in range(50):
            colors = random.sample(list(professional_colors.keys()), 3)
            response = json.dumps(colors)
        f.write(f"{response}\n")
else:
    with open(file_path, "w") as f:
        for _ in range(50):
            colors = random.sample(list(professional_colors.keys()), 3)
            response = json.dumps(colors)
        f.write(f"{response}\n")

print(f"✅ Dataset saved to: {file_path}")