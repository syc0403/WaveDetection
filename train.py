from ultralytics.models import YOLO
import os
from swanlab.integration.ultralytics import add_swanlab_callback
import swanlab
 
if __name__ == '__main__':
    # 初始化SwanLab项目
    swanlab.init(project="YOLOv11_Wave_Detection", experiment_name="YOLOv11",)
    
    # 加载YOLO模型配置
    model = YOLO(model='ultralytics/cfg/models/11/yolo11.yaml')
    
    # 添加SwanLab回调
    add_swanlab_callback(model)
    
    # 开始训练
    model.train(
        data='./data.yaml',      # 数据配置文件
        epochs=100,                # 训练轮数
        batch=16,                # 批次大小
        device='0',             # 使用GPU 0
        optimizer='SGD',
        pretrained=False,
        imgsz=640,              # 图像尺寸
        workers=2,              # 数据加载线程数
        cache=False,            # 不使用缓存
        amp=True,               # 使用混合精度训练
        mosaic=False,           # 关闭马赛克数据增强
        project='runs/train',   # 输出目录
        name='YOLOv11'              # 实验名称
    )