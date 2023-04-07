from abc import ABC, abstractmethod


class Connect(ABC):

    @abstractmethod
    def execute(self, sql):
        pass

    @abstractmethod
    def query(self, sql):
        pass

    @abstractmethod
    def table(self, table_name):
        pass

    @abstractmethod
    def insert(self, table_name):
        pass
    
    def convert_std_dtype(self, dtype):
        # print(dtype)
        if dtype.get() in ["varchar", "unknown"]:  # unknown 为 postgres/greenplum 的数据类型
            return DTYPE("string")
        if dtype.get() == "numeric":
            return DTYPE("decimal", 38, 4)
        
        for key in self.dtype_map:
            types = self.dtype_map[key]
            for type in types:
                if type == dtype.name:
                    dtype.name = key
                    return dtype
        print(f"ERROR: self to std: {dtype} ==> varchar(128)")
    
    def convert_self_dtype(self, dtype):
        for key in self.dtype_map:
            if key == dtype.name:
                dtype.name = self.dtype_map[key][0]
                return dtype
        print(f"ERROR: std to self: {dtype} ==> varchar(128)")


class DTYPE:

    def __init__(self, name: str, precision: int = None, scale: int = None):
        self.name = name
        self.precision = precision
        self.scale = scale

    def get(self) -> str:
        if self.precision and self.scale:
            return f"{self.name}({self.precision},{self.scale})"

        if self.precision:
            return f"{self.name}({self.precision})"

        return self.name

    def __str__(self) -> str:
        return f"name={self.name}, precision={self.precision}, scale={self.scale}"
