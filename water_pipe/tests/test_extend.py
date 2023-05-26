class A:
    
    def __init__(self, name) -> None:
        self.name = name
        
    def get(self):
        print(self.name)
        
class B:
    pass

a=A('aaa')
a.get()

print(type(a))
print(type(A))
print(a.__class__.__name__)
print(A.__class__.__name__)
print(isinstance(a, (A, B)))

# 动态增加属性
setattr(a, 'info', 'information')
print(a.info)

# 动态增加方法
from types import MethodType
def run(self):
    print('running...')
    
a.run=MethodType(run, a)
a.run()