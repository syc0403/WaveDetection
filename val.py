import warnings
import glob
import os
warnings.filterwarnings('ignore')
from ultralytics import YOLO, RTDETR

def val_all_models(base_dir='runs/train'):
    # 查找所有模型权重文件
    weight_files = glob.glob(os.path.join(base_dir, '**/weights/best.pt'), recursive=True)
    
    for weight_path in weight_files:
        # 获取模型名称（文件夹名）
        model_name = os.path.basename(os.path.dirname(os.path.dirname(weight_path)))
        print(f"\n正在评估模型: {model_name}")
        
        # 根据模型名称选择对应的模型类型
        if 'rtdetr' in model_name.lower():
            model = RTDETR(weight_path)
        else:
            model = YOLO(weight_path)
            
        model.val(
            data=r'./data.yaml',
            split='test',
            imgsz=640,
            batch=16,
            project='runs/test',
            name=model_name,
        )

if __name__ == '__main__':
    val_all_models()