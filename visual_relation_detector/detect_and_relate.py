from deep_learning.models.detector_functions import unitary_inference, resize_bounding_boxes
from deep_learning.models.detector_definition import model_defintion
from deep_learning.models.relational_classification_model import PairedImageClassifier
from deep_learning.models.relational_classification_functions import unitary_inference_classificator
from visual_relation_detector.src.read_bboxes import read_boxes
from visual_relation_detector.src.utils import max_min_coordinates
import torch
from torchvision.transforms.functional import pil_to_tensor
from PIL import Image
from deep_learning.datasets.dataset import visualize_images


def crop_detections_and_relate(image, pred_boxes, classifier_weights_path, classifier_thresh=0.9474):
    model = PairedImageClassifier()
    model.load_state_dict(torch.load(classifier_weights_path))
    for index_source, box_source in enumerate(pred_boxes):
        for index_target, box_target in enumerate(pred_boxes):
            if index_target != index_source:
                xmin, ymin, xmax, ymax = max_min_coordinates(box_source, box_target)
                crop_image = image.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
                prediction = unitary_inference_classificator(model, image, crop_image)
                if prediction >= classifier_thresh:
                    print("ELEMENT SOURCE: ", index_source, " IS RELATED TO ELEMENT TARGET: ", index_target,
                          " SCORE: ", prediction[0])


if __name__ == "__main__":
    model_detector = model_defintion()
    detector_weights_path = r"deep_learning\output\model_15.pth"
    classifier_weights_path = r"deep_learning\output\classification_output\experiment_2\best_model_17.pth"
    test_image = r"data_generator\test\img214.png"
    dims = (320, 320)
    image = Image.open(test_image)
    pred_boxes, pred_labels = unitary_inference(model_detector, detector_weights_path, image, dims)
    original_size_pred_boxes = resize_bounding_boxes(image, pred_boxes, dims)
    image = image.convert('L')
    crop_detections_and_relate(image, original_size_pred_boxes, classifier_weights_path)
    # with open('pred_boxes.pkl', 'wb') as file_boxes:
    #     pickle.dump(original_size_pred_boxes, file_boxes)
    # with open('pred_labels.pkl', 'wb') as file_labels:
    #     pickle.dump(pred_labels, file_labels)
    image_tensor = pil_to_tensor(image)
#
    visualize_images(image_tensor, original_size_pred_boxes, pred_labels, inference=True, box_index=True)

    read_boxes(image, original_size_pred_boxes)
