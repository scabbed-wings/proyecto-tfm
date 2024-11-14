from datasets.relational_classificator_dataset import create_classificator_dataset
from models.relational_classification_model import PairedImageClassifier
from models.relational_classification_functions import train_model


if __name__ == "__main__":
    train_annotation_file = "data_generator/train_relational_images/labels.json"
    train_images_folder = "data_generator/train_relational_images/images"
    test_annotation_file = "data_generator/test_relational_images/labels.json"
    test_images_folder = "data_generator/test_relational_images/images"
    model = PairedImageClassifier()
    train_dataloader, validation_dataloader, test_dataloader = create_classificator_dataset(train_annotation_file,
                                                                                            train_images_folder,
                                                                                            test_annotation_file,
                                                                                            test_images_folder)
    train_model(train_dataloader, validation_dataloader, model, "experiment_1")
