from model.existent_model import unitary_inference
from model.model_definition import model_defintion
from relator.read_bboxes import read_boxes
from torch import tensor
from torchvision.transforms.functional import pil_to_tensor
from PIL import Image
from dataset.dataset import visualize_images


if __name__ == "__main__":

    model = model_defintion()
    weights_path = "AI_PROJECT\output\model_25.pth"
    test_image = r"data_generator\test\img398.png"
    dims = (320, 320)
    image = Image.open(test_image)
    original_size_tensor = tensor([image.width, image.height, image.width, image.height])
    resized_tensor = tensor([dims[0], dims[1], dims[0], dims[1]])
    pred_boxes, pred_labels = unitary_inference(model, weights_path, image, dims)
    prop_pred_boxes = pred_boxes / resized_tensor
    original_size_pred_boxes = prop_pred_boxes * original_size_tensor
    image = image.convert('L')
    image_tensor = pil_to_tensor(image)
    visualize_images(image_tensor, original_size_pred_boxes, pred_labels, inference=True)
    read_boxes(image, original_size_pred_boxes)