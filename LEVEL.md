# **Documentation: Defining level files**

This guide explains the structure and usage of `level.json` files in Pipr Qwest. These files define the layout, events, and gameplay elements of each level in the game.

The levels are stored in res/levels

---

## **Structure of a `level.json` File**

A `level.json` file typically includes the following sections:

1. **`name`**:  
   The name of the level file.
   ```json
   "name": "example_level.json"
   ```

2. **`grid`**:  
   A 2D array representing the layout of the level. Each number corresponds to a field in the level.
   ```json
   "grid": [
       [1, 2, 3],
       [4, 5, 6]
   ]
   ```

3. **`graph`**:  
   An array of pairs that define the connections between fields. Fields can only connect if they are adjacent in the grid.  
   Example: `[1, 2]` means field 1 connects to field 2.
   ```json
   "graph": [
       [1, 2], [2, 3],
       [4, 5], [5, 6],
       [2, 5]
   ]
   ```

4. **`startField`**:  
   The field where the player begins the level.
   ```json
   "startField": 1
   ```

5. **`fields`**:  
   A dictionary containing definitions for each field, including events, decorations, and obstacles.
   ```json
   "fields": {
       "1": {
           "eventOnEnter": "startDialogue",
           "decorations": ["tree"]
       },
       "2": {
           "eventOnInspect": "findKey"
       }
   }
   ```

6. **`events`**:  
   A list of events that can occur within the level, such as combat, item collection, or dialogue.
   ```json
   "events": [
       {
           "eventType": "ItemGiveEvent",
           "eventId": "findKey",
           "params": {
               "item_id": "golden_key"
           }
       },
       {
           "eventType": "ConversationEvent",
           "eventId": "startDialogue",
           "params": {
               "dialogue": [
                   ["guardian", "Welcome to the forest!"],
                   ["player", "What lies ahead?"],
                   ["guardian", "Find the golden key to proceed."]
               ]
           }
       }
   ]
   ```

---

## **Field Definition**

Each field in the `fields` dictionary can have the following properties:

### **1. `eventOnEnter`**
Triggers when the player enters the field.
```json
"eventOnEnter": "startDialogue"
```

### **2. `eventOnInspect`**
Triggers when the player inspects the field.
```json
"eventOnInspect": "findKey"
```

### **3. `eventOnLeave`**
Triggers when the player leaves the field.
```json
"eventOnLeave": "closeGate"
```

### **4. `decorations`**
An array of decorations (e.g., trees, rocks) that visually enhance the field.
```json
"decorations": ["tree", "boulder"]
```

### **5. `blocked`**
A boolean indicating whether the field is inaccessible.
```json
"blocked": true
```

---

## **Event Definition**

The `events` array defines all possible events for the level. Each event must include:
- **`eventType`**: The type of event (e.g., `CombatEvent`, `ItemGiveEvent`).  
- **`eventId`**: A unique identifier for the event.  
- **`params`**: Event-specific parameters.

### **Common Event Types**

#### **1. `ItemGiveEvent`**
Gives an item to the player.
```json
{
    "eventType": "ItemGiveEvent",
    "eventId": "findKey",
    "params": {
        "item_id": "golden_key"
    }
}
```

#### **2. `CombatEvent`**
Starts a combat encounter.
```json
{
    "eventType": "CombatEvent",
    "eventId": "batAttack",
    "params": {
        "opponentHealth": 15,
        "opponentAttack": 5,
        "opponentDefense": 2,
        "nextEvent": "afterBattle"
    }
}
```

#### **3. `ConversationEvent`**
Triggers a dialogue sequence.
```json
{
    "eventType": "ConversationEvent",
    "eventId": "startDialogue",
    "params": {
        "dialogue": [
            ["guardian", "Welcome to the forest!"],
            ["player", "What lies ahead?"]
        ]
    }
}
```

#### **4. `ChangeLevelEvent`**
Transitions to a new level.
```json
{
    "eventType": "ChangeLevelEvent",
    "eventId": "exitLevel",
    "params": {
        "nextLevel": "castle.json",
        "nextField": 1
    }
}
```

---

## **Example `level.json` File**

```json
{
    "name": "forest_level.json",
    "grid": [
        [1, 2, 3],
        [4, 5, 6]
    ],
    "graph": [
        [1, 2], [2, 3],
        [4, 5], [5, 6],
        [2, 5]
    ],
    "startField": 1,
    "fields": {
        "1": {
            "eventOnEnter": "startDialogue",
            "decorations": ["tree"]
        },
        "2": {
            "eventOnInspect": "findKey"
        },
        "3": {
            "blocked": true
        }
    },
    "events": [
        {
            "eventType": "ConversationEvent",
            "eventId": "startDialogue",
            "params": {
                "dialogue": [
                    ["guardian", "Welcome to the forest!"],
                    ["player", "What lies ahead?"],
                    ["guardian", "Find the golden key to proceed."]
                ]
            }
        },
        {
            "eventType": "ItemGiveEvent",
            "eventId": "findKey",
            "params": {
                "item_id": "golden_key"
            }
        }
    ]
}
```

---

## **Best Practices**

1. **Ensure Adjacency in the `graph` Section**:
   - Fields can only connect if they are adjacent in the grid.

2. **Unique Event IDs**:
   - Each event must have a unique `eventId`.

3. **Avoid Unreachable Fields**:
   - Ensure all fields in the grid are accessible through the `graph`.

4. **Test Field Events**:
   - Verify that all events are properly linked and trigger as expected during gameplay.

