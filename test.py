import os

def create_txt_files(image_folder):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(image_folder):
        # 检查是否是jpg文件
        if filename.lower().endswith(('.jpg', '.jpeg')):
            # 获取文件名（不含扩展名）
            name_without_ext = os.path.splitext(filename)[0]
            # 创建对应的txt文件
            txt_path = os.path.join(image_folder, name_without_ext + '.txt')
            # 创建空txt文件
            open(txt_path, 'w').close()
            print(f'已创建: {txt_path}')

if __name__ == '__main__':
    # 指定图片文件夹路径
    folder_path = 'test'  # 替换为你的文件夹路径
    create_txt_files(folder_path)