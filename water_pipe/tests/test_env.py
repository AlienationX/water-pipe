import sys

print(sys.path)

# 方法1

cur_path = sys.path[0]
print(cur_path)
path = cur_path[:cur_path.find("water_pipe")]
print(path)  # 需要添加 package 的上级目录

sys.path.append(path)
print(sys.path)

import water_pipe

print(water_pipe.__version__)

# 方法2


