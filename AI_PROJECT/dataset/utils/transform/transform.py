import torchvision.transforms.functional as FT
import random
import dataset.utils.transform.transform_operations as TO


def transform(images, bboxes, labels, split, dims=(300, 300)):
    mean = (0.9844960020963516,)  
    std = (0.11468420904814396,)
    new_image = images
    new_bboxes = bboxes
    new_labels = labels
    if split == 'TRAIN':
        # A series of photometric distortions in random order, each with 50% chance of occurrence, as in Caffe repo

        # Convert PIL image to Torch tensor
        new_image = FT.to_tensor(new_image)

        # Expand image (zoom out) with a 50% chance - helpful for training detection of small objects
        # Fill surrounding space with the mean of ImageNet data that our base VGG was trained on

        # if random.random() < 0.5:
        #     new_image, new_bboxes = expand(new_image, bboxes, filler=mean)

        # Randomly crop image (zoom in)
        new_image, new_bboxes, new_labels = TO.random_crop(new_image, new_bboxes, new_labels)

        # Convert Torch tensor to PIL image
        new_image = FT.to_pil_image(new_image)

        # Flip image with a 50% chance
        if random.random() < 0.5:
            new_image, new_bboxes = TO.flip(new_image, new_bboxes)

    # Resize image to (300, 300) - this also converts absolute boundary coordinates to their fractional form
    new_image, new_bboxes = TO.resize(new_image, new_bboxes, dims)

    # Convert PIL image to Torch tensor
    new_image = FT.to_tensor(new_image)

    # Normalize by mean and standard deviation of ImageNet data that our base VGG was trained on
    # new_image = FT.normalize(new_image, mean=mean, std=std)

    return new_image, new_bboxes, new_labels