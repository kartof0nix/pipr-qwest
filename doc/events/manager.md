The `manager.py` file is responsible for managing the execution of game events. It acts as a centralized controller to handle event logic, including integrating TUIs (Text User Interfaces) when applicable. Here's a breakdown of its functionality:

---

### **Responsibilities**
1. **Event Execution**
   - Executes individual events using `runEvent`.
   - Checks for a corresponding TUI for the event and invokes it if available.

2. **Event Chaining**
   - Uses `launchEvents` to execute a chain of events, where each event determines the next event to be executed.

---

### **Functions**

#### **1. `runEvent(eventId: str) -> str`**
Executes a single event identified by `eventId`.
- **Example**:
  ```python
  result = await runEvent("event_1")
  print(f"Next event: {result}")
  ```

#### **2. `launchEvents(eventId: str)`**
Launches a series of events starting from the given `eventId`.


- **Error Handling**:
  - Logs an error if any event in the chain fails.
  - Captures and logs the stack trace for debugging.

- **Example**:
  ```python
  await launchEvents("start_event")
  ```

