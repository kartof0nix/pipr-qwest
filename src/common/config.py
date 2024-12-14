
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

'''
A config class should be generated once for a module - with init specifing what config fields it contains'''

class Config:
    def __init__(self, values : Dict[str, Any] = {}):
        self.config = values

    def set_value(self, name: str, value: Any):
        if name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")
        self.config[name] = value

    def get_value(self, name: str) -> Any:
        if name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")
        return self.config[name]

    def to_dict(self) -> Dict[str, Any]:
        return {key: vars(item) for key, item in self.config.items()}

    def from_dict(self, data: Dict[str, Any]):
        for name, item_data in data.items():
            self.set_value(name, item_data)

    def save_to_file(self, file_path: str):
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_from_file(self, file_path: str):
        with open(file_path, "r") as f:
            data = json.load(f)
        self.from_dict(data)

    # Subscription support
    def __getitem__(self, key: str) -> Any:
        return self.get_value(key)

    def __setitem__(self, key: str, value: Any):
        self.set_value(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self.config


'''User-selected settings (via GUI)'''
class Setting(Config):
    def __init__(self, values : Dict[str, Any] = {}, constrains : Dict[str, Dict[str, Any]] = {}):
        super().__init__(values)
        for key in constrains:
            if("type" not in constrains[key]):
                constrains[key]["type"] = type(values[key])
        self.constrains = constrains

    def check_value(self, name : str, value: Any):
        if name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")

        if type(value) != self.constrains[name]['type'] :
            raise TypeError(f"Type '{type(value)}' not supported")

        if(self.constrains[name]['value_type'] == "bound" and not (self.constrains[name]['min_val'] <= value <= self.constrains[name]['max_val'])):
            raise ValueError(f"Value {value} is not between {self.constrains[name]['min_val']} and {self.constrains[name]['max_val']}")
        
        if(self.constrains[name]['value_type'] == "choice" and not value in self.constrains[name]['choice']):
            raise ValueError(f"Value {value} is not one of {self.constrains[name]['choice']}")
            
    def set_value(self, name, value):
        self.check_value(name, value)
        return super().set_value(name, value)
    
