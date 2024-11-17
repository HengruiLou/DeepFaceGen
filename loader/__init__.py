from .aigc_loader import load_images 
from .all_label_loader import load_images as ld_all_label
from .kaggle_loader import load_images  as load_kaggle

def load_data(data_name, data_type='train'):
    print('-' * 50)
    print('DATA NAME:', data_name)
    print('DATA TYPE:', data_type)
    print('-' * 50)

    # assert data_name in ['cifar10', 'celeb', 'dfdc', 'sdxl', 'sdre', 'aigc']
    if 'all_label' in data_name:
        data_loader = ld_all_label(data_type, data_name)
    elif 'kaggle' in data_name:
        data_loader = load_kaggle(data_type, data_name)
    else:
        data_loader = load_images(data_type, data_name)
    return data_loader