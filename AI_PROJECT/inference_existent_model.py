from dataset.load_dataset import get_torch_dataloader
from model.existent_model import model_test_metrics
from model.model_definition import model_defintion

if __name__ == "__main__":

    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional",
                                                                                  dims=(320, 320))
    model = model_defintion()
    model_test_metrics("AI_PROJECT\output\model_20.pth", model, test_data_loader)
