from torch.utils.data import DataLoader
from torchvision import transforms
from loader.datasets.csv_dataset import Dataset_Csv
from torch.utils.data import WeightedRandomSampler
from random import shuffle
import config
import csv
import torch
import random

def base_data(csv_file, train_label, train_list):
    rows = []
     # 打开 CSV 文件并将行存储到列表中
    with open(csv_file, 'r') as frame_reader:
        csv_reader = csv.reader(frame_reader)
        rows = list(csv_reader)
    random.shuffle(rows)
    for row in rows:
        path = row[0]
        # path = path.replace('AIGC_dataset', 'AIGC_dataset_crop')
        label = int(row[1])
        train_label.append(label)
        train_list.append(path)


def validation_data(csv_file, test_label, test_list):
    rows = []
     # 打开 CSV 文件并将行存储到列表中
    with open(csv_file, 'r') as frame_reader:
        csv_reader = csv.reader(frame_reader)
        rows = list(csv_reader)
    random.shuffle(rows)
    for row in rows:
        path = row[0]
        # path = path.replace('AIGC_dataset', 'AIGC_dataset_crop')
        label = int(row[1])
        test_label.append(label)
        test_list.append(path)


def make_weights_for_balanced_classes(train_dataset):
    targets = []
    
    targets = torch.tensor(train_dataset)

    class_sample_count = torch.tensor(
        [(targets == t).sum() for t in torch.unique(targets, sorted=True)])
    weight = 1. / class_sample_count.float()
    samples_weight = torch.tensor([weight[t] for t in targets])
    return samples_weight


def load_images(data_type=None, data_name=None):
    assert data_type is None or data_type in ['train', 'test']

    data_config = config.get_data_config(data_name)
    train_csv = data_config['train_csv']
    test_csv = data_config['test_csv']
    batch_size = data_config['batch_size']
    img_size = data_config['img_size']

    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)), # 299 * 299
        transforms.ToTensor(),
        transforms.Normalize([0.5] * 3, [0.5] * 3)
    ])

    params = {'shuffle': False, 'num_workers': 4, 'pin_memory': True}

    if data_type == 'train':
        train_list = []
        train_label = []
        base_data(train_csv, train_label, train_list)

        ziplist = list(zip(train_list, train_label))
        shuffle(ziplist)
        train_list[:], train_label[:] = zip(*ziplist)

        weights = make_weights_for_balanced_classes(train_label)
        data_sampler = WeightedRandomSampler(weights, len(train_label), replacement=True)
        
        data_set = Dataset_Csv(train_list, train_label, transform=transform)
        data_loader = DataLoader(data_set, sampler=data_sampler, batch_size=batch_size, **params)
        
    else:
        test_list = []
        test_label = []
        validation_data(test_csv, test_label, test_list)

        data_set = Dataset_Csv(test_list, test_label, transform=transform)
        data_loader = DataLoader(data_set, batch_size=batch_size, **params)


    return data_loader, data_config
