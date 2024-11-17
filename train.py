import torch
import argparse
import util
import os
import time
import copy

from torch.utils.tensorboard import SummaryWriter
from torch import nn
from torch import optim
from tqdm import tqdm

import loader
import models
import config
from util import AverageStorage, ProgressMeter, AucStorage, ClassAccuracy,  accuracy


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

def train(train_loader, model, criterion, optimizer, device):
    loss_meter = AverageStorage('Loss', ':.4e')
    acc_meter = AverageStorage('Acc', ':.2%')
    auc_meter = AucStorage('Auc', ':.2%')
    progress = ProgressMeter(total=len(train_loader), step=20, prefix='Training',
                             meters=[loss_meter, acc_meter, auc_meter])

    model.train()

    for i, samples in enumerate(train_loader):

        inputs, labels = samples
        inputs = inputs.to(device)
        labels = labels.to(torch.float32).to(device)

        outputs = model(inputs)

        loss = criterion(outputs, labels)
        acc = accuracy(outputs, labels)

        loss_meter.update(loss.item(), inputs.size(0))
        acc_meter.update(acc.item(), inputs.size(0))
        auc_meter.update(labels.cpu().tolist(), outputs.cpu().tolist())

        optimizer.zero_grad()  # 1
        loss.backward()  # 2
        optimizer.step()  # 3
        # scheduler.step()

        progress.display(i)

    return loss_meter, acc_meter, auc_meter

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--model_name', type=str, default='squeezenet')
    parser.add_argument('--dataset_name', type=str, default='celeb')
    parser.add_argument('--device', type=str, default='cuda:0')
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    
    # 模型、日志保存路径
    basic_dir = util.get_basic_dir(args.model_name, args.dataset_name, 'pretrained')
    log_dir = os.path.join(basic_dir, 'runs')
    model_path = os.path.join(basic_dir, 'model_ori.pth')

    # 数据集
    train_loader, data_config = loader.load_data(args.dataset_name, data_type='train')
    test_loader, _ = loader.load_data(args.dataset_name, data_type='test')

    # 模型
    in_channels, num_classes = data_config['in_channels'], data_config['num_classes']
    model = models.load_model(args.model_name, in_channels=in_channels, num_classes=num_classes)
    # model = models.load_model(args.model_name)
    model = model.to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(params=model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    scheduler = optim.lr_scheduler.StepLR(optimizer=optimizer, step_size=config.step_size, gamma=config.gamma)
    # optimizer = optim.SGD(params=model.parameters(), lr=config.lr, momentum=config.momentum, weight_decay=config.weight_decay)
    # scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer=optimizer, T_max=config.num_epochs)

    writer = SummaryWriter(log_dir)


    # ----------------------------------------
    # each epoch
    # ----------------------------------------
    since = time.time()
    best_acc = None
    best_epoch = None
    best_auc = None

    for epoch in tqdm(range(config.num_epochs)):
        loss, acc, auc = train(train_loader, model, criterion, optimizer, device)
        writer.add_scalar(tag='training loss', scalar_value=loss.avg, global_step=epoch)
        writer.add_scalar(tag='training acc1', scalar_value=acc.avg, global_step=epoch)
        writer.add_scalar(tag='training auc', scalar_value=auc.avg, global_step=epoch)
        loss, acc, auc, classAccuracy = test(test_loader, model, criterion, num_classes, device)
        writer.add_scalar(tag='test loss', scalar_value=loss.avg, global_step=epoch)
        writer.add_scalar(tag='test acc', scalar_value=acc.avg, global_step=epoch)
        writer.add_scalar(tag='test auc', scalar_value=auc.avg, global_step=epoch)

        # ----------------------------------------
        # save best model
        # ----------------------------------------
        if best_auc is None or best_auc < auc.avg:
            best_auc = auc.avg
            best_epoch = epoch
            torch.save(model.state_dict(), model_path)
            best_classAcc = copy.deepcopy(classAccuracy)

        scheduler.step()

    print('COMPLETE !!!')
    print('BEST AUC', best_auc)
    print('BEST EPOCH', best_epoch)
    print('TIME CONSUMED', time.time() - since)
    print(best_classAcc)


if __name__ == '__main__':
    main()