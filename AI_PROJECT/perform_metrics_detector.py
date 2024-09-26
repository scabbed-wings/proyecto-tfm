from datasets.detector_dataset import get_torch_dataloader
from models.detector_functions import inference_test, get_inference_and_metrics
from models.utils import create_PRC
from models.detector_definition import model_defintion

if __name__ == "__main__":

    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional",
                                                                                  dims=(320, 320))
    model = model_defintion()
    weights_path = r"AI_PROJECT\output\model_15.pth"
    # inference_test(weights_path, model, test_data_loader)
    y_true, y_scores = get_inference_and_metrics(weights_path, model, test_data_loader, 3, iou_threshold=0.5)
    create_PRC(y_true, y_scores, 3)
