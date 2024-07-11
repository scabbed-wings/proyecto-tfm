from glob import glob
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
from utils.generate_relational_image import crop_relational_image

if __name__ == "__main__":
    path = "data_generator/prueba"
    images_list = glob(path + "/*.png")
    for image_name in images_list:
        image_path = Path(image_name)
        csv_path = f"{image_path.parent}/{image_path.stem}.csv"
        image = Image.open(image_path).convert('L')
        image = np.array(image)
        df = pd.read_csv(csv_path, sep=";")
        crop_relational_image(image, df)