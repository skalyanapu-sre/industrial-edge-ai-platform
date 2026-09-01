from prometheus_client import Counter, Histogram

INFERENCE_REQUESTS = Counter(
    "edgeai_inference_requests_total",
    "Total number of inference requests.",
)


INFERENCE_PREDICTIONS = Counter(
    "edgeai_predictions_total",
    "Predictions grouped by severity.",
    ["severity"],
)


INFERENCE_DURATION = Histogram(
    "edgeai_inference_duration_seconds",
    "Time spent performing inference.",
)
