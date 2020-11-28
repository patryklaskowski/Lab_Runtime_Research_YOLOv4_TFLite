# run_example.py

from TensorFlowLiteModel import create_prediction_stream

def raw_yolov4_tflite():
    model_path = 'Yolov4_TensorFlow_Lite_Model/models/yolov4-coco-416.tflite'
    names_path = 'Yolov4_TensorFlow_Lite_Model/labels/coco.names'
    video_source = 0 # 'http://208.139.200.133/mjpg/video.mjpg'
    create_prediction_stream(model_path, names_path, video_source)

if __name__ == '__main__':
    
    raw_yolov4_tflite()
