import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

#load the dataset
data = pd.read_csv("data/emails.csv")

#check which columns python actually loaded
print("File columns:", data.columns.tolist())
print("First 3 rows:")

#remove missing entries
print(data.head(3))

#remove missing entries
data = data.dropna(subset=["text", "label"])
data["text"] = data["text"].astype(str)
data["label"] = data["label"].astype(int)

#seperate email text and labels
x = data["text"]
y = data["label"]

#split into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size = 0.2, random_state = 42, stratify = y
)

#build machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words = "english",
        max_features = 5000,
        ngram_range = (1,2)
    )),
    ("classifier", LogisticRegression(
        max_iter = 1000,
        class_weight = "balanced"

    ))
])

#train the model
model.fit(x_train, y_train)

#test the performance
predictions = model.predict(x_test)

print(classification_report(
    y_test, predictions, target_names = ["Legitimate", "Phishing"]
))

#save trained model
joblib.dump(model, "phishing_model.pkl")
print("Model trained and saved successfully!")

