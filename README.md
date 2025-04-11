#  AI-Driven Architectural Testing for [MIFOS Payment Hub EE](https://payments.mifos.org/)

This project is a Proof of Concept (PoC) demonstrating how AI techniques can be used to test, monitor, and enhance the resilience and reliability of the [MIFOS Payment Hub EE](https://payments.mifos.org/) architecture.

##  Objectives

- Detect anomalies in transaction logs
- Simulate traffic and failure conditions
- Leverage AI models to assess stability
- Integrate OpenTelemetry, Elasticsearch, and Kibana for observability

##  Getting Started

1. Clone this repo
2. Create a virtual environment and install requirements:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Run model training manually:

```bash
python3 run_model.py
```

4. Launch the notebook manually (optional):

```bash
jupyter notebook notebooks/model_experimentation.ipynb
```

##  View the AI Anomaly Detection Report

You can preview the results of the AI-driven anomaly detection directly without running the code:

 [Click to View Report](https://norbline.github.io/ph-ee-ai-testing/report.html)

If you're viewing this from GitHub, just click the link above to see the rendered HTML report.

---




