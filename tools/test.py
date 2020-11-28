import cv2
import time
import numpy as np
import os


def video_stream_with_trackbars():
    from Yolov4_TensorFlow_Lite_Model.TensorFlowLiteModel import Yolov4TensorFlowLiteModel
    from random import uniform

    model_path = './Yolov4_TensorFlow_Lite_Model/models/yolov4-coco-416.tflite'
    names_path = './Yolov4_TensorFlow_Lite_Model/labels/coco.names'

    # TF model
    tflite_model = Yolov4TensorFlowLiteModel(model_path, names_path, treshold=0.2, iou=0.4)

    def nothing(x):
        pass
    
    # Camera
    time.sleep(uniform(1, 4))
    cam = cv2.VideoCapture(0) # http://208.139.200.133/mjpg/video.mjpg
    time.sleep(1)

    # Video
    video_window = f'VideoFeed PID: {os.getpid()}'

    # Trackbars
    blank = np.zeros((10,400,3), np.uint8)
    trackbars_window = f'Trackbars PID: {os.getpid()}'

    cv2.namedWindow(trackbars_window)
    cv2.createTrackbar('show_info', trackbars_window, 1, 1, nothing)
    cv2.createTrackbar('scale', trackbars_window, 10, 10, nothing)
    cv2.createTrackbar('max_fps', trackbars_window, 30, 40, nothing)
    cv2.createTrackbar('tensorflow', trackbars_window, 0, 1, nothing)
    cv2.createTrackbar('gray', trackbars_window, 0, 1, nothing)
    cv2.createTrackbar('show', trackbars_window, 0, 1, nothing)

    # MainStream / SubStream variables
    counterMainStream = 0
    counterSubStream = 0
    timerMainStream = time.perf_counter()
    timerSubStream = time.perf_counter()

    firstShot = True
    text = 'Info off'
    opened = False
    fps_main = fps_sub = 0

    while True:
        success, img = cam.read()
        assert success, 'Cant get img'
        
        if firstShot:
            imgShow = img
            firstShot = False

        imgHeight, imgWidth, *_= img.shape

        # Main stream
        counterMainStream += 1
        if time.perf_counter() - timerMainStream >= 1:

            print(text + f'    %2.2f s (benchmark: 1 s.)' % (time.perf_counter() - timerMainStream))

            fps_main = counterMainStream
            counterMainStream = 0
            timerMainStream = time.perf_counter()

        # Get trackbar info
        show_info = cv2.getTrackbarPos('show_info', trackbars_window)
        scale = cv2.getTrackbarPos('scale', trackbars_window)
        scale = 1/10 if scale == 0 else scale/10
        max_fps = cv2.getTrackbarPos('max_fps', trackbars_window)
        max_fps = 1 if max_fps == 0 else max_fps
        tensorflow = cv2.getTrackbarPos('tensorflow', trackbars_window)
        gray = cv2.getTrackbarPos('gray', trackbars_window)
        show = cv2.getTrackbarPos('show', trackbars_window)

        # Sub stream
        #
        # This not prevent from capturing maximum fps.
        # This limits number of processed fps.
        #
        if counterMainStream < max_fps:
            counterSubStream += 1
            if time.perf_counter() - timerSubStream >= 1:
                fps_sub = counterSubStream
                counterSubStream = 0
                timerSubStream = time.perf_counter()

            img = cv2.resize(img, (int(imgWidth * scale), int(imgHeight * scale)))
            
            if gray:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if tensorflow:
                img = tflite_model.predict(img, resize=False)

            if show_info:
                text = (
                    f'FPS_main: {fps_main}; '
                    f'FPS_sub: {fps_sub}; '
                    f'Scale: {scale*100}%; '
                    f'Max_fps: {max_fps}; '
                    f'Shape: {img.shape}; '
                    f'PID: {os.getpid()};')
                img = cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7*scale, (0, 255, 0), int(2*scale), cv2.LINE_AA)
            else:
                text = 'Info off'
            imgShow = img

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Quitting...')
            break

        if show:
            cv2.imshow(video_window, imgShow)
            opened = 1
        if not show and opened:
            cv2.destroyWindow(video_window)
            opened = 0
        cv2.imshow(trackbars_window, blank)
    
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_stream_with_trackbars()