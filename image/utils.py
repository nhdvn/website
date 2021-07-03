
from PIL import Image as ImagePIL
from PIL import ImageDraw
from yolo.yolo import predict, predict_video


def test_process(path, config, model):
    image = ImagePIL.open(path)
    editor = ImageDraw.Draw(image)
    shape = [(50, 50), (1000, 1000)]
    editor.rectangle(shape, outline = 'red')
    image = image.convert('RGB')
    image.save(path)


def true_process(image, config, model):
    image_dst = predict(image, config, model)
    predicted = ImagePIL.fromarray(image_dst)
    predicted.save(image)


def video_process(cap, config):
    for pred in predict_video(cap, config):
        yield pred
