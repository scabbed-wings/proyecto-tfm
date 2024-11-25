from visual_relation_detector.src.relation_metrics import get_relation_metrics
# from deep_learning.models.utils import get_cuda_device
from visual_relation_detector.src.utils import load_model


if __name__ == "__main__":
    dataset = r"data_generator\test"
    detector_weights_path = r"deep_learning\output\model_15.pth"
    classifier_weights_path = r"deep_learning\output\classification_output\experiment_2\best_model_17.pth"
    device = "cuda"  # get_cuda_device()
    dims = (320, 320)
    print("Loading detector model")
    detector_model = load_model(detector_weights_path, device, "detector")
    print("Loading classifier model")
    classifier_model = load_model(classifier_weights_path, device, "classification")
    print("Performing relation metrics")
    precision, recall, f1_score = get_relation_metrics(dataset, detector_model, classifier_model, device,  dims)
    print("Precision: ", precision, "\tRecall: ", recall, "\tF1 Score: ", f1_score)
