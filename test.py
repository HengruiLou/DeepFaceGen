import torch
import argparse
import util
import os
import time
import csv

from torch.utils.tensorboard import SummaryWriter
from torch import nn

import loader
import models
import config
from core.graph3 import HookModule
from util import AverageStorage, ProgressMeter, accuracy, AucStorage, ClassAccuracy


def test(test_loader, model, criterion, num_classes, device):
    loss_meter = AverageStorage('Loss', ':4e')
    acc_meter = AverageStorage('Acc', ':.2%')
    auc_meter = AucStorage('Auc', ':.2%')
    progress = ProgressMeter(total=len(test_loader), step=20, prefix='Testing',
                             meters=[loss_meter, acc_meter, auc_meter])
    model.eval()
    classAccuracy = ClassAccuracy(num_classes)

    for i, samples in enumerate(test_loader):
        inputs, labels = samples
        inputs = inputs.to(device)
        labels = labels.to(torch.float32).to(device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        acc = accuracy(outputs, labels)

        classAccuracy.accuracy(outputs, labels)

        loss_meter.update(loss.item(), inputs.size(0))
        acc_meter.update(acc.item(), labels.size(0))
        auc_meter.update(labels.cpu().tolist(), outputs.cpu().tolist())

        progress.display(i)

    return loss_meter, acc_meter, auc_meter, classAccuracy



def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--model_name', type=str, default='xception')
    parser.add_argument('--ori_dataset', type=str, default='celeb')
    parser.add_argument('--tar_dataset', type=str, default='celeb')
    parser.add_argument('--model_type', type=str, default='ori')
    parser.add_argument('--device', type=str, default='cuda:0')
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    
    # 模型、日志保存路径
    basic_dir = util.get_basic_dir(args.model_name, args.ori_dataset)
    log_dir = os.path.join(basic_dir, 'runs')
    model_path = os.path.join(basic_dir, 'model_' + 'ori' + '.pth')
    static_dir = './tmp.csv'

    # 数据集
    test_loader, data_config = loader.load_data(args.tar_dataset, data_type='test')
    # test_loader, data_config = loader.load_data('dfdc', data_type='test')

    # 模型
    in_channels, num_classes = data_config['in_channels'], data_config['num_classes']

    model = models.load_model(args.model_name, in_channels=in_channels, num_classes=num_classes)
    model = model.to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))


    criterion = nn.BCEWithLogitsLoss()
    criterion_gcn = nn.CrossEntropyLoss()

    writer = SummaryWriter(log_dir)

    # ----------------------------------------
    # each epoch
    # ----------------------------------------
    since = time.time()

    loss, acc, auc, classAccuracy = test(test_loader, model, criterion, num_classes, device)
    
    print('-' * 20 + 'ORI Model Test' + '-' * 20)
    print(loss, acc, auc)
    print(classAccuracy)
    print('TIME CONSUMED', time.time() - since)


    static_dir = '/data/usr/testuser/code/deepfake_detection/tmp.csv'
    prop = ["id", 'acc', 'auc', '0', '1']
    with open(static_dir, mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.stat(static_dir).st_size == 0:
            writer.writerow(prop)  # Write header only if file is empty
        id = f'{args.model_name}_{args.ori_dataset}_{args.tar_dataset}'
        acc0 = format((classAccuracy.sum[0] / classAccuracy.count[0]) * 100, ".2f")
        acc1 = format((classAccuracy.sum[1] / classAccuracy.count[1]) * 100, ".2f")
        acc = format(acc.avg * 100, ".2f")
        auc = format(auc.avg * 100, ".2f")
        writer.writerow([id, acc, auc, acc0, acc1])

if __name__ == '__main__':
    main()