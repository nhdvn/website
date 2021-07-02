import numpy as np
import cv2
import onnxruntime
from PIL import Image as ImagePIL

from .utils import *

# model_path = '/home/potato/website/yolo/models/yolov4_1_3_608_608_static.onnx'
model_path = '/home/potato/website/yolo/models/yolov4-tiny_1_3_416_416_static.onnx'

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

    namesfile = '/home/potato/website/yolo/data/coco.names'

    class_names = load_class_names(namesfile)

    image_dst = plot_boxes_cv2(image_src, boxes[0], class_names=class_names)

    return image_dst

def predict(image_path, conf_thresh):
    session = onnxruntime.InferenceSession(model_path)

    image_src = np.array(ImagePIL.open(image_path).convert('RGB'))

    image_dst = detect(session, image_src, conf_thresh)

    return image_dst