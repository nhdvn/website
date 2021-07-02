
from PIL import Image as ImagePIL
from PIL import ImageDraw
from yolo.yolo import predict

def test_process(path, config):
    image = ImagePIL.open(path)
    editor = ImageDraw.Draw(image)
    shape = [(50, 50), (1000, 1000)]
    editor.rectangle(shape, outline = 'red')
    image.save(path)

def true_process(image, config):
    image_dst = predict(image, config)
    predicted = ImagePIL.fromarray(image_dst)
    predicted.save(image)
