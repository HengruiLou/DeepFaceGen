import torch
import config
import os
import numpy as np
from sklearn.metrics import roc_auc_score

def get_basic_dir(model_name, dataset_name, phase):
    model_dataset = model_name + '_' + dataset_name
    output_dir = os.path.join(config.output_dir, model_dataset)
    
    basic_dir = os.path.join(output_dir, phase)
    if not os.path.exists(basic_dir):
        os.makedirs(basic_dir)
    
    return basic_dir

'''
计算当前epoch的acc、loss
'''
class AverageStorage(object):
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self._reset()

    def _reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name}[AVG:{avg' + self.fmt + '}]'
        return fmtstr.format(**self.__dict__)

'''
计算当前epoch的auc
'''  
class AucStorage(object):
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self._reset()

    def _reset(self):
        self.y_true = []
        self.y_pred = []
        self.avg = 0

    def update(self, y_true, y_pred):
        self.y_true += y_true
        self.y_pred += y_pred
        try: # 如果存在一个类别没有数据就会报错
            self.avg = roc_auc_score(self.y_true, self.y_pred)
        except ValueError:
            self.avg = -1

    def __str__(self):
        fmtstr = '{name}[AVG:{avg' + self.fmt + '}]'
        return fmtstr.format(**self.__dict__)   

class ProgressMeter(object):
    # 展示
    def __init__(self, total, step, prefix, meters):
        self._fmtstr = self._get_fmtstr(total)
        self.meters = meters
        self.prefix = prefix
        self.total = total

        self.step = step

    def display(self, running):
        if (running + 1) % self.step == 0 or (running + 1) == self.total:
            entries = [self.prefix + self._fmtstr.format(running + 1)]  # [prefix xx.xx/xx.xx]
            entries += [str(meter) for meter in self.meters]
            print('  '.join(entries))

    def _get_fmtstr(self, total):
        num_digits = len(str(total // 1))
        fmt = '{:' + str(num_digits) + 'd}'
        return '[' + fmt + '/' + fmt.format(total) + ']'  # [prefix xx.xx/xx.xx]
    
'''
计算当前batch的精度
'''
def accuracy(outputs, labels):
    with torch.no_grad():
        batch_size = labels.size(0)
        # pred = outputs.argmax(dim=1)
        pred = torch.sigmoid(outputs)
        pred = torch.where(pred > 0.5, 1, 0)

        correct = (pred == labels).sum()
        val = correct / batch_size
        return val
    
def accuracy_gcn(outputs, labels):
    with torch.no_grad():
        batch_size = labels.size(0)
        pred = outputs.argmax(dim=1)

        correct = (pred == labels).sum()
        val = correct / batch_size
        return val



'''
计算每一个类别下的精度
'''   
class ClassAccuracy_gcn:
    def __init__(self, num_classes):
        self.sum = np.zeros(num_classes)
        self.count = np.zeros(num_classes)

    def accuracy(self, outputs, labels):
        _, pred = outputs.max(dim=1)
        correct = pred.eq(labels)

        for b, label in enumerate(labels):
            label = label.cpu()
            self.count[label] += 1
            self.sum[label] += correct[b].cpu()

    def __str__(self):
        fmtstr = '{}:{:6.2f}'
        avg = (self.sum / self.count) * 100
        result = '\n'.join([fmtstr.format(l, a) for l, a in enumerate(avg)])
        return result
    
class ClassAccuracy:
    # 最后一层神经元只有一个
    def __init__(self, num_classes):
        self.sum = torch.zeros(num_classes + 1) # 2
        self.count = torch.zeros(num_classes + 1) # 2

    def accuracy(self, outputs, labels):
        pred = torch.sigmoid(outputs.cpu())
        pred = torch.where(pred > 0.5, 1, 0)
        for b, label in enumerate(labels.cpu()):
            idx = int(label[0])
            self.count[idx] += 1
            self.sum[idx] += (label == pred[b]).sum()

    def __str__(self):
        fmtstr = '{}:{:6.2f}'
        avg = (self.sum / self.count) * 100
        result = '\n'.join([fmtstr.format(l, a) for l, a in enumerate(avg)])
        return result

class ClassAccuracy_all_label:
    def __init__(self, num_classes_main):
        self.num_classes_main = num_classes_main
        self.sum = torch.zeros(num_classes_main + 1)  # 用于主标签的统计
        self.count = torch.zeros(num_classes_main + 1)  # 用于主标签的计数
        self.aux_sum = {}  # 用于辅助标签的统计
        self.aux_count = {}  # 用于辅助标签的计数
        self.len_label = 0

    def accuracy(self, outputs, labels):
        pred = torch.sigmoid(outputs.cpu())
        pred = torch.where(pred > 0.5, 1, 0)

        for b, label in enumerate(labels):
            self.len_label = len(label)
            main_idx = int(label[0])  # 主标签
            self.count[main_idx] += 1
            self.sum[main_idx] += (pred[b] == main_idx).sum().item()

            # 处理辅助标签
            for i, aux_label in enumerate(label[1:], start=1):
                aux_idx = int(aux_label)
                if i not in self.aux_sum:
                    self.aux_sum[i] = {}
                    self.aux_count[i] = {}

                if aux_idx not in self.aux_sum[i]:
                    self.aux_sum[i][aux_idx] = 0
                    self.aux_count[i][aux_idx] = 0

                self.aux_count[i][aux_idx] += 1
                self.aux_sum[i][aux_idx] += (pred[b] == main_idx).sum().item()
        # print(self.aux_sum)

    def __str__(self):
        fmtstr = '{}:{}:{:6.2f}-------{}-{}'
        results = []

        # 打印主标签的准确率
        avg_main = (self.sum / self.count) * 100
        for l, a in enumerate(avg_main):
            results.append(fmtstr.format("Main", l, a, self.sum[l], self.count[l]))

        # 打印辅助标签的准确率
        for i in range(1, self.len_label):
            for aux_idx in self.aux_sum[i]:
                if self.aux_count[i][aux_idx] != 0:
                    avg = (self.aux_sum[i][aux_idx] / self.aux_count[i][aux_idx]) * 100
                    results.append(fmtstr.format(i, aux_idx, avg, self.aux_sum[i][aux_idx], self.aux_count[i][aux_idx]))

        result = '\n'.join(results)
        return result