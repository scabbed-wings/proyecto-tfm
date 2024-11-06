from visual_relation_detector.src.relation_metrics import get_relation_metrics
from visual_relation_detector.src.utils import load_model


def main():
    dataset = r"data_generator\test"
    detector_weights_path = r"deep_learning\output\model_15.pth"
    device = "cuda"  # get_cuda_device()
    dims = (320, 320)
    print("Loading detector model")
    detector_model = load_model(detector_weights_path, device, "detector")
    print("Performing relation metrics")
    precision, recall, f1_score = get_relation_metrics(dataset, detector_model, None, device,  dims, method="contours")
    print("Precision: ", precision, "\tRecall: ", recall, "\tF1 Score: ", f1_score)


if __name__ == "__main__":
    main()
