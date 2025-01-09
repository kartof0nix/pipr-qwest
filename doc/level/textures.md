### **Responsibilities and Usage of `level/textures.py`**

The `level/textures.py` file is responsible for rendering and managing the visual representation of levels and fields in the game's text-based UI. It focuses on generating, styling, and animating textures and items displayed in the TUI. By combining various components like fields, textures, and decorations, this module plays a central role in visually enhancing gameplay.

---

### **Core Responsibilities**

#### **1. Texture Rendering**
- The `texture` and `dynamicTexture` classes handle loading and rendering of textures.
- Supports resizing, sketching, and applying textures dynamically to fit the visual requirements of fields or animations.

#### **2. Animation and Movement**
- The `dynamicTexture` and `PlayerTexture` classes enable smooth movement animations using **asyncio**.
- Animations are handled through a queue system (`move_queue`) and are configurable using settings like `anim speed`.

#### **3. Field Visualization**
- The `itemSquare` and `itemSquareForest` classes render individual fields with paths, decorations, and themes.
- Fields are dynamically updated based on interactions or changes in the game state.

#### **4. Themes and Customization**
- Supports multiple visual themes, such as "forest" and "default," through the `squareThemes` dictionary.
- Enables dynamic switching between themes using the `current_itemSquare` function.

---

### **Key Components**

#### **1. `item` Base Class**
- Defines the base functionality for rendering items on a grid.
- **Methods**:
  - **`sketch(item_size)`**: Creates a transparent grid with a specific size.
  - **`apply(offset, item_size, char, style)`**: Applies the rendered item onto the game canvas at a given offset.

---

#### **2. `texture` Class**
- Represents a static texture loaded from a JSON file.
- **Key Features**:
  - Supports multi-size textures, selecting the best match based on the item size.
  - Applies textures with proper alignment to the center of the canvas.
- **Example Usage**:
  ```python
  tex = texture("tree.json")
  tex.apply((x, y), (width, height), char, style)
  ```

---

#### **3. `dynamicTexture` Class**
- Extends `texture` to support animated movement.
- **Key Features**:
  - Uses an asyncio task (`move_loop`) to manage animations.
  - Supports resizing and smooth transitions between positions.
- **Methods**:
  - **`move_anim(target_offset)`**: Queues an animation to a target position.
  - **`move_instant(target_offset)`**: Instantly moves the texture to a target position.
  - **`apply_anim(char, style)`**: Applies the texture with its current animated position.

---

#### **4. `PlayerTexture` Class**
- A specialized `dynamicTexture` representing the player's visual presence on the grid.
- **Key Features**:
  - Automatically adjusts size and position based on the level and field configuration.
  - Smoothly animates the player’s movement between fields.
- **Example Usage**:
  ```python
  player_tex = PlayerTexture(current_level)
  player_tex.update(grid_size, instant=False)
  ```

---

#### **5. `itemSquare` Class**
- Visualizes individual fields on the level grid.
- **Key Features**:
  - Displays paths between connected fields and decorations.
  - Supports dynamic updates based on field properties like `blocked` or `neighbours`.
- **Methods**:
  - **`update()`**: Updates the field's visualization based on its current state.
  - **`sketch(item_size)`**: Renders the field with decorations and paths.

---

#### **6. Themes and Decorations**
- **Themes**:
  - Themes like "forest" and "default" are handled by specialized classes (`itemSquare`, `itemSquareForest`).
- **Decorations**:
  - Decorations like "tree" are dynamically applied using the `texture` class.

**Example Theme Switching**:
```python
squareThemes = {
    "default": itemSquare,
    "forest": itemSquareForest
}

current_theme = squareThemes[cfg["theme"]]
```

---
