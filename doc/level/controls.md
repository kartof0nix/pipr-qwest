### **Responsibilities and Usage of `controls.py`**

The `controls.py` file is responsible for processing player input and delegating actions to the game's level logic. It maps user inputs (like directional keys and interaction commands) to appropriate functions within the `Level` class, allowing seamless interaction with the game's environment.

---

### **Core Responsibilities**

#### **1. Input Handling**
- The `Control` class processes keypress inputs and determines the corresponding action:
  - Movement (up, down, left, right).
  - Inspecting the current field.
  - Exiting the game.

#### **2. Delegation to Level Logic**
- All player actions are forwarded to the `Level` object, ensuring a clean separation of concerns:
  - Movement keys call `Level.move()`.
  - The inspect key (`i`) calls `Level.inspect()`.

#### **3. Event Management**
- Sends game-ending events (`gameover`) to the event queue when the escape key (`esc`) is pressed.
