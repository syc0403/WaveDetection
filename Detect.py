import warnings
import glob
import os
warnings.filterwarnings('ignore')
from ultralytics import YOLO, RTDETR

def detect_all_models(base_dir='runs/train'):
    # 查找所有模型权重文件
    weight_files = glob.glob(os.path.join(base_dir, '**/weights/best.pt'), recursive=True)
    
    for weight_path in weight_files:
        # 获取模型名称
        model_name = os.path.basename(os.path.dirname(os.path.dirname(weight_path)))
        print(f"\n使用模型进行检测: {model_name}")
        
        # 根据模型名称选择对应的模型类型
        if 'rtdetr' in model_name.lower():
            model = RTDETR(weight_path)
        else:
            model = YOLO(weight_path)
            
        model.predict(
            source='demo',
            imgsz=640,
            project='runs/detect',
            name=model_name,
            save=True,
            line_width=5
            # classes=0, # 是否指定检测某个类别
        )

if __name__ == '__main__':
    detect_all_models()