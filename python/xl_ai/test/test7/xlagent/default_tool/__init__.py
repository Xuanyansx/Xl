import importlib
import pkgutil


# tools_dict = {}

# for i in pkgutil.iter_modules(__path__):
#     mod = importlib.import_module(f"{__name__}.{i.name}")
#     for name,value in vars(mod).items():
#         if isinstance(value,type):
#             tools_dict[name] = value            


class Tools:
    def __init__(self,cfg):
        self.__tools_dict = {}
        for i in pkgutil.iter_modules(__path__):
            mod = importlib.import_module(f"{__name__}.{i.name}")
            for name,value in vars(mod).items():
                if isinstance(value,type):
                    if value.__module__ == mod.__name__:
                        obj = value()
                        obj.cfg = cfg
                        self.__tools_dict[name] = obj

#  2026/10/31 19:38:自动注册工具，hhhhh
        

    @property
    def tools_dict(self):
        return self.__tools_dict
    
