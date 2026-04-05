# OpenModelica Model Simulator - Code Documentation

## Overview

A simple PyQt6-based GUI application that execute OpenModelica simulation models with configurable start and stop times. The application is designed to be **beginner-friendly** with clear, understandable code structure.

---

## Project Structure

```
IITB_Project/
├── src/
│   └── app.py                        (Main GUI application)
├── model/
│   ├── TwoConnectedTanks.exe         (Compiled OpenModelica model)
│   ├── TwoConnectedTanks.bat         (Batch wrapper for execution)
│   └── TwoConnectedTanks_init.xml    (Model initialization config)
├── launcher.py                       (Splash screen launcher)
├── launcher.bat                      (Windows batch launcher)
├── run.bat                           (Setup and run script)
├── requirements.txt                  (Python dependencies)
└── README.md                         (This file)
```

---

## Core Architecture

### Application Flow Diagram

```
User Launches Application
        ↓
launcher.bat (optional splash screen)
        ↓
src/app.py (Main GUI Window)
        ↓
User enters: Executable path, Start time, Stop time
        ↓
User clicks START button
        ↓
WorkerThread spawned (background execution)
        ↓
Batch file runs OpenModelica .exe
        ↓
Output captured and displayed in real-time
        ↓
Simulation completes / User clicks STOP
        ↓
Thread finishes, buttons re-enabled
```

---

## Main Components

### 1. `src/app.py` (Main Application - ~200 lines)

The core GUI application with two main classes:

#### **Class: `WorkerThread`** (Lines 16-60)
Runs the simulation in a background thread to prevent GUI freezing.

```
WorkerThread (QThread) - Inherits from Qt's QThread
├── __init__(bat_file, exe_path, start_time, stop_time)
│   └── Store parameters for execution
├── Signals:
│   ├── output (pyqtSignal) - Emits text output as it happens
│   └── finished (pyqtSignal) - Emitted when done
└── run() - Execution method (called by Qt automatically)
    ├── Validate inputs
    ├── Build command line: [batch_file, -startTime=X, -stopTime=Y]
    ├── Emit start message
    ├── Execute via subprocess.Popen()
    ├── Capture stdout/stderr in real-time
    ├── Emit output to main thread
    └── Emit finished when complete
```

**Key Concept:** Signals are used to communicate back to the main GUI thread safely in a multi-threaded application.

#### **Class: `SimpleSimulator`** (Lines 63-200)
Main GUI window that displays controls and output.

```
SimpleSimulator (QMainWindow) - Inherits from Qt's Main Window class
├── __init__()
│   ├── Store reference to worker thread
│   └── Call init_ui()
├── init_ui() - Build all UI elements
│   ├── Create window title and size
│   ├── Executable input field + Browse button
│   ├── Start time input (DSpinBox)
│   ├── Stop time input (DSpinBox)
│   ├── START button (green, enabled)
│   ├── STOP button (red, disabled initially)
│   ├── Output text area (read-only log)
│   └── Status label
├── get_default_exe() - Get TwoConnectedTanks.exe path
├── browse_exe() - File dialog for executable selection
├── run_simulation()
│   ├── Get user inputs
│   ├── Validate paths and times
│   ├── Find batch file (.bat in same dir as .exe)
│   ├── Disable START, enable STOP
│   ├── Clear output area
│   ├── Create WorkerThread with parameters
│   ├── Connect signals to slots
│   └── Start thread
├── stop_simulation() - Terminate running process
├── append_output(text) - Add text to output area and scroll
└── on_finished() - Re-enable buttons when done
```

---

## Detailed Code Explanation

### Entry Point: `main()` Function (Lines 193-200)

```python
def main():
    app = QApplication(sys.argv)      # Create Qt application
    window = SimpleSimulator()          # Create main window
    window.show()                       # Display window
    sys.exit(app.exec())               # Start event loop
```

This follows the standard PyQt6 pattern:
1. Create QApplication (must be first)
2. Create main window
3. Show window
4. Run event loop until user closes

### Signal-Slot Mechanism

The application uses **signals** and **slots** for communication:

```python
# In WorkerThread.run():
self.output.emit("Starting simulation...\n")  # Send message to main thread

# In SimpleSimulator.run_simulation():
self.worker.output.connect(self.append_output)  # Connect signal to slot
self.worker.finished.connect(self.on_finished)  # Another connection
```

**Why?** Qt requires thread-safe communication. Signals let the worker thread safely send data to the GUI thread.

### Input Validation

```python
# In run_simulation():
if not exe_path:                               # Check executable entered
    QMessageBox.warning(self, "Error", ...)
    return

if start_time >= stop_time:                    # Check valid time range
    QMessageBox.warning(self, "Error", ...)
    return

if not exe_path.exists():                      # Check file exists
    QMessageBox.warning(self, "Error", ...)
    return
```

### Subprocess Execution

```python
# In WorkerThread.run():
self.process = subprocess.Popen(
    cmd,                              # ["batch.bat", "-startTime=5.1", "-stopTime=100.0"]
    stdout=subprocess.PIPE,           # Capture output
    stderr=subprocess.PIPE,           # Capture errors
    text=True,                        # Text mode (not binary)
    cwd=work_dir                      # Working directory
)

stdout, stderr = self.process.communicate()   # Wait for completion
```

This runs the batch file and captures all output for display in the GUI.

---

## 2. `launcher.py` (Splash Screen - ~180 lines)

Optional launcher with a fancy splash screen.

```
SplashScreen (QDialog)
├── init_ui() - Create splash window
│   ├── Title: "OpenModelica"
│   ├── Subtitle: "Model Simulator"
│   ├── Description text
│   ├── LAUNCH button (white button on gradient)
│   └── Auto-launch countdown timer
├── on_timer() - Update countdown every second
│   └── Auto-launch when counter reaches 0
└── launch_app() - Start src/app.py in new process
    └── Use subprocess.Popen() to launch app.py
```

**Purpose:** Provides a professional entry point with 5-second countdown before launching main app.

---

## 3. Model Execution

### `model/TwoConnectedTanks.bat`

The batch file that actually runs the OpenModelica executable:

```batch
@echo off
REM Try to find OpenModelica bin directory
if exist "C:\OpenModelica\bin" (
    SET PATH=C:\OpenModelica\bin;%PATH%
) else if exist "D:\Harish Kumar\bin" (
    SET PATH=D:\Harish Kumar\bin;%PATH%
)

SET ERRORLEVEL=
CALL "%CD%/TwoConnectedTanks.exe" %*    REM Run executable with parameters
SET RESULT=%ERRORLEVEL%
EXIT /b %RESULT%
```

**Purpose:**
- Sets up environment (PATH for DLL files)
- Runs the compiled model with parameters
- Returns exit code to Python

### Parameter Passing

```python
# Python side:
cmd = ["TwoConnectedTanks.bat", "-startTime=5.1", "-stopTime=100.0"]

# Batch file side:
CALL "TwoConnectedTanks.exe" %*          REM %* passes all parameters
```

This allows Python to control simulation time range.

---

## Data Flow

### 1. User Interaction
```
User enters paths/times
        ↓
User clicks START
        ↓
Event handler: SimpluSimulator.execute_simulation()
```

### 2. Validation & Setup
```
Check executable exists
        ↓
Check start_time < stop_time
        ↓
Find batch file (.bat)
        ↓
Build command: ["batch.bat", "-startTime=X", "-stopTime=Y"]
```

### 3. Execution
```
Create WorkerThread(bat_file, exe_path, times)
        ↓
Connect signals and slots:
  - output signal → append_output method
  - finished signal → on_finished method
        ↓
Call worker.start() (Qt runs in background thread)
```

### 4. Output Display
```
WorkerThread.run() executes subprocess
        ↓
subprocess sends text to stdout/stderr
        ↓
WorkerThread.run() reads output
        ↓
Emit signal with text: self.output.emit(text)
        ↓
Main thread receives signal
        ↓
Slot executed: append_output(text)
        ↓
Text added to QTextEdit
```

---

## Key Design Patterns

### 1. **Threading Pattern**
- **Problem:** Long-running operations block GUI
- **Solution:** Use QThread to run operation in background
- **Implementation:** WorkerThread class inherits QThread

### 2. **Signal-Slot Pattern**
- **Problem:** Multi-threaded communication is dangerous
- **Solution:** Use Qt Signals/Slots for thread-safe communication
- **Implementation:** Worker emits signals, main window connects to slots

### 3. **Model-View Pattern**
- **Model:** The simulation executable
- **Controller:** WorkerThread
- **View:** SimpleSimulator GUI

### 4. **Validation Pattern**
- Check all inputs before execution
- Return early with error messages if invalid
- Prevents invalid states

---

## Class Hierarchy

```
QWidget (Qt base class)
    ↓
QMainWindow (Main application window)
    ↓
SimpleSimulator (Our GUI application)


QThread (Qt threading class)
    ↓
WorkerThread (Our background worker)


QDialog (Dialog window)
    ↓
SplashScreen (Optional launcher)
```

---

## Method Summary

### SimpleSimulator Methods

| Method | Purpose | Trigger |
|--------|---------|---------|
| `init_ui()` | Build GUI layout | Constructor |
| `get_default_exe()` | Find default executable path | `init_ui()` |
| `browse_exe()` | Open file dialog | Browse button |
| `run_simulation()` | Start simulation | START button |
| `stop_simulation()` | Terminate simulation | STOP button |
| `append_output()` | Add text to log | `worker.output` signal |
| `on_finished()` | Handle completion | `worker.finished` signal |

### WorkerThread Methods

| Method | Purpose | Runs In |
|--------|---------|---------|
| `__init__()` | Store parameters | Main thread |
| `run()` | Execute subprocess | Background thread |
| (Signals) | Communicate to main | Background → Main |

---

## Common Terms Explained

### **QApplication**
The top-level object that manages GUI application. Must be created first.

### **QMainWindow**
A window with menu bar, toolbars, status bar. Our SimpleSimulator inherits this.

### **Signal**
A message sent from one object to another (usually across threads).

### **Slot**
A method that receives a signal. Connected via `.connect()`.

### **QThread**
Allows code to run in parallel without blocking the main GUI thread.

### **subprocess.Popen()**
Python's way to launch external programs and capture their output.

### **.bat File**
Windows batch script - plain text file with commands executed in sequence.

---

## Configuration Files

### `requirements.txt`
```
PyQt6>=6.7.1
```
Only dependency: PyQt6 for GUI. Model executable is pre-compiled.

### `model/TwoConnectedTanks_init.xml`
OpenModelica initialization values. Not modified by Python - just ensures model simulation parameters are correct.

---

## Error Handling

### In Python
```python
try:
    # Execute simulation
    self.process = subprocess.Popen(...)
except Exception as e:
    self.output.emit(f"Error: {str(e)}")
```

### In Batch File
```batch
SET ERRORLEVEL=
CALL "TwoConnectedTanks.exe" %*
SET RESULT=%ERRORLEVEL%
EXIT /b %RESULT%
```

Exit codes indicate success/failure:
- **0** = Success
- **Non-zero** = Error occurred

---

## How to Extend/Modify

### Add a new input field:
1. In `init_ui()`, add QSpinBox or QLineEdit
2. Store in `self.new_input = ...`
3. In `run_simulation()`, read: `value = self.new_input.value()`
4. Pass to WorkerThread or use in command building

### Change button appearance:
In `init_ui()`, modify button creation:
```python
self.start_btn.setStyleSheet("background-color: blue;")
self.start_btn.setText("▶ CUSTOM TEXT")
```

### Add progress bar:
```python
self.progress_bar = QProgressBar()
main_layout.addWidget(self.progress_bar)
# In WorkerThread: self.progress_updated.emit(percentage)
```

### Change window title/size:
```python
# In init_ui():
self.setWindowTitle("New Title")
self.setGeometry(100, 100, new_width, new_height)
```

---

## Simplified Code - Why These Changes

**Original:** 500+ lines with complex styling, timers, progress calculations
**Simplified:** ~200 lines with focus on core functionality

**Removed:**
- ❌ Complex CSS styling (removed decorative button colors)
- ❌ Elapsed time timer (removed time tracking logic)
- ❌ Progress percentage calculation (simplified progress)
- ❌ Fancy error dialogs (simplified error handling)

**Kept:**
- ✅ Core GUI layout
- ✅ Executable selection
- ✅ Time inputs
- ✅ Threading (non-blocking execution)
- ✅ Output display
- ✅ Start/Stop buttons

---

## Summary

This is a **simple, clean** PyQt6 application that demonstrates:

1. **GUI Programming** - Creating windows, buttons, text areas
2. **Threading** - Running long tasks without freezing UI
3. **Signal-Slot Communication** - Safe multi-threaded messaging
4. **Subprocess Management** - Launching and capturing external programs
5. **Input Validation** - Checking user inputs before execution

All code is beginner-friendly and heavily commented for learning.

---

## Credits & Acknowledgments

### Development Team

**Original Development:**
- Initial application architecture and PyQt6 implementation with GitHub Copilot (~85% code generation)
- Professional UI/UX with styling and advanced features
- Complete error handling and logging system

**Code Simplification & Documentation (v2.0):**
- **Claude AI (Anthropic)** - Code refactoring from 500+ lines to ~200 lines
  - Removed unnecessary complexity while maintaining core functionality
  - Created comprehensive technical documentation
  - Fixed DLL error handling in batch file
  - Made code beginner-friendly with clear comments
  - Detailed architecture and design pattern explanations

### Technologies & Credits

- **PyQt6** - Python GUI framework
- **OpenModelica** - Simulation engine
- **GitHub Copilot** - Initial code generation (~85%)
- **Claude AI** - Code review, simplification, and documentation

### How This Version Differs

**Version 1.0 (Original):**
- 500+ lines of code
- Complex styling and decorative elements
- Advanced features (progress tracking, elapsed time, fancy buttons)
- Professional but harder to understand for beginners

**Version 2.0 (Simplified - Current):**
- ~200 lines of clean, readable code
- Focus on core functionality
- Beginner-friendly with extensive comments
- Comprehensive technical documentation
- Easier to modify and extend

---

**Version:** 2.0 (Simplified & Documented)
**Language:** Python 3.8+
**Framework:** PyQt6
**Model:** OpenModelica (TwoConnectedTanks.exe)
**Last Updated:** April 5, 2026
**Developed with:** GitHub Copilot + Claude AI (Anthropic)
