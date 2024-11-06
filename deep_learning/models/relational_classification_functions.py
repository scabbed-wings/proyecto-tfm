import torch
from torchmetrics.classification import BinaryAccuracy, BinaryPrecision, BinaryRecall, BinaryROC, BinaryF1Score
import matplotlib.pyplot as plt
import os
from deep_learning.datasets.relational_classificator_dataset import transform_image_test


def checkpoint(model, filedir, epoch, best):
    filename = f"best_model_{epoch}.pth" if best else f"model_{epoch}.pth"
    filename = os.path.join(filedir, filename)
    torch.save(model.state_dict(), filename)


def evaluate_epoch(model, validation_dataloader, device, roc_curve: bool = False, roc_thresholds: int = 20):
    model.eval()
    accuracy = BinaryAccuracy().to(device)
    precision = BinaryPrecision().to(device)
    recall = BinaryRecall().to(device)
    f1_score = BinaryF1Score().to(device)
    broc = BinaryROC(thresholds=roc_thresholds).to(device) if roc_curve else None
    with torch.no_grad():
        for images_source, images_crop, labels in validation_dataloader:
            images_source_tensor = images_source.to(device)
            images_crop_tensor = images_crop.to(device)
            labels_tensor = labels.to(device)
            outputs = model(images_source_tensor, images_crop_tensor)
            predictions = torch.sigmoid(outputs)
            predictions = predictions.squeeze()

            # Calcular métricas
            accuracy(predictions, labels_tensor)
            precision(predictions, labels_tensor)
            recall(predictions, labels_tensor)
            f1_score(predictions, labels_tensor)
            if roc_curve:
                target = labels_tensor.type(torch.int8)
                broc(predictions, target)

    acc = accuracy.compute()
    prec = precision.compute()
    rec = recall.compute()
    f1 = f1_score.compute()
    if roc_curve:
        fig_, ax_ = broc.plot(score=True)
        print(broc.compute())
        plt.show()

    return acc, prec, rec, f1


def train_model(train_data_loader, valid_data_loader,
                model,
                save_checkpoint="AI_PROJECT/output/classification_output"):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Training on: ", device)
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    # optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, weight_decay=0.01)
    optimizer = torch.optim.Adam(params, lr=0.0001)
    loss_function = torch.nn.BCEWithLogitsLoss()
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)
    num_epochs = 30
    best_f1 = 0

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for train_images_source, train_images_crop, train_labels in train_data_loader:
            images_source_tensor = train_images_source.to(device)
            images_crop_tensor = train_images_crop.to(device)
            labels_tensor = train_labels.to(device)
            outputs = model(images_source_tensor, images_crop_tensor)
            loss = loss_function(outputs.squeeze(), labels_tensor.float())
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        val_acc, val_prec, val_rec, val_f1 = evaluate_epoch(model, valid_data_loader, device)
        if lr_scheduler is not None:
            lr_scheduler.step(loss)
        print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_data_loader)}')
        print(f'Validation: Accuracy {val_acc}, Precision {val_prec}, Recall {val_rec}, F1 {val_f1}')

        if (epoch + 1) % 2 == 0:
            checkpoint(model, save_checkpoint, epoch=epoch+1, best=False)
        elif val_f1 > best_f1:
            best_f1 = val_f1
            checkpoint(model, save_checkpoint, epoch=epoch+1, best=True)


def test_model_metrics(weights_file, model, test_dataloader):
    model.load_state_dict(torch.load(weights_file))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    test_accuracy, test_precision, test_recall, test_f1 = evaluate_epoch(model, test_dataloader,
                                                                         device, roc_curve=True)
    print(f'Validation: Accuracy {test_accuracy}, Precision {test_precision}, Recall {test_recall}, F1 Score {test_f1}')


def unitary_inference_classificator(model, image_source, image_crop, dims=(320, 320)):
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    transform = transform_image_test(dims)
    # Preparing image source tensor
    image_source_tensor = transform(image_source)
    image_source_tensor = image_source_tensor.unsqueeze(0)
    image_source_tensor = image_source_tensor.to(device)
    # Preparing image crop tensor
    image_crop_tensor = transform(image_crop)
    image_crop_tensor = image_crop_tensor.unsqueeze(0)
    image_crop_tensor = image_crop_tensor.to(device)

    output = model(image_source_tensor, image_crop_tensor)
    predictions = torch.sigmoid(output)
    return predictions
