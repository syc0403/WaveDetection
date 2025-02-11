# import os
# import subprocess

# def cut_first_minute(input_folder, output_folder):
#     # 如果输出文件夹不存在，创建它
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # 获取所有MP4文件
#     for filename in os.listdir(input_folder):
#         if filename.endswith('.mp4'):
#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_folder, f'first_minute_{filename}')
            
#             # FFmpeg命令：截取前60秒
#             command = [
#                 'ffmpeg',
#                 '-i', input_path,           # 输入文件
#                 '-ss', '0',                 # 开始时间
#                 '-t', '60',                 # 持续时间（秒）
#                 '-c:v', 'copy',             # 复制视频编码（避免重新编码）
#                 '-c:a', 'copy',             # 复制音频编码
#                 output_path
#             ]
            
#             try:
#                 subprocess.run(command, check=True)
#                 print(f'Successfully processed: {filename}')
#             except subprocess.CalledProcessError as e:
#                 print(f'Error processing {filename}: {e}')

# # 使用示例
# input_folder = 'E:/格美'
# output_folder = 'video'
# cut_first_minute(input_folder, output_folder)

# import os

# def get_third_video_files(folder_path):
#     # 获取文件夹中所有文件
#     files = os.listdir(folder_path)
    
#     # 过滤出所有 mp4 文件
#     mp4_files = [f for f in files if f.endswith('.mp4')]
    
#     # 按照顺序保留每第三个文件
#     selected_files = mp4_files[::3]
    
#     return selected_files

# # 设置文件夹路径
# folder_path = 'video'  # 修改为您文件夹的实际路径

# # 获取每第三个视频文件
# selected_files = get_third_video_files(folder_path)

# # 打印结果
# for file in selected_files:
#     print(file)

import os

def delete_unwanted_videos(folder_path):
    # 获取文件夹中所有文件
    files = os.listdir(folder_path)
    
    # 过滤出所有 mp4 文件
    mp4_files = [f for f in files if f.endswith('.mp4')]
    
    # 按照顺序保留从第一个开始的每第三个文件
    selected_files = mp4_files[::3]
    
    # 删除其他不需要的视频
    for file in mp4_files:
        if file not in selected_files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)  # 删除文件
            print(f"Deleted: {file}")

# 设置文件夹路径
folder_path = 'video'  # 修改为您文件夹的实际路径

# 执行删除操作
delete_unwanted_videos(folder_path)
