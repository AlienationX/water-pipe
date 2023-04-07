import sys

print(sys.path)

# 方法1，使用python程序添加 project 路径到 sys.path

cur_path = sys.path[0]
print(cur_path)
path = cur_path[:cur_path.find("water_pipe")]
print(path)  # 需要添加 package 的上级目录

# sys.path.append(path)
sys.path.insert(0, path)
print(sys.path)

import water_pipe

print(water_pipe.__version__)

# 方法2，使用shell程序添加 project 路径到 PYTHONPATH，推荐