# 切分视频数据集

import pandas as pd
import os
from tqdm import tqdm
import cv2
from sklearn.model_selection import train_test_split

types = ['Animatediff-rs']

input_file = '../datasets/t2v_video_labels_relative.csv'
video_output_folder = '../datasets/videos'
image_output_folder = '../datasets/images'

os.makedirs(image_output_folder, exist_ok=True)

df = pd.read_csv(input_file, header=None)

for typ in tqdm(types):
    contains_value = df.iloc[:, 0].str.contains(typ, case=False)
    filtered_df = df[contains_value]

    train_fake, temp_fake = train_test_split(filtered_df, test_size=0.3, random_state=42)
    val_fake, test_fake = train_test_split(temp_fake, test_size=2/3, random_state=42)

    output_train = os.path.join(output_folder, f'{typ}_train.csv')
    output_val = os.path.join(output_folder, f'{typ}_val.csv')
    output_test = os.path.join(output_folder, f'{typ}_test.csv')

    # 用于保存新的数据集信息
    train_data = []
    val_data = []
    test_data = []

    def process_videos(data_split, output_list, split_name):
        for index, row in data_split.iterrows():
            video_path = row[0]  
            label = row[1]       

            if not os.path.exists(video_path):
                continue

            # 创建类别文件夹
            class_folder = os.path.join(image_output_folder, split_name, typ)
            os.makedirs(class_folder, exist_ok=True)

            # 读取视频并截取帧
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # frames_to_capture = min(10, frame_count)  
            frame_interval = max(frame_count // frames_to_capture, 1)

            frame_idx = 0
            captured_frames = 0

            while cap.isOpened() and captured_frames < frames_to_capture:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % frame_interval == 0:
                    output_image_path = os.path.join(class_folder, f"{os.path.basename(video_path)}_frame{captured_frames}.jpg")
                    cv2.imwrite(output_image_path, frame)
                    output_list.append([output_image_path, label])
                    captured_frames += 1

                frame_idx += 1

            cap.release()

    process_videos(train_fake, train_data, "train")
    process_videos(val_fake, val_data, "val")
    process_videos(test_fake, test_data, "test")

    pd.DataFrame(train_data).to_csv(output_train, index=False, header=False)
    pd.DataFrame(val_data).to_csv(output_val, index=False, header=False)
    pd.DataFrame(test_data).to_csv(output_test, index=False, header=False)

