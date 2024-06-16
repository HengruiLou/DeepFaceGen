# DeepFaceGen: A Large-scale Universal Evaluation Benchmark For Face Forgery Detection (Updating)
## Dataset Construction

```
Image Real Subsets 
├── Celeb-DF
│   ├── *.png
├── ForgeryNet
│   ├── *.jpg
├── real_image_labels_relative.csv (It contains the file paths of all the image-level real samples in the dataset)

Image Forged Subsets (27 mainstream face generation techniques)
├── SD1
│   ├── output_0.png
│   ├──...
│   ├── output_40319.png
├── tra_FSGAN
│   ├── Output00000.jpg
│   ├──...
│   ├── Output10499.jpg
├──...
├── pix2pix
│   ├── fake00001.png
│   ├──...
│   ├── fake10000.png
├── i2i_image_labels_relative.csv (It contains the file paths of all the image2image forged samples in the dataset)
├── t2i_image_labels_relative.csv (It contains the file paths of all the text2image forged samples in the dataset)
├── tra_image_labels_relative.csv (It contains the file paths of all the localized editing-based forged samples in the dataset)

Video Real Subsets 
├── CMLR
│   ├── *.mp4
├── ForgeryNet
│   ├── *.mp4
├── Celeb-DF
│   ├── *.mp4
├── CN-CVS
│   ├── *.mp4
├── real_video_labels_relative.csv (It contains the file paths of all the video-level real samples in the dataset)

Video Forged Subsets (16 mainstream face generation techniques)
├── Animatediff-rs
│   ├── output_0.mp4
│   ├──...
│   ├── output_40319.mp4
├── tra_FaceShifter
│   ├── Output_2_000000.mp4
│   ├──...
│   ├── Output078721.mp4
├──...
├── t2v_video_labels_relative.csv (It contains the file paths of all the text2video forged samples in the dataset)
├── tra_video_labels_relative.csv (It contains the file paths of all the localized editing-based forged samples in the dataset)
```
