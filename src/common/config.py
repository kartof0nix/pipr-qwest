
import json
from typing import Any, Dict, List
from dataclasses import dataclass, field
from pathlib import Path

import traceback
import logging
logger = logging.getLogger(__name__)


'''
A config class should be generated once for each module that needs it - with init specifing what config fields it contains
'''

# def clearAllSettings():
#     """
#     Removes every file in the config directory.
#     """
#     for item in CONFIG_PATH.iterdir():
#         # Check if the item is a file and remove it
#         if item.is_file():
#             item.unlink()


class Config:
    CONFIG_PATH = Path("~/.pipr-qwest/config").expanduser()

    def __init__(self, filename, defaultValues: Dict[str, Any] = {}, readAll=False, critical=True):
        self.critical = critical
        self.readAll = readAll
        self.name = filename
        if (not self.CONFIG_PATH.exists()):
            self.CONFIG_PATH.mkdir(parents=True)
            logger.info("Directory %s not found, creating",
                        self.CONFIG_PATH.absolute())
        self.defaultValues = defaultValues
        self.fpath = self.CONFIG_PATH.joinpath(filename)
        self.config = dict(defaultValues)
        self.load_from_file()
        logger.info("Config %s : %s", filename, self.config)
        self.save_to_file()  # If any values have been fixed, import

    def reset(self):
        self.config = self.defaultValues

    def set_value(self, name: str, value: Any):
        if not self.readAll and name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")
        self.config[name] = value

    def get_value(self, name: str) -> Any:
        if name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")
        return self.config[name]

    # def to_dict(self) -> Dict[str, Any]:
    #     return {key: vars(item) for key, item in self.config}

    def from_dict(self, data: Dict[str, Any]):
        for key in self.config:
            if key not in data:
                logger.info("Key %s not defined in config %s", key, self.fpath)
        for name, item_data in data.items():
            try:
                logger.info("Setting %s = %s", name, item_data)
                self.set_value(name, item_data)
            except KeyError:
                logger.warning(
                    "Config file %s contains invalid key %s", self.fpath, self.name)

    def save_to_file(self):
        with open(self.fpath, "w") as f:
            json.dump(self.config, f, indent=4)

    def load_from_file(self):
        logger.debug("Loading config from %s", self.fpath.absolute())
        try:
            with open(self.fpath, "r") as f:
                data = json.load(f)
            self.from_dict(data)
        except Exception as e:
            if (self.critical):
                logger.error("Failed to load file: %s", e)
                logger.debug("Failed to load file: %s", traceback.format_exc())

    # Subscription support
    def __getitem__(self, key: str) -> Any:
        return self.get_value(key)

    def __setitem__(self, key: str, value: Any):
        self.set_value(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self.config


'''User-selected settings (via GUI)'''


class Setting(Config):

    def __init__(self, name: str, defaultValues: Dict[str, Any] = {}, constrains: Dict[str, Dict[str, Any]] = {}):
        for key in constrains:
            if ("type" not in constrains[key]):
                constrains[key]["type"] = type(defaultValues[key])
        self.name = name
        self.constrains = constrains
        super().__init__(name, defaultValues)

    def check_value(self, name: str, value: Any):
        if name not in self.config:
            raise KeyError(f"Config item '{name}' not found.")

        if isinstance(value, self.constrains[name]['type']):
            raise TypeError(f"Type '{type(value)}' does not match {
                            name}'s type {self.constrains[name]['type']}")

        if (self.constrains[name]['value_type'] == "bound" and not (self.constrains[name]['min_val'] <= value <= self.constrains[name]['max_val'])):
            raise ValueError(f"Value {value} is not between {
                             self.constrains[name]['min_val']} and {self.constrains[name]['max_val']}")

        if (self.constrains[name]['value_type'] == "selectable" and value not in self.constrains[name]['selectable']):
            raise ValueError(f"Value {value} is not one of {
                             self.constrains[name]['selectable']}")

    def set_value(self, name, value):
        self.check_value(name, value)
        return super().set_value(name, value)


'''
A global list of registered settings from any module edditable from GUI
'''
registered_settings: List[Setting] = []
