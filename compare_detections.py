import cv2
import glob
import os
import numpy as np
from matplotlib import pyplot as plt
from collections import OrderedDict

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
    model_dirs = {os.path.basename(d): d for d in glob.glob(os.path.join(detect_base, '*')) if os.path.isdir(d)}
    sorted_dirs = [(name, model_dirs[name]) for name in FIXED_ORDER if name in model_dirs]
    return OrderedDict(sorted_dirs)

def create_comparison_plot(demo_dir='demo', detect_base='runs/detect'):
    demo_images = sorted(glob.glob(os.path.join(demo_dir, '*.[jp][pn][g]')))
    model_results = get_model_results(detect_base)
    
    n_models = len(model_results) + 1
    n_images = len(demo_images)
    
    # 创建图表，适当调整figsize的宽高比
    fig, axes = plt.subplots(n_models, n_images + 1, 
                            figsize=(4*n_images, 2*n_models),
                            gridspec_kw={
                                'width_ratios': [0.15] + [1]*n_images,
                                'height_ratios': [1]*n_models
                            })
    
    # 显著减小子图之间的间距
    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    
    # 添加行标签
    axes[0, 0].text(0.5, 0.5, '(a)\nOriginal', ha='center', va='center', rotation=0, fontsize=14)
    axes[0, 0].axis('off')
    
    # 显示所有原图
    for j, img_path in enumerate(demo_images):
        original = cv2.imread(img_path)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        axes[0, j+1].imshow(original)
        axes[0, j+1].text(0.02, 0.98, f'(a{j+1})', 
                         transform=axes[0, j+1].transAxes,
                         color='black',
                         fontsize=14,
                         fontweight='bold',
                         va='top')
        axes[0, j+1].axis('off')
    
    # 显示每个模型的检测结果
    for i, (model_name, result_dir) in enumerate(model_results.items(), 1):
        axes[i, 0].text(0.5, 0.5, f'({chr(97+i)})\n{model_name}', 
                       ha='center', 
                       va='center', 
                       rotation=0, 
                       fontsize=14)
        axes[i, 0].axis('off')
        
        for j, img_path in enumerate(demo_images):
            img_name = os.path.basename(img_path)
            result_path = os.path.join(result_dir, img_name)
            
            if os.path.exists(result_path):
                result_img = cv2.imread(result_path)
                result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                axes[i, j+1].imshow(result_img)
                axes[i, j+1].text(0.02, 0.98, f'({chr(97+i)}{j+1})', 
                                transform=axes[i, j+1].transAxes,
                                color='black',
                                fontsize=14,
                                fontweight='bold',
                                va='top')
            axes[i, j+1].axis('off')
    
    # 调整整体布局
    plt.tight_layout(pad=0.5)  # 减小边距
    
    # 保存结果
    save_dir = 'runs/comparison'
    os.makedirs(save_dir, exist_ok=True)
    
    plt.savefig(os.path.join(save_dir, 'model_comparison.pdf'),  
                dpi=300, 
                bbox_inches='tight',
                pad_inches=0.1)
    
    plt.savefig(os.path.join(save_dir, 'model_comparison.png'), 
                dpi=300, 
                bbox_inches='tight',
                pad_inches=0.1)
    plt.close()

if __name__ == '__main__':
    create_comparison_plot()