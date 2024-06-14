# DeepFaceGen: A Large-scale Universal Evaluation Benchmark For Face Forgery Detection
## Dataset Construction

```
datasets
├── FaceForensics++
│   ├── original_sequences
│   │   ├── youtube
│   │   │   ├── c23
│   │   │   │   ├── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   └── c40
│   │   │   │   ├── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │       └── *.npy
│   │   ├── actors
│   │   │   ├── c23
│   │   │   │   ├── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │       └── *.npy
│   │   │   └── c40
│   │   │   │   ├── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │       └── *.npy
│   ├── manipulated_sequences
│   │   ├── Deepfakes
│   │   │   ├── c23
│   │   │   │   └── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │       └── *.npy
│   │   │   └── c40
│   │   │   │   ├── videos
│   │   │   │   │   └── *.mp4
│   │   │   │   └── frames (if you download my processed data)
│   │   │   │   │   └── *.png
|   |   |   |   └── masks (if you download my processed data)
│   │   │   │   │   └── *.png
│   │   │   │   └── landmarks (if you download my processed data)
│   │   │   │       └── *.npy
│   │   ├── Face2Face
│   │   │   ├── ...
│   │   ├── FaceSwap
│   │   │   ├── ...
│   │   ├── NeuralTextures
│   │   │   ├── ...
│   │   ├── FaceShifter
│   │   │   ├── ...
│   │   └── DeepFakeDetection
│   │       ├── ...

Other datasets are similar to the above structure
```
