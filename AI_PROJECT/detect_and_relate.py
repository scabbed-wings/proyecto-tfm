from model.existent_model import unitary_inference
from model.model_definition import model_defintion

if __name__ == "__main__":

    model = model_defintion()
    weights_path = "AI_PROJECT\output\model_25.pth"
    test_image = r"data_generator\test\img7.png"
    unitary_inference(model, weights_path, test_image)