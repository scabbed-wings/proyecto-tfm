from dataset.load_dataset import get_torch_dataloader
from model.existent_model import inference_test, get_inference_and_metrics
from model.utils import create_PRC
from model.model_definition import model_defintion

if __name__ == "__main__":

    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional",
                                                                                  dims=(320, 320))
    model = model_defintion()
    weights_path = "AI_PROJECT\output\model_25.pth"
    # inference_test(weights_path, model, test_data_loader)
    y_true, y_scores = get_inference_and_metrics(weights_path, model, test_data_loader, 3, iou_threshold=0.5)
    create_PRC(y_true, y_scores, 3)
