### **Responsibilities and Usage of `overlay.py`**

The `overlay.py` file provides a dynamic and interactive overlay widget for displaying the player's stats (health, attack, and defense) in the game's text-based UI. This overlay is updated in real time as game events occur, ensuring that the player has immediate feedback about changes to their attributes.

---

### **Core Responsibilities**

#### **1. Dynamic Stat Display**
- The overlay dynamically updates to reflect the player's current health, attack, and defense.
- This ensures that the player always sees the latest stats during gameplay.

#### **2. Event-Driven Updates**
- The widget listens for specific game events (`event_end` and `event_change`) using the event queue.
- When triggered, the overlay refreshes its content to show updated player stats.

#### **3. Integration with Game Loop**
- Seamlessly integrates with the game's event system via `event_queue.registerHandler`, ensuring real-time updates without manual intervention.

---

### **Key Components**

#### **1. `overlayWidget` Class**
- Extends `urwid.Pile` to create a vertically stacked widget displaying player stats.
- **Attributes**:
  - `widgetList`: A list of `urwid.Text` widgets representing health, attack, and defense stats.
- **Methods**:
  - **`update()`**: Updates the widget with the current values of the player's stats.
  - **`eventHandler(params)`**: Handles events to refresh the overlay when triggered.
  - **`__del__()`**: Ensures event handlers are unregistered when the widget is destroyed.
  - **`render(size, focus)`**: Overrides the render method to trigger an update before displaying the widget.


### **Example Integration**

1. **Adding the Overlay to the TUI**:
   ```python
   from src.graphics.overlay import overlayWidget
   from src.graphics.tui_main import add_frame

   overlay = overlayWidget()
   add_frame(overlay, width=20, height=5, side="right", title="Player Stats")
   ```

2. **Real-Time Stat Updates**:
   - During gameplay, when an event like `event_change` occurs, the overlay automatically updates the player's displayed stats.

3. **Removing the Overlay**:
   - When the overlay is no longer needed, remove it from the TUI and unregister handlers:
     ```python
     rem_frame()
     del overlay
     ```
