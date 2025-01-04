import warnings
warnings.filterwarnings('ignore')
import argparse
import os
import time
import numpy as np
import torch
import torch.utils.data
from tqdm import tqdm
from ultralytics.utils.torch_utils import select_device
from ultralytics.nn.tasks import attempt_load_weights
import logging
from tabulate import tabulate
import glob

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_weight_size(path):
    """获取模型权重文件的大小（以MB为单位）。"""
    try:
        stats = os.stat(path)
        return f'{stats.st_size / (1024 ** 2):.1f}'
    except OSError as e:
        logging.error(f"Error getting weight size: {e}")
        return "N/A"


def warmup_model(model, device, example_inputs, iterations=200):
    """模型预热，准备进行高效推理。"""
    logging.info("Beginning warmup...")
    for _ in tqdm(range(iterations), desc='Warmup'):
        model(example_inputs)


def test_model_latency(model, device, example_inputs, iterations=1000):
    """测试模型的推理延迟。"""
    logging.info("Testing latency...")
    time_arr = []
    for _ in tqdm(range(iterations), desc='Latency Test'):
        if device.type == 'cuda':
            torch.cuda.synchronize(device)
        start_time = time.time()

        model(example_inputs)

        if device.type == 'cuda':
            torch.cuda.synchronize(device)
        end_time = time.time()
        time_arr.append(end_time - start_time)

    return np.mean(time_arr), np.std(time_arr)


def test_all_models(opt):
    """测试多个模型并比较结果"""
    device = select_device(opt.device)
    results = []
    
    # 获取所有模型权重文件
    if os.path.isdir(opt.weights):
        weight_files = glob.glob(os.path.join(opt.weights, '**/best.pt'), recursive=True)
    else:
        weight_files = [opt.weights]
    
    for weights in weight_files:
        try:
            model = attempt_load_weights(weights, device=device, fuse=True)
            model = model.to(device)
            example_inputs = torch.randn((opt.batch, 3, *opt.imgs)).to(device)

            if opt.half:
                model = model.half()
                example_inputs = example_inputs.half()

            warmup_model(model, device, example_inputs, opt.warmup)
            mean_latency, std_latency = test_model_latency(model, device, example_inputs, opt.testtime)
            
            model_name = os.path.basename(os.path.dirname(os.path.dirname(weights)))
            results.append([
                model_name,
                f"{get_weight_size(weights)}M",
                f"{mean_latency:.5f}s",
                f"{1 / mean_latency:.1f}",
                opt.batch
            ])
            
            # 释放显存
            del model
            torch.cuda.empty_cache()
            
        except Exception as e:
            logging.error(f"测试模型 {weights} 时出错: {e}")
    
    # 输出表格形式的结果
    headers = ["Model", "Size", "Latency", "FPS", "Batch"]
    print("\n" + tabulate(results, headers=headers, tablefmt="grid"))


def main(opt):
    test_all_models(opt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test YOLOv11 model performance.")
    parser.add_argument('--weights', type=str, default='runs/train', help='model weights path or directory')
    parser.add_argument('--batch', type=int, default=1, help='total batch size for all GPUs')
    parser.add_argument('--imgs', nargs='+', type=int, default=[640, 640], help='image sizes [height, width]')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--warmup', default=200, type=int, help='warmup iterations')
    parser.add_argument('--testtime', default=1000, type=int, help='test iterations for latency')
    parser.add_argument('--half', action='store_true', help='use FP16 mode for inference')
    opt = parser.parse_args()

    main(opt)
