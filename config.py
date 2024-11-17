# 路径
base_dir = 'root_path/'
dataset_dir = base_dir + 'dataset/'
output_dir = root_dir + 'output/'


# 数据集参数设置
def get_data_config(data_name):
    config = {}

    config['img_size'] = 299
    config['in_channels'], config['num_classes'], config['batch_size'] = 3, 1, 64


    config['train_csv'] = dataset_dir + '/datasets/images/' + data_name + '_train.csv'
    config['test_csv'] = dataset_dir + '/datasets/images/' + data_name + '_test.csv'
    
    return config


# 训练参数-optim
lr=0.001
momentum=0.9
weight_decay=0.001
# scheduler
step_size=2
gamma=0.5
# epochs
num_epochs=100