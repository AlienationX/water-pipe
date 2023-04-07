#!/bin/bash

python="e:/Codes/Python/water-pipe/.venv/Scripts/python.exe"
project_path="e:/Codes/Python/water-pipe"
project_path="E:\Codes\Python\water-pipe"

echo $PYTHONPATH

# export PYTHONPATH=$PYTHONPATH:${project_path}      # 报错
export PYTHONPATH=${project_path}                    # 成功

"${python}" "${project_path}/water_pipe/tests/test.py"