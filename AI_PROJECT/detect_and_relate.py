from models.detector_functions import unitary_inference
from models.detector_definition import model_defintion
from relator.read_bboxes import read_box
from torch import tensor
from torchvision.transforms.functional import pil_to_tensor
from PIL import Image
from datasets.dataset import visualize_images
import pickle


def resize_bounding_boxes(bounding_boxes, dims):
    original_size_tensor = tensor([image.width, image.height, image.width, image.height])
    resized_tensor = tensor([dims[0], dims[1], dims[0], dims[1]])
    prop_pred_boxes = bounding_boxes / resized_tensor
    original_size_pred_boxes = prop_pred_boxes * original_size_tensor
    return original_size_pred_boxes


if __name__ == "__main__":
    model = model_defintion()
    weights_path = "AI_PROJECT\output\model_25.pth"
    test_image = r"data_generator\test\img362.png"
    dims = (320, 320)
    image = Image.open(test_image)
    pred_boxes, pred_labels = unitary_inference(model, weights_path, image, dims)
    original_size_pred_boxes = resize_bounding_boxes(pred_boxes, dims)
    image = image.convert('L')
    
    with open('pred_boxes.pkl', 'wb') as file_boxes:
        pickle.dump(original_size_pred_boxes, file_boxes)
    
    with open('pred_labels.pkl', 'wb') as file_labels:
        pickle.dump(pred_labels, file_labels)

    image_tensor = pil_to_tensor(image)
    visualize_images(image_tensor, original_size_pred_boxes, pred_labels, inference=True, box_index=True)
    # read_boxes(image, original_size_pred_boxes)