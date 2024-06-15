from dataset.dataset import process_data_bboxes
from sklearn.model_selection import train_test_split
from dataset.utils.custom_dataset import CustomBBoxDataset
from torch.utils.data import DataLoader
from dataset.utils.transformations import collate_function
from dataset.dataset import visualize_images


def get_torch_dataloader(dims, dataset_path="data_generator/img", not_background=True):
    print("Processing data")
    df = process_data_bboxes(dataset_path, not_background)
    print("Splitting data")
    train_set, valid_set = train_test_split(df, test_size=0.1,
                                            shuffle=True)
    train_set, test_set = train_test_split(train_set, test_size=0.1, shuffle=True)
    train_set_obj = CustomBBoxDataset(train_set, "train", size=dims)
    valid_set_obj = CustomBBoxDataset(valid_set, "test", size=dims)
    test_set_obj = CustomBBoxDataset(test_set, split="test", size=dims)
    # train_data_loader = DataLoader(train_set_obj, 8, shuffle=True,
    #                                collate_fn=collate_function, pin_memory=True, num_workers=1)
    test_data_loader = DataLoader(test_set_obj, 8, shuffle=True,
                                  collate_fn=collate_function, num_workers=1)
    valid_data_loader = DataLoader(valid_set_obj, 8, shuffle=True,
                                   collate_fn=collate_function, num_workers=1)

    return train_set_obj, valid_data_loader, test_data_loader


if __name__ == "__main__":
    get_torch_dataloader()
