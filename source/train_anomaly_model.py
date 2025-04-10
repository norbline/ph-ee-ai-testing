import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
import joblib
from sklearn.metrics import classification_report, confusion_matrix

class AnomalyDetector:
    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.encoder = OneHotEncoder()

    def load_logs(self, file_path):
        return pd.read_json(file_path)

    def preprocess(self, df):
        df['@timestamp'] = pd.to_datetime(df['@timestamp'])
        df['hour'] = df['@timestamp'].dt.hour
        df['minute'] = df['@timestamp'].dt.minute

        cat_features = ['Platform-TenantId', 'url', 'status']
        encoded = self.encoder.fit_transform(df[cat_features]).toarray()

        numerical = df[['hour', 'minute']].values
        features = np.concatenate([encoded, numerical], axis=1)

        return df, features

    def train(self, features):
        self.model.fit(features)

    def predict(self, df, features):
        preds = self.model.fit_predict(features)
        df['anomaly'] = preds
        df['anomaly_label'] = df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')
        # Inject synthetic ground truth for evaluation (5% random anomalies)
        np.random.seed(42)
        df['anomaly_ground_truth'] = np.where(np.random.rand(len(df)) < 0.05, 'anomaly', 'normal')

        # Evaluate model performance

        print("\n=== Classification Report ===")
        print(classification_report(df['anomaly_ground_truth'], df['anomaly_label']))

        # Save with ground truth for notebook use
        df[['@timestamp', 'Platform-TenantId', 'url', 'status', 'anomaly_label', 'anomaly_ground_truth']] \
            .to_csv('anomaly_detection_report.csv', index=False)

        return df

    def save_results(self, df, output_path):
        df[['@timestamp', 'Platform-TenantId', 'url', 'status', 'anomaly_label']].to_csv(output_path, index=False)

    def save_model(self, model_path):
        joblib.dump(self.model, model_path)

    def load_model(self, model_path):
        self.model = joblib.load(model_path)
