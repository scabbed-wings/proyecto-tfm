from torchview import draw_graph
from models.detector_definition import model_defintion
from models.relational_classification_model import PairedImageClassifier
if __name__ == "__main__":
    classifier = PairedImageClassifier()
    model_graph = draw_graph(classifier, input_size=[(128, 1, 320, 320), (128, 1, 320, 320)], device='meta', save_graph=True, show_shapes=False)
    detector = model_defintion()
    detector_graph = draw_graph(detector.backbone, input_size=[(128, 1, 320, 320), (128, 1, 320, 320)], device='meta', save_graph=True, show_shapes=False)