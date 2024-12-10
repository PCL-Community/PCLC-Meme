import os
import shutil
import hashlib

def calculate_md5(file_path, chunk_size=8192):
    """计算文件的 MD5 哈希值"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()

def move_images_with_rename_and_md5_check(source_dir, dest_dir):
    # 确保目标文件夹存在
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 使用 os.walk 遍历文件夹及子文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件后缀是否符合条件
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                source_file_path = os.path.join(root, file)  # 获取源文件的完整路径
                dest_file_path = os.path.join(dest_dir, file)  # 目标文件路径

                # 计算源文件的 MD5 值
                source_md5 = calculate_md5(source_file_path)

                # 如果文件已存在，比较 MD5
                if os.path.exists(dest_file_path):
                    dest_md5 = calculate_md5(dest_file_path)
                    if source_md5 == dest_md5:
                        print(f'Skipping (same file): {file}')
                        continue  # 如果文件相同则跳过，不移动
                    else:
                        # 文件不同则继续重命名逻辑
                        base_name, ext = os.path.splitext(file)
                        counter = 2
                        while os.path.exists(dest_file_path):
                            new_name = f"{base_name} ({counter}){ext}"
                            dest_file_path = os.path.join(dest_dir, new_name)
                            counter += 1

                # 移动文件到目标文件夹
                shutil.move(source_file_path, dest_file_path)
                print(f'Moved: {file} to {dest_file_path}')

# 示例使用
source_directory = 'PCL2Hub'  # 源文件夹
destination_directory = 'meme'  # 目标文件夹
move_images_with_rename_and_md5_check(source_directory, destination_directory)
