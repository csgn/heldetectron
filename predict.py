import cv2

from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo


weights = 'weights/model_final.pth'
config_file = 'COCO-Detection/retinanet_R_101_FPN_3x.yaml'
threshold = 0.5
device = 'cpu'
classes = {
    'helmet': (255, 0, 0),
    'vest': (0, 255, 0),
    'head': (0, 0, 255),
}


def load_predictor():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(config_file))
    cfg.MODEL.WEIGHTS = weights
    cfg.MODEL.DEVICE = device

    return DefaultPredictor(cfg)

def make_predict(predictor, image):
    return predictor(image)

def draw_bboxes(image, outputs):
    preds = outputs["instances"].pred_classes.tolist()
    scores = outputs["instances"].scores.tolist()
    bboxes = outputs["instances"].pred_boxes

    for j, bbox in enumerate(bboxes):
        bbox = bbox.tolist()

        score = scores[j]
        pred = preds[j]

        if score > threshold:
            x1, y1, x2, y2 = [int(i) for i in bbox]
            
            class_name, color = classes[pred].items()
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 5)
            cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)


    return image
