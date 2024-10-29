from relator.relation_metrics import get_relation_metrics
from relator.utils import load_model


if __name__ == "__main__":
    dataset = r"data_generator\test"
    detector_weights_path = r"AI_PROJECT\output\model_15.pth"
    classifier_weights_path = r"AI_PROJECT\output\classification_output\best_model_13.pth"
    device = "cuda"  # get_cuda_device()
    dims = (320, 320)
    print("Loading detector model")
    detector_model = load_model(detector_weights_path, device, "detector")
    print("Performing relation metrics")
    precision, recall, f1_score = get_relation_metrics(dataset, detector_model, None, device,  dims, method="contours")
    print("Precision: ", recall, "\tRecall: ", recall, "\tF1 Score: ", f1_score)
