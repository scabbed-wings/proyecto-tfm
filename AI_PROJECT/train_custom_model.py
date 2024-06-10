from model.model import ObjectDetection
from model.utils import get_cuda_device
from dataset.dataset import get_torch_dataloader
import torch
from tqdm import tqdm


def setup_stage(batch_size=32, img_shape=[320,320], dataset='data_generator/img'):
    train_dataloader, test_dataloader, num_train, num_test = get_torch_dataloader(batch_size, 
                                                             img_shape[0], 
                                                             img_shape[1],
                                                             dataset)
    return train_dataloader, test_dataloader, num_train, num_test


def train(train_set, test_set, epochs, num_train, LR=0.001):
    device = get_cuda_device()
    print("CUDA_device: ", device)
    model = ObjectDetection(in_channels=1, out_channels_cnn=3, bboxes=4)
    model.to(device)

    classification_loss = torch.nn.CrossEntropyLoss()
    bbox_loss = torch.nn.MSELoss()
    opt = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=0.01)

    train_loss = []
    train_accuracy = []
    test_loss = []
    test_accuracy = []

    for epoch in tqdm(range(epochs)):
        correct = 0
        iter = 0
        iter_loss = 0
        model.train()
        for i, (images, labels, bbox) in enumerate(train_set):
            images = images.to(device)
            labels = labels.to(device)
            bbox = bbox.to(device)

            regressor, classifier = model(images)

            _, predicted = torch.max(classifier, 1) ## To get the labels of predicted 
            predicted_bbox = bbox + regressor ## to get the bbox of the predicted (add the regression offset with the original bbox)

            clf_loss = classification_loss(classifier, labels)
            reg_loss = bbox_loss(predicted_bbox, bbox)
            
            
            total_loss = (clf_loss + reg_loss).clone().detach().requires_grad_(True)

            opt.zero_grad()
            total_loss.backward()
            opt.step()
            
            iter_loss += total_loss.item()
            correct += (predicted == labels).sum().item()
            iter += 1
        
        train_loss.append(iter_loss / iter)
        train_accuracy.append((100 * correct / num_train))
        print(f"Epoch [{epoch + 1} / {epochs}], Training Loss: {train_loss[-1]:.3f}, Training Accuracy: {train_accuracy[-1]:.3f}")


if __name__ == "__main__":
    train_set, test_set, num_train, num_test = setup_stage(batch_size=32, img_shape=[394, 516])
    train(train_set=train_set, test_set=test_set, epochs=10, LR=0.001, num_train=num_train)
