class A:
    
    def __init__(self, name) -> None:
        self.name = name
        
    def get(self):
        print(self.name)
        

a=A('aaa')
a.get()

# 动态增加属性
setattr(a, 'info', 'information')
print(a.info)

# 动态增加方法
from types import MethodType
def run(self):
    print('running...')
    
a.run=MethodType(run, a)
a.run()