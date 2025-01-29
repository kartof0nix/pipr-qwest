
## **Configuration Management with `config.py`**

The `config.py` file provides classes to manage configuration settings for your game, including saving, loading, and validating settings.

------


### **1. Basic Usage**

#### **Initialization**
Create a configuration object by specifying a filename and default values:
```python
from common.config import Config

config = Config("game_config.json", {"volume": 50, "difficulty": "medium"})
```

#### **Accessing Values**
Retrieve or modify configuration values:
```python
volume = config["volume"]  # Get the value
config["volume"] = 75      # Set the value
```

#### **Saving and Loading**
- Configurations are automatically saved to `~/.pipr-qwest/config/<filename>`.
- They are loaded automatically during initialization.

#### **Reset to Default Values**
```python
config.reset()  # Resets all values to the provided defaults
```

---

### **2. Validating Settings with Constraints**
For settings that require validation, use the `Setting` class.

#### **Initialization with Constraints**
```python
from common.config import Setting

setting = Setting(
    "user_preferences.json",
    {"brightness": 50},
    constrains={
        "brightness": {"type": int, "value_type": "bound", "min_val": 0, "max_val": 100}
    }
)
```

#### **Setting Values**
```python
setting.set_value("brightness", 75)  # Valid
setting.set_value("brightness", 200)  # Raises ValueError
```

---

### **3. Global Settings**
To register settings for centralized management:
```python
from common.config import registered_settings

registered_settings.append(setting)
```

---

### **4. Error Handling**
- `KeyError`: Raised if a requested configuration key does not exist.
- `TypeError`: Raised if a value's type does not match the defined type.
- `ValueError`: Raised if a value is out of defined bounds.

---

### **5. Logging**
Logs are used to report errors, missing keys, and directory/file creation:
- Use `logging` to view logs or troubleshoot issues.

---

This file simplifies managing, validating, and persisting configuration settings across your game modules.