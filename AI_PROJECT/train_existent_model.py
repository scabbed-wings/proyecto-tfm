from model.model_definition import model_defintion
from dataset.load_dataset import get_torch_dataloader
from model.existent_model import train_model, inference_test


if __name__ == "__main__":
    model = model_defintion()
    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional",
                                                                                  dims=(320, 320))
    
    train_model(train_data_loader, valid_data_loader, model)
    # inference_test("AI_PROJECT\output\model_20.pth", model, test_data_loader)
