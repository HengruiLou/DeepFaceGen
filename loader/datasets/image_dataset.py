import os
import PIL.Image as Image
from torch.utils.data import Dataset


def _img_loader(path, mode='RGB'):
    assert mode in ['RGB', 'L']
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert(mode)


def _find_classes(root):
    class_names = [d.name for d in os.scandir(root) if d.is_dir()]
    class_names.sort()
    classes_indices = {class_names[i]: i for i in range(len(class_names))}
    # print(classes_indices)
    return class_names, classes_indices  # 'class_name':index


def _make_dataset(image_dir):
    samples = []  # image_path, class_idx

    class_names, class_indices = _find_classes(image_dir)

    for class_name in sorted(class_names):
        class_idx = class_indices[class_name]
        target_dir = os.path.join(image_dir, class_name)

        if not os.path.isdir(target_dir):
            continue

        for root, _, files in sorted(os.walk(target_dir)):
            for file in sorted(files):
                image_path = os.path.join(root, file)
                item = image_path, class_idx
                samples.append(item)
    return samples


class ImageDataset(Dataset):
    def __init__(self, image_dir, mode='RGB', transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.samples = _make_dataset(self.image_dir)
        self.targets = [s[1] for s in self.samples]
        self.mode = mode

    def __getitem__(self, index):
        image_path, target = self.samples[index]
        image = _img_loader(image_path, mode=self.mode)
        name = os.path.split(image_path)[1]

        if self.transform is not None:
            image = self.transform(image)

        return image, target, name

    def __len__(self):
        return len(self.samples)
