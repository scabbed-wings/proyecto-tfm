from models.detector_functions import unitary_inference
from models.detector_definition import model_defintion
from models.relational_classification_model import PairedImageClassifier
from models.relational_classification_functions import unitary_inference_classificator
from relator.read_bboxes import read_box
from relator.follow_line_algorithm import max_min_coordinates
import torch
from torchvision.transforms.functional import pil_to_tensor
from PIL import Image
from datasets.dataset import visualize_images
import pickle


def crop_detections_and_relate(image, pred_boxes, classifier_weights_path, classifier_thresh=0.889):
    model = PairedImageClassifier()
    model.load_state_dict(torch.load(classifier_weights_path))
    for index_source, box_source in enumerate(pred_boxes):
        for index_target, box_target in enumerate(pred_boxes):
            if index_target != index_source:
                xmin, ymin, xmax, ymax = max_min_coordinates(box_source, box_target)
                crop_image = image.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
                prediction = unitary_inference_classificator(model, image, crop_image)
                if prediction >= classifier_thresh:
                    print("ELEMENT SOURCE: ", index_source, " IS RELATED TO ELEMENT TARGET: ", index_target)
                

def resize_bounding_boxes(bounding_boxes, dims):
    original_size_tensor = torch.tensor([image.width, image.height, image.width, image.height])
    resized_tensor = torch.tensor([dims[0], dims[1], dims[0], dims[1]])
    prop_pred_boxes = bounding_boxes / resized_tensor
    original_size_pred_boxes = prop_pred_boxes * original_size_tensor
    return original_size_pred_boxes


if __name__ == "__main__":
    model_detector = model_defintion()
    detector_weights_path = "AI_PROJECT\output\model_25.pth"
    classifier_weights_path = r"AI_PROJECT\output\classification_output\best_model_13.pth"
    test_image = r"AI_PROJECT\descarga (1).png"
    dims = (320, 320)
    image = Image.open(test_image)
    pred_boxes, pred_labels = unitary_inference(model_detector, detector_weights_path, image, dims)
    original_size_pred_boxes = resize_bounding_boxes(pred_boxes, dims)
    image = image.convert('L')
    crop_detections_and_relate(image, original_size_pred_boxes, classifier_weights_path)
    # with open('pred_boxes.pkl', 'wb') as file_boxes:
    #     pickle.dump(original_size_pred_boxes, file_boxes)
    # 
    # with open('pred_labels.pkl', 'wb') as file_labels:
    #     pickle.dump(pred_labels, file_labels)
    image_tensor = pil_to_tensor(image)
#
    visualize_images(image_tensor, original_size_pred_boxes, pred_labels, inference=True, box_index=True)

    # read_boxes(image, original_size_pred_boxes)