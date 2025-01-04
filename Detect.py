import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('runs/train/YOLOv11n/weights/best.pt') # select your model.pt path
    model.predict(source='E:/data/wave/all_wave_images',
                  imgsz=640,
                  project='runs/detect',
                  name='yolov11n',
                  save=True,
                  iou=0.9,
                  # classes=0, 是否指定检测某个类别.
                )