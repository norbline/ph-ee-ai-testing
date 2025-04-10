from train_anomaly_model import AnomalyDetector

detector = AnomalyDetector()

# 👇 Change to your synthetic log file path
df = detector.load_logs('/home/norbline/AI-Driven_ph_testing/data/synthetic_ph_ee_logs.json')
df, features = detector.preprocess(df)
detector.train(features)
df = detector.predict(df, features)
detector.save_results(df, 'anomaly_results.csv')
detector.save_model('isolation_forest_model.pkl')
