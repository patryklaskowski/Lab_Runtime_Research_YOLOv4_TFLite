# Lab_Runtime_Research_YOLOv4_TFLite/tools

---

Tools that were used for performance analytics.

### 1. Initialize vitual environment and install requirements

```bash
cd tools
python3.7 -m venv env
source env/bin/activate

python3 -m pip install -r requirements.txt
```

### 2. Download model and place in `Lab_Runtime_Research_YOLOv4_TFLite/tools/Yolov4_TensorFlow_Lite_Model/models`

Download `.tflite` model: [from my Google Drive](https://drive.google.com/file/d/1ARWYou1LfNq9aIBB5r4pDZCE6S3Lcni6/view?usp=sharing)
**Model path should be `Lab_Runtime_Research_YOLOv4_TFLite/tools/Yolov4_TensorFlow_Lite_Model/models/yolov4-coco-416.tflite`**

### 3. Run `test2.py`

```bash
python3 test2.py
```

---
