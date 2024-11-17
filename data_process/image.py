# 切分图片数据集
import pandas as pd
import os
from tqdm import tqdm
from sklearn.model_selection import train_test_split

types = ['img2img']

input_file = '../datasets/i2i_image_labels_relative.csv'
output_folder = '../datasets/images'


df = pd.read_csv(input_file, header=None)
os.makedirs(output_folder, exist_ok=True)

for typ in tqdm(types):
    contains_value = df.iloc[:, 0].str.contains(typ, case=False)
    
    filtered_df = df[contains_value]

    train_fake, temp_fake = train_test_split(filtered_df, test_size=0.3, random_state=42)
    val_fake, test_fake = train_test_split(temp_fake, test_size=2/3, random_state=42)

    output_train = os.path.join(output_folder, f'{typ}_train.csv')
    output_val = os.path.join(output_folder, f'{typ}_val.csv')
    output_test = os.path.join(output_folder, f'{typ}_test.csv')

    train_fake.to_csv(output_train, index=False, header=False)
    val_fake.to_csv(output_val, index=False, header=False)
    test_fake.to_csv(output_test, index=False, header=False)
