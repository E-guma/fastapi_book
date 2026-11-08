# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Libraries imported successfully!")

# %%
# Create a Sample DataFrame
data = {
    "Category": ["A", "B", "C", "D", "E"],
    "Values": [23, 45, 56, 78, 33],
    "Score": [85, 90, 78, 92, 88],
}

df = pd.DataFrame(data)
print(df.describe())
df

# %%
# Plotting Data (Matplotlib)
plt.figure(figsize=(8, 4))
plt.plot(df["Category"], df["Values"], marker="o", color="b", label="Values")
plt.bar(df["Category"], df["Score"], alpha=0.3, color="r", label="Score (Alpha)")
plt.title("Helium In-Editor Plotting Test")
plt.xlabel("Categories")
plt.ylabel("Metrics")
plt.legend()
plt.grid(True)
plt.show()

# %%
# Quick Math Loop
total = sum(df["Values"])
print(f"Total sum of values: {total}")
