The manager.py file is responsible for managing the lifecycle and transitions between game levels. It acts as the central controller for loading, running, and switching levels, ensuring smooth transitions and maintaining the integrity of the player's progress.

### Core Responsibilities
#### 1. Level Lifecycle Management

    Handles initialization, execution, and cleanup of levels using the `LevelManagerClass`.
    Manages the active level and its associated resources.

#### 2. Level Transition

    Facilitates seamless transitions between levels via the `changeLevel` method.
    Listens for level-related events (e.g., `event_end`, `gameover`) to trigger transitions or exit gameplay.

#### 3. Level Listing

    Provides a utility to list all available levels stored in the game's directory.

#### 4. Error Handling and Logging

    Captures errors during level loading or execution and logs detailed information for debugging.