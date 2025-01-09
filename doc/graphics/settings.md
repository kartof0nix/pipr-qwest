### **Responsibilities and Usage of `graphics/settings.py`**

The `graphics/settings.py` file provides a user interface for managing and editing game settings. It allows players to adjust configurable parameters dynamically during gameplay using a text-based UI powered by **Urwid**. The file focuses on providing a clean, interactive way to update settings like selectable options or numerical ranges, ensuring that changes are persisted across game sessions.

---

### **Core Responsibilities**

#### **1. Settings Management**
- Facilitates the display and modification of game settings stored in `Setting` objects.
- Supports selectable options and value ranges using specialized widgets (`SelectBox` and `ValueBox`).

#### **2. Dynamic Configuration**
- Dynamically creates UI elements based on the constraints (`value_type`) defined for each setting:
  - **Selectable Settings**: Represented as a dropdown-style `SelectBox`.
  - **Bounded Settings**: Represented as an adjustable numerical `ValueBox`.

#### **3. Persistence**
- Changes made in the settings menu are saved to the corresponding configuration files using the `Setting.save_to_file()` method.

#### **4. User Interaction**
- Provides interactive navigation, with buttons for applying changes, closing the menu, and adjusting individual settings using keypress events.

---

### **Key Components**

#### **1. SelectBox**
- A widget for displaying and navigating through a list of selectable options.
- **Methods**:
  - **`increment()` / `decrement()`**: Navigate forward or backward through the list.
  - **`get_value()`**: Retrieve the currently selected value.

**Example Usage**:
```python
box = SelectBox(["Option1", "Option2", "Option3"], current="Option1")
```
**Key Features**:
- Allows easy navigation using arrow keys (`left`/`right`).
- Displays the currently selected value.

---

#### **2. ValueBox**
- A widget for adjusting numerical values within a bounded range.
- **Methods**:
  - **`increment()` / `decrement()`**: Increase or decrease the current value.
  - **`get_value()`**: Retrieve the current value.

**Example Usage**:
```python
box = ValueBox(min_val=1, max_val=100, current=50)
```
**Key Features**:
- Supports both integer and floating-point values.
- Automatically adjusts the step size based on the range.

---

#### **3. SettingsItem**
- Represents an individual setting in the menu, combining a label and a configurable widget (e.g., `SelectBox` or `ValueBox`).
- **Constructor**:
  - `item`: The name of the setting.
  - `widget`: The widget used to adjust the setting.
  - `title`: An optional custom label.

**Example Usage**:
```python
item = SettingsItem("graphics_quality", SelectBox(["Low", "Medium", "High"]))
```

---

#### **4. SettingsView**
- The main UI for displaying and managing all settings.
- Dynamically generates pages for each `Setting` object, displaying configurable items as `SettingsItem` widgets.
- **Key Methods**:
  - **`apply(button)`**: Applies changes to the settings and saves them to the file.
  - **`exit(button)`**: Closes the settings menu.
  - **`subpage(setting)`**: Creates a subpage for a specific `Setting` object, including all its configurable items.

**Example Usage**:
```python
settings = SettingsView([graphics_setting, audio_setting])
```

---

#### **5. `launchSettings()`**
- An asynchronous function that launches the settings menu as an overlay in the TUI.
- **Steps**:
  1. Saves the current TUI state.
  2. Displays the `SettingsView` overlay.
  3. Waits for the user to close the settings menu.
  4. Restores the previous TUI state.

**Example Usage**:
```python
await launchSettings()
```
