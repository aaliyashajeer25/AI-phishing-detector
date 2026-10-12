import pandas as pd

# Load original dataset
data = pd.read_csv("data/CEAS_08.csv")

# Show original labels
print("Original labels:")
print(data["label"].value_counts(dropna=False))

# Combine subject and body into text
data["text"] = (
    data["subject"].fillna("").astype(str)
    + " "
    + data["body"].fillna("").astype(str)
)

# Keep only text and label columns
data = data[["text", "label"]].copy()

# Remove empty emails and duplicates
data = data[data["text"].str.strip() != ""]
data = data.dropna(subset=["label"])
data = data.drop_duplicates(subset=["text"])

print("\nCleaned dataset:")
print(data.head())

print("\nLabels:")
print(data["label"].value_counts(dropna=False))

data["label"] = data["label"].astype(int)

data.to_csv("data/emails.csv", index=False)

print("Dataset saved successfully!")

