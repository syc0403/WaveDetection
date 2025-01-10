import cv2
import glob
import os
import numpy as np
from matplotlib import pyplot as plt
from collections import OrderedDict
# 固定的模型顺序
FIXED_ORDER = [
    'RT-DETR-L',
    'YOLOv5n',
    'YOLOv6n',
    'YOLOv8n',
    'YOLOv9t',
    'YOLOv10n',
    'YOLOv11l',
    'YOLOv11m',
    'YOLOv11n',
    'YOLOv11s'
]

def get_model_results(detect_base='runs/detect'):
    # 获取所有子目录
    model_dirs = {os.path.basename(d): d for d in glob.glob(os.path.join(detect_base, '*')) if os.path.isdir(d)}
    
    # 按照固定顺序生成 OrderedDict
    sorted_dirs = [(name, model_dirs[name]) for name in FIXED_ORDER if name in model_dirs]
    return OrderedDict(sorted_dirs)
def create_comparison_plot(demo_dir='demo', detect_base='runs/detect'):
    demo_images = sorted(glob.glob(os.path.join(demo_dir, '*.[jp][pn][g]')))
    model_results = get_model_results(detect_base)
    print(model_results)
    # 减小每行高度，从3改为2
    n_models = len(model_results) + 1
    n_images = len(demo_images)
    plt.figure(figsize=(4*n_images, 2*n_models))
    
    # 调整网格布局，进一步减小列间距
    grid = plt.GridSpec(n_models, n_images+1, 
                       width_ratios=[0.2] + [1]*n_images,
                       hspace=0.1,  # 行间距
                       wspace=0.01)  # 列间距
    
    # 添加行标签
    plt.subplot(grid[0, 0])
    plt.text(0.5, 0.5, '(a)\nOriginal', ha='center', va='center', rotation=0, fontsize=14)
    plt.axis('off')
    
    # 显示所有原图
    for j, img_path in enumerate(demo_images):
        plt.subplot(grid[0, j+1])
        original = cv2.imread(img_path)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        plt.imshow(original)
        # 添加字母标签
        plt.text(0.02, 0.98, f'(a{j+1})', 
                transform=plt.gca().transAxes,
                color='red',
                fontsize=14,
                fontweight='bold',
                va='top')
        plt.axis('off')
    
    # 显示每个模型的检测结果
    for i, (model_name, result_dir) in enumerate(model_results.items(), 1):
        # 添加模型名称和字母标签
        plt.subplot(grid[i, 0])
        plt.text(0.5, 0.5, f'({chr(97+i)})\n{model_name}', 
                ha='center', 
                va='center', 
                rotation=0, 
                fontsize=14)
        plt.axis('off')
        
        # 显示该模型的所有检测结果
        for j, img_path in enumerate(demo_images):
            img_name = os.path.basename(img_path)
            result_path = os.path.join(result_dir, img_name)
            
            plt.subplot(grid[i, j+1])
            if os.path.exists(result_path):
                result_img = cv2.imread(result_path)
                result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                plt.imshow(result_img)
                # 添加字母数字标签
                plt.text(0.02, 0.98, f'({chr(97+i)}{j+1})', 
                        transform=plt.gca().transAxes,
                        color='red',
                        fontsize=14,
                        fontweight='bold',
                        va='top')
            plt.axis('off')
    
    # 保存结果
    save_dir = 'runs/comparison'
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, 'model_comparison.pdf'),  
                dpi=300, 
                bbox_inches='tight',
                pad_inches=0.2,  # 整体边距也稍微减小
                format='pdf')
    
    plt.savefig(os.path.join(save_dir, 'model_comparison.png'), 
                dpi=300, 
                bbox_inches='tight',
                pad_inches=0.2)
    plt.close()

if __name__ == '__main__':
    create_comparison_plot() 