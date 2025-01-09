### **Responsibilities and Usage of `graphics/pauseMenu.py`**

The `pauseMenu.py` file implements a **pause menu** for the game, allowing players to perform various actions while pausing gameplay. It provides functionality to save progress, exit the game, and unpause to resume gameplay. This file is critical for managing mid-session interactions in a text-based game environment.

---

### **Core Responsibilities**

#### **1. Pause Menu Implementation**
- Provides a visually styled pause menu using the **Urwid** library.
- Implements buttons for key actions such as saving, exiting, and unpausing the game.

#### **2. Game State Management**
- Enables saving the player's current progress (e.g., player data and field attributes).
- Sends specific events (like "gameover") to the event queue for terminating the game.

#### **3. Unpause Functionality**
- Allows the player to return to the game by removing the pause menu frame from the TUI stack.


---

### **Example Usage in Gameplay**

1. **Display the Pause Menu**:
   ```python
   from src.graphics.tui_main import add_frame
   from src.graphics.pauseMenu import PauseMenu

   # Add pause menu frame
   pause_menu = PauseMenu()
   add_frame(pause_menu, width=30, height=10, side="center", title="Paused")
   ```

2. **Save Progress**:
   - When the player selects "Save Game," the `saveGame` function saves progress and displays a notification.

3. **Unpause Gameplay**:
   - The player can unpause by pressing the `Unpause` button or the `esc` key.

---

