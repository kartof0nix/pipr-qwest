### **Responsibilities and Usage of `graphics/tui_main.py`**

The `graphics/tui_main.py` file is responsible for managing the game's text-based user interface (TUI) using the **Urwid** library. It provides a robust framework for creating, displaying, and managing various UI elements like frames, overlays, and widgets. This file serves as the central manager for all TUI-related tasks, allowing developers to easily integrate graphical elements into the game.

---

### **Core Responsibilities**

#### **1. Main TUI Management**
- The `MainView` class acts as the core UI manager, handling the stacking of overlays, managing widgets, and interacting with the Urwid event loop.
- Provides functionality to add, remove, and manipulate frames and overlays within the game's UI.

#### **2. Frame Management**
- Frames represent distinct UI components that can be added or removed dynamically during gameplay.
- Functions like `add_frame` and `rem_frame` allow easy creation and deletion of frames with options for alignment, size, and titles.

#### **3. Event Loop and Rendering**
- The `render` function initializes the Urwid main loop and integrates it with **asyncio** for asynchronous tasks.
- Allows the TUI to operate seamlessly alongside other game logic.

---

### **Key Components**

#### **1. `MainView` Class**
The `MainView` class provides the central placeholder for managing the TUI. Key features include:
- **Overlay Stacking**:
  - Handles overlays dynamically with methods like `push_top` and `pop_top`.
  - Supports nested overlays for modular and layered UI design.
- **Widget Manipulation**:
  - Allows setting and accessing the bottom and top widgets of the stack.
- **Custom Key Handling**:
  - Implements custom keypress behavior for interaction.

#### **3. Frame Management**
- **`add_frame`**:
  - Adds a new frame to the TUI with customizable width, height, alignment, title, and interaction blocking.
  - Supports both relative and absolute sizing for flexibility.
- **`rem_frame`**:
  - Removes the current top frame (overlay) from the TUI.

#### **4. Rendering and Event Loop**
- **`render(callback, exitFunction)`**:
  - Initializes the Urwid main loop and ties it to the asyncio event loop for handling asynchronous tasks.
  - Accepts a callback for further game execution and an `exitFunction` to handle cleanup when the game ends.

---

### **Usage Examples**

#### **1. Adding and Removing Frames**
Frames can be added dynamically during gameplay for events, dialogs, or menus:
```python
add_frame(
    urwid.Text("Welcome to the game!"),
    width=40,
    height=5,
    side="center",
    title="Greeting",
    block_move=True
)

# Remove the current top frame
rem_frame()
```

#### **2. Rendering the TUI**
Initialize the TUI and tie it to an asyncio callback:
```python
async def game_logic():
    await asyncio.sleep(1)
    add_frame(urwid.Text("Starting the game..."), width=30, height=5, side="center")
    await asyncio.sleep(2)
    rem_frame()

render(game_logic, exitFunction=lambda: print("Game exited"))
```

