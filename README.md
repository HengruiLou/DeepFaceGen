# DeepFaceGen: A Large-scale Universal Evaluation Benchmark For Face Forgery Detection (Updating)
## Dataset Construction
> Abstract: The rapid progress of photorealistic synthesis techniques has reached at a critical point where the boundary between real and manipulated images starts to blur. Thus, benchmarking and advancing digital forgery analysis have become a pressing issue. However, existing face forgery datasets either have limited diversity or only support coarse-grained analysis. To counter this emerging threat, we construct the ForgeryNet dataset, an extremely large face forgery dataset with unified annotations in image- and video-level data across **four tasks**: 1) *Image Forgery Classification*, including two-way (real / fake), three-way (real / fake with identity-replaced forgery approaches / fake with identity-remained forgery approaches), and n-way (real and 15 respective forgery approaches) classification. 2) *Spatial Forgery Localization*, which segments the manipulated area of fake images compared to their corresponding source real images. 3) *Video Forgery Classification*, which re-defines the video-level forgery classification with manipulated frames in random positions. This task is important because attackers in real world are free to manipulate any target frame. and 4) *Temporal Forgery Localization*, to localize the temporal segments which are manipulated. ForgeryNet is by far the largest publicly available deep face forgery dataset in terms of data-scale (**2.9 million** images, **221,247** videos), manipulations (**7 image-level approaches, 8 video-level approaches**), perturbations (36 independent and more mixed perturbations) and annotations (**6.3 million** classification labels, **2.9 million** manipulated area annotations and **221,247** temporal forgery segment labels). We perform extensive benchmarking and studies of existing face forensics methods and obtain several valuable observations.
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
