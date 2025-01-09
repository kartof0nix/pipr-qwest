The `level/game.py` file is responsible for defining and managing game levels and their associated fields. It provides the functionality to create, load, and manipulate levels, enabling player navigation and interaction with the game world.

---

### **Key Responsibilities**
1. **Level and Field Management**
   - The `Field` class represents individual game areas with properties, events, and neighbors.
   - The `Level` class defines a complete level, consisting of multiple fields, connections (graph), and an optional grid layout.

2. **Event Integration**
   - Fields can trigger events when entered, inspected, or exited.
   - Levels can initialize and link events using the global event system.

3. **Player Interaction**
   - Enables movement within levels, checking for blocked fields and triggering events.
   - Allows inspection of the current field and tracks the player’s position.

4. **Persistence and Configuration**
   - Fields and levels are saved and loaded using the `Config` system for persistence and reusability.
   - Supports loading level configurations from files in the `res/levels/` directory.

---

### **Key Components**

#### **1. `Field` Class**
Represents an individual area or location in the game.

- **Properties**:
  - `num`: Unique field identifier.
  - `eventOnEnter`, `eventOnInspect`, `eventOnLeave`: Events triggered by interactions.
  - `neighbours`: Connections to adjacent fields.
  - `decorations`, `obstacles`, `blocked`: Visual and logical attributes of the field.

- **Methods**:
  - **`enter()`**: Triggers the "enter" event for the field.
  - **`exit()`**: Triggers the "exit" event and cancels pending tasks.
  - **`inspect()`**: Triggers the "inspect" event for the field.
  - **`move(direction: str)`**: Moves to a neighboring field if allowed.

---

#### **2. `Level` Class**
Represents a game level with multiple interconnected fields.

- **Properties**:
  - `name`: Name of the level.
  - `fields`: Dictionary of all fields in the level.
  - `graph`: List of connections between fields.
  - `grid`: 2D layout of fields (TODO : optional).
  - `startField`: Field where the level starts.

- **Methods**:
  - **`move(direction: str)`**: Moves the player in the specified direction.
  - **`start()`**: Begins the level by entering the starting field.
  - **`inspect()`**: Inspects the current field.
  - **`getField(i, j)`**: Retrieves a field from grid coordinates.
  - **`exit()`**: Cleans up all fields in the level.

- **Example**:
  ```python
  level = Level(name="Main", fieldsInit={1: {}, 2: {}}, startField=1, graph=[(1, 2)], grid=[[1, 2]])
  level.start()
  level.move("right")
  level.exit()
  ```

---

#### **3. Level Loading**
The `loadLevel` function loads a level from a configuration file.

- **Parameters**:
  - `filename`: Name of the level file in the `res/levels/` directory.
  - `startField`: Optional starting field override.

- **Example**:
  ```python
  level = loadLevel("level1.json")
  ```
