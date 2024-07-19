from datasets.relational_classificator_dataset import create_classificator_dataset
from models.relational_classification_model import PairedImageClassifier
from models.relational_classification_functions import test_model_metrics


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
    weights = r"AI_PROJECT\output\classification_output\best_model_13.pth"
    test_model_metrics(weights, model, test_dataloader)