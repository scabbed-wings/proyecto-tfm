from models.detector_definition import model_defintion
from datasets.detector_dataset import get_torch_dataloader
from models.detector_functions import train_model


if __name__ == "__main__":
    model = model_defintion()
    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional",
                                                                                  dims=(320, 320))

    train_model(train_data_loader, valid_data_loader, model, experiment_name="experiment2", epochs=25)
