from dataset.dataset import process_data_bboxes
from sklearn.model_selection import train_test_split
from dataset.utils.custom_dataset import CustomBBoxDataset
from torch.utils.data import DataLoader
from dataset.utils.transformations import collate_function
from dataset.dataset import visualize_images

def get_torch_dataloader(dataset_path="data_generator/img"):
    print("Processing data")
    df = process_data_bboxes(dataset_path)
    print("Splitting data")
    train_set, test_set = train_test_split(df, test_size=0.1,
                                           shuffle=True)
    train_set_obj = CustomBBoxDataset(train_set, "train")
    train_data_loader = DataLoader(train_set_obj, 8, shuffle=True, 
                                   collate_fn=collate_function, pin_memory=True, num_workers=2)
    for images, boxes, labels in train_data_loader:
        visualize_images(images[0], boxes[0], labels[0])


if __name__ == "__main__":
    get_torch_dataloader()