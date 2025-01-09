### **Responsibilities and Usage of `graphics/common.py`**

The `graphics/common.py` file provides utility functions and classes for creating and styling reusable UI components in the game’s text-based user interface (TUI). It focuses on enhancing the usability and appearance of buttons, notifications, and general widgets by integrating with the **Urwid** library. These utilities serve as building blocks for other TUI components, ensuring consistent styling and functionality.

---

### **Core Responsibilities**

#### **1. Custom Button Implementation**
- **`CustomButton` Class**:
  - Extends the functionality of the `urwid.Button` class by adding customizable prefixes and suffixes to the button text.
  - Allows dynamic label updates via the `set_label` method.
  - Provides flexibility for buttons with additional visual elements.

#### **2. Notification System**
- **`notificationWidget` Class**:
  - Displays a simple notification with a message and an "OK" button.
  - Allows an optional callback function to execute after the notification is confirmed.
  - Uses an asynchronous event (`self.confirmed`) for synchronization.

- **`notify` Function**:
  - Simplifies the creation of `notificationWidget` instances.
  - Adds the notification to the TUI using `tui_main.add_frame`.

#### **3. Button Styling**
- **`buttonAttr` and `buttonAttr2`**:
  - Wrap buttons in `urwid.AttrMap` to apply consistent styles (`button` and `button2`) for normal and focused states.
  - Focus styling uses `reversed_button` or `reversed_button2` for visual differentiation.

#### **4. Widget Styling**
- **`niceFiller` Function**:
  - Creates a styled filler widget with centered alignment and a padded background.
  - Enhances the appearance of generic widgets by wrapping them in layered styling.

---

### **Key Components**

#### **1. `CustomButton` Class**
Customizable buttons with additional text elements:
- **Attributes**:
  - `prefix`: Text displayed before the button label.
  - `suffix`: Text displayed after the button label.
- **Methods**:
  - `set_label(label)`: Dynamically updates the button's label.

**Example**:
```python
btn = CustomButton("Start", prefix="[", suffix="]", on_press=callback)
btn.set_label("Resume")
```

**Appearance**:
```
[ Resume ]
```

---

#### **2. `notificationWidget` Class**
Creates a notification with a message and a confirmation button:
- **Attributes**:
  - `text`: Notification message.
  - `callback`: Function to execute after confirmation.
  - `confirmed`: An `asyncio.Event` triggered when the notification is confirmed.
- **Methods**:
  - `confirm(button)`: Handles confirmation and executes the callback.

**Example**:
```python
notif = notificationWidget("Game Saved!", callback=save_complete)
await notif.confirmed.wait()
```

---

#### **3. Utility Functions**
- **`notify(text)`**:
  - Creates and displays a `notificationWidget` using `tui_main.add_frame`.
  - Automatically removes the notification after confirmation.

- **`buttonAttr(button)` / `buttonAttr2(button)`**:
  - Styles buttons with predefined attributes for normal and focus states.

- **`niceFiller(widget)`**:
  - Applies centered alignment, padding, and a styled background to a widget.


This file serves as a utility hub for building and styling UI components, enabling consistent and visually appealing interactions in the game’s TUI. 