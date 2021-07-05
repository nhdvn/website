import numpy as np
import cv2
import onnxruntime
from PIL import Image as ImagePIL

from .utils import *

session_coco = onnxruntime.InferenceSession('yolo/models/yolov4-tiny_1_3_416_416_static.onnx')
session_fruits = onnxruntime.InferenceSession('yolo/models/yolov4-tiny-fruits_1_3_416_416_static.onnx')

class_names_coco = load_class_names('yolo/data/coco.names')
class_names_fruits = load_class_names('yolo/data/fruits.names')

session = session_coco
class_names = class_names_coco

threshold = 0.4

def set_threshold(thresh):
    global threshold
    threshold = thresh

def set_model_data(model_type):

    global session, class_names

    if model_type == 'coco':
        session = session_coco
        class_names = class_names_coco
        return

    if model_type == 'fruits':
        session = session_fruits
        class_names = class_names_fruits
        return


def detect(session, image_src, conf_thresh):

    in_image_h = session.get_inputs()[0].shape[2]
    in_image_w = session.get_inputs()[0].shape[3]

    resized = cv2.resize(image_src, (in_image_w, in_image_h), interpolation=cv2.INTER_LINEAR)
    img_in = np.transpose(resized, (2, 0, 1)).astype(np.float32)
    img_in = np.expand_dims(img_in, axis=0)
    img_in /= 255.0

    input_name = session.get_inputs()[0].name

    outputs = session.run(None, {input_name: img_in})

    boxes = post_processing(img_in, conf_thresh, 0.6, outputs)    

    image_dst = plot_boxes_cv2(image_src, boxes[0], class_names=class_names)

    return image_dst


def predict(image_path, conf_thresh, model_type):

    set_model_data(model_type)

    image_src = np.array(ImagePIL.open(image_path).convert('RGB'))

    image_dst = detect(session, image_src, conf_thresh)

    return image_dst


def predict_video(cap):

    while True:
        ret, frame = cap.read()
        path = 'media/video/demo.jpg'

        if not ret:
            print("Error: failed to capture image")
            break

        image_dst = detect(session, frame, threshold)

        cv2.imwrite(path, image_dst)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(path, 'rb').read() + b'\r\n')