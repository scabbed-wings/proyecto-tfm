from datasets.relational_classificator_dataset import create_classificator_dataset


if __name__ == "__main__":
    annotation_file = "data_generator/relational_images/labels.json"
    images_folder = "data_generator/relational_images/images"
    create_classificator_dataset(annotation_file, images_folder)