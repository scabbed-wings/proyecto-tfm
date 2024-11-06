class MetricCalculator:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0

    def increment_tp(self, value: int = 1):
        self.tp += value

    def increment_fp(self, value: int = 1):
        self.fp += value

    def increment_fn(self, value: int = 1):
        self.fn += value

    def calculate_metrics(self):
        precision = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0
        recall = self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return precision, recall, f1_score
