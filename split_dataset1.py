from pathlib import Path
import random
import shutil
from tqdm import tqdm

def create_dataset_structure(dst_root):
    """
    创建数据集目录结构
    
    Args:
        dst_root: 目标根目录路径
    """
    dst_root = Path(dst_root)
    
    # 创建目录结构
    for split in ['train', 'val', 'test']:
        for type in ['images', 'labels']:
            (dst_root / type / split).mkdir(parents=True, exist_ok=True)
    
    return dst_root

def split_dataset(src_dir, dst_dir, test_class='taozhi', train_ratio=0.7, val_ratio=0.2):
    """
    划分数据集
    
    Args:
        src_dir: 源目录(包含图片和标签)
        dst_dir: 目标目录(存放划分后的数据集)
        test_class: 作为测试集的类别名称
        train_ratio: 训练集比例
        val_ratio: 验证集比例
    """
    # 创建目录结构
    dataset_root = create_dataset_structure(dst_dir)
    
    # 获取所有图片文件
    img_files = list(Path(src_dir).glob('*.jpg'))
    
    # 分离测试集和其他数据
    test_files = [img for img in img_files if test_class in img.stem]
    other_files = [img for img in img_files if test_class not in img.stem]
    
    # 随机打乱其他数据
    random.seed(42)  # 设置随机种子以保证可重复性
    random.shuffle(other_files)
    
    # 计算训练集和验证集大小
    n_other = len(other_files)
    n_train = int(n_other * train_ratio)
    n_val = int(n_other * val_ratio)
    
    # 划分训练集和验证集
    splits = {
        'train': other_files[:n_train],
        'val': other_files[n_train:n_train + n_val],
        'test': test_files
    }
    
    # 复制文件到对应文件夹
    for split_name, files in splits.items():
        print(f'\n处理{split_name}集...')
        for img_path in tqdm(files, desc=f'复制{split_name}集'):
            # 复制图片
            dst_img = dataset_root / 'images' / split_name / img_path.name
            shutil.copy2(img_path, dst_img)
            
            # 复制对应的标签文件
            label_path = img_path.with_suffix('.txt')
            if label_path.exists():
                dst_label = dataset_root / 'labels' / split_name / label_path.name
                shutil.copy2(label_path, dst_label)
            else:
                print(f'警告: 未找到标签文件 {label_path}')

    # 打印统计信息
    print('\n数据集划分完成!')
    print(f'总数据集大小: {len(img_files)}')
    print(f'训练集: {len(splits["train"])} ({train_ratio*100:.0f}%)')
    print(f'验证集: {len(splits["val"])} ({val_ratio*100:.0f}%)')
    print(f'测试集: {len(splits["test"])} ({(1-train_ratio-val_ratio)*100:.0f}%)')

if __name__ == '__main__':
    # 使用示例
    split_dataset(
        src_dir='E:/data/wave/augmented_waves',    # 替换为你的源数据目录
        dst_dir='datasets',                        # 替换为你想要的目标目录
        test_class='taozhi'                        # 指定测试集类别
    )