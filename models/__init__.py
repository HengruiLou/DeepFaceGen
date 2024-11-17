import torch
import timm
import torch.nn as nn

def load_model(model_name, in_channels=3, num_classes=1):
    print('-' * 50)
    print('LOAD MODEL:', model_name)
    print('-' * 50)

    if model_name == 'xception':
        model = models.xcetion.Xception_concat(num_classes)

    return model
