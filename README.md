
# Pipr Qwest

Pipr Qwest is a dynamic, text-based RPG game that combines strategic decision-making, exploration, and storytelling. Navigate through levels, engage in events, and manage your player’s stats and inventory, all through an intuitive text-based user interface (TUI).

---

## **Installation**


### Prequisites
This project can only run on Linux / Mac.
To run this project python>=3.12 needs to be installed.
If you wish to run on windows, use WSL.

Follow these steps to install and run the game:

1. **Download the Source Code**  
   Clone or download the source code from the repository.

2. **Create a Python Virtual Environment**  
   ```bash
   python3 -m venv pipr-qwest-env
   ```

3. **Install Dependencies**  
   Activate the virtual environment and install all required libraries using:
   ```bash
   pip install -r requirements.txt
   ```

4. **Activate the Virtual Environment**  
   - On Linux/Mac:
     ```bash
     source pipr-qwest-env/bin/activate
     ```
5. **Run the Game**  
   Launch the game by running the `src` module:
   ```bash
   python3 -m src
   ```

---

## **Game Features**

- **Text-Based Adventure**: Explore dynamic levels, inspect fields, and interact with events through an engaging TUI.  
- **Player Management**: Keep track of your health, attack, defense, and inventory.  
- **Event-Driven Gameplay**: Encounter various events like combat, conversations, and puzzles.  
- **Save and Load**: Save your player stats, inventory, and current level progress.  

---

## **How to Play**

### **Controls**  
- **Arrow Keys**: Move between fields.  
- **`i` Button**: Inspect the current field for items or hidden features.  
- **`esc` Button**: Open the pause menu.  

### **Pause Menu Options**  
- **Save Game**: Save your player stats, inventory, and current level progress.  
  _(Note: Current field state is not saved.)_  
- **Save and Exit**: Save your progress and exit the game.  
- **Exit Without Saving**: Exit without saving progress.  
- **Unpause**: Return to the game.

---

## **File Storage**

### **Configuration and Settings**
All settings and configuration files are stored in the `~/.pipr-qwest` folder for easy access and management through the TUI.  

### **Game Logs**  
Debugging information and error logs are written to `qwest.log` in the source code folder.

---

## **Documentation**

Detailed documentation is available in the `doc` folder of the repository. It includes descriptions of the game’s structure, classes, and functionality.

---

## **Contributing**

If you encounter any issues, please create an Issue in the GitHub repository. Contributions are welcome! Submit a pull request with your improvements or feature suggestions.

---

## **License**

This project is open-source. Please refer to the `LICENSE` file in the repository for details.

---

## Creating levels
You may define custom levels in .json files. Refer to (this guide)[/LEVEL.md]

## Modding
Simple modding is supported via adding files to the 'mod' folder. Currently it is impossible to overrite the behaviour of the game, but you may add your own:

### GameEvents and GameEventTUI - [documentation](/doc/events/game.md)
You can achieve this by inhereting from the GameEvent and GameEvent TUI classes. The newly defined Events should become available in the level.json file.
See the mod/example.py file.

### Act upon game events
By registering a listener to the [event queue](/doc/common/event_queue.md) you can act upon various events in the game. The newly launched functions are asynchronous, so you may use this to 'launch' your modpack to add new functionality.
