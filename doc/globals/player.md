## **Module Description: `player.py`**

The `player.py` module manages player-specific data and functionality within the game, including player attributes, inventory management, and save system operations. It extends the configuration system to provide persistence for player data across sessions, allowing multiple save files.

---

### **Core Responsibilities**
1. **Player Data Management**
   - Handles player attributes such as health, armor, attack, and current level.
   - Supports inventory management with operations to add, check, and calculate the effects of items.

2. **Save System**
   - Allows for multiple saves, with utilities to list, load, and remove save files.
   - Saves are stored as JSON files in `~/.pipr-qwest/saves`.

3. **Inventory System**
   - Integrates a simple inventory mechanism to store items carried by the player.
   - Calculates the player's total attack and defense based on equipped items.

---

### **Structure**
- **`PlayerClass`**: Manages player-specific attributes and inventory, while handling save and load operations.
- **Utility Functions**:
  - `listSaves`: Lists all available save files.
  - `removeSave`: Deletes a specific save file.
  - `loadSave`: Loads a save file and initializes the `player` object.

---

### **Predefined Items**
The module includes a global dictionary of predefined items (`ITEMS`) for easy reference. Each item contains:
- `item_id`: A unique identifier for the item.
- `display_name`: The item's name for display purposes.
- `attack`: The item's attack value.
- `defense`: The item's defense value.

---

### **Key Features**
- Modular design for managing player data and saves.
- Simple inventory system for item storage and stat calculation.
- Persistent storage for player data in JSON format.

### **Example Usage**
```python
from globals.player import listSaves, loadSave, removeSave, PlayerClass

# List all saves
saves = listSaves()
print("Available saves:", saves)

# Load a save
loadSave("my_save")
print(player["health"])  # Access the player's health from the save

# Remove a save
removeSave("my_save")
```


This module serves as a central hub for handling player-related logic in the game, ensuring scalability and maintainability.