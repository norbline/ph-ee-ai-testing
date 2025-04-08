import pandas as pd
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Load logs from JSON
with open('synthetic_ph_ee_logs.json', 'r') as file:
    logs = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(logs)

# Display structure
print("Log structure sample:")
print(df.head())

# Preprocessing: Convert timestamp to datetime & extract time features
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute

# Encode categorical features
categorical_features = ['tenant', 'endpoint', 'status']
encoder = OneHotEncoder()
encoded = encoder.fit_transform(df[categorical_features]).toarray()

# Combine with numerical features
features = np.concatenate([
    encoded,
    df[['hour', 'minute']].values
], axis=1)

# Train Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(features)

# Label anomalies: -1 = anomaly, 1 = normal
df['anomaly_label'] = df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')

# Output: Save results with anomaly labels
df[['timestamp', 'tenant', 'endpoint', 'status', 'message', 'anomaly_label']].to_csv('anomaly_detection_report.csv', index=False)

# Summary
print("Anomaly detection complete.")
print(df['anomaly_label'].value_counts())

# Optional: Display a few anomalies
print("\nSample Anomalies:")
print(df[df['anomaly_label'] == 'anomaly'].head())
