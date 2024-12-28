from ultralytics.models import YOLO
import os
from swanlab.integration.ultralytics import add_swanlab_callback
import swanlab
 
if __name__ == '__main__':
    # 初始化SwanLab项目
    swanlab.init(project="YOLOv11_Wave_Detection", experiment_name="YOLOv11s",)
    
    # 加载YOLO模型配置
    model = YOLO(model='yolo11s.yaml')
    
    # 添加SwanLab回调
    add_swanlab_callback(model)
    
    # 开始训练
    model.train(
        data='./data.yaml',      # 数据配置文件
        cache=False,
        imgsz=640,
        epochs=100,
        single_cls=True,  # 是否是单类别检测
        batch=16,
        close_mosaic=0,
        workers=0,
        device='0',
        optimizer='SGD', # using SGD 优化器 默认为auto建议大家使用固定的.
        # resume=, # 续训的话这里填写True, yaml文件的地方改为lats.pt的地址,需要注意的是如果你设置训练200轮次模型训练了200轮次是没有办法进行续训的.
        amp=True,  # 如果出现训练损失为Nan可以关闭amp
        project='runs/train',   # 输出目录
        name='YOLOv11s'              # 实验名称
    )