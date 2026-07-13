from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

# Load the dataset
data = pd.read_csv("dataset/spam.csv", encoding="latin-1")

# Display first 5 rows
print("First 5 Rows:")
print(data.head())

# Display column names
print("\nColumn Names:")
print(data.columns)

# Display dataset information
print("\nDataset Information:")
print(data.info())

# Remove unnecessary columns
data = data[['v1', 'v2']]

# Rename columns
data.columns = ['label', 'message']

# Check first 5 rows after cleaning
print("\nCleaned Dataset:")
print(data.head())

# Check missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Convert labels into numbers
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

print("\nEncoded Dataset:")
print(data.head())

# Separate input and output
X = data['message']
y = data['label']

print("\nTotal Messages:", len(X))
print("Total Labels:", len(y))

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data:", len(X_train))
print("Testing Data:", len(X_test))

# Convert text into numerical features
vectorizer = CountVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)
# Create the model
model = MultinomialNB()

# Train the model
model.fit(X_train, y_train)
# Predict on test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
# Save the trained model
joblib.dump(model, "models/spam_model.pkl")

# Save the CountVectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel and Vectorizer saved successfully!")