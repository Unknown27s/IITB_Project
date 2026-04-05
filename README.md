# OpenModelica Model Simulator - Complete Documentation

A professional PyQt6-based GUI application for executing OpenModelica simulation models with configurable start and stop times. Designed with both **beginner-friendly code structure** and **production-quality error handling**.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture & Design](#architecture--design)
- [Code Quality](#code-quality)
- [Building Standalone Executable](#-building-standalone-executable)
- [Troubleshooting](#-troubleshooting)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (3.10+ recommended)
- **Windows**, Linux, or macOS
- **PyQt6** (installed automatically)

### Installation (2 minutes)

```bash
# Clone or download the project
cd IITB_Project

# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

### First Simulation

1. **Launch the app**: `python src/app.py`
2. **Select executable**: Click "Browse" → choose `model/TwoConnectedTanks.exe`
3. **Set times**: 
   - Start Time: `0.0` seconds
   - Stop Time: `100.0` seconds
4. **Click "START SIMULATION"**
5. **View results** in the output log

---

## ✨ Features

### Core Functionality
- ✅ **GUI-Based Execution**: No command-line knowledge required
- ✅ **Configurable Time Parameters**: Set start/stop times with decimal precision
- ✅ **Real-Time Output**: View simulation results as they happen
- ✅ **Non-Blocking UI**: Multi-threaded execution prevents UI freezing
- ✅ **File Browser**: Easy executable selection with system file dialog
- ✅ **Error Handling**: Comprehensive error messages with recovery suggestions

### Code Quality Features
- ✅ **Type Hints**: Full Python type annotations (PEP 484)
- ✅ **PEP 8 Compliant**: Professional code formatting
- ✅ **Configuration Management**: Centralized settings via `config.py`
- ✅ **Logging**: Built-in debugging and error tracking
- ✅ **Comprehensive Docstrings**: Every function documented
- ✅ **OOP Design Patterns**: Clear separation of concerns

---

## 📁 Project Structure

```
IITB_Project/
├── .venv/                          # Python virtual environment
├── src/
│   ├── app.py                      # Main GUI application (~450 lines, fully typed)
│   ├── config.py                   # Configuration management class
│   └── __init__.py                 # Python package marker
├── model/
│   ├── TwoConnectedTanks.exe       # Compiled OpenModelica model
│   ├── TwoConnectedTanks.bat       # Windows batch wrapper
│   ├── TwoConnectedTanks_init.xml  # Model initialization config
│   └── TwoConnectedTanks_info.json # Model metadata
├── launcher.py                     # Optional splash screen launcher
├── launcher.bat                    # Windows launcher script
├── run.bat                         # Setup and run script (Windows)
├── run.sh                          # Setup and run script (Unix)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── SUBMISSION.py                   # Project metadata generator
```

### Key Files Explained

| File | Purpose | Size |
|------|---------|------|
| `src/app.py` | Main GUI application with threading | ~450 lines |
| `src/config.py` | Configuration constants and validation | ~200 lines |
| `launcher.py` | Splash screen (optional entry point) | ~250 lines |
| `requirements.txt` | Package dependencies | 1 line |

---

## 💾 Installation

### Option 1: Windows (Recommended)
```bash
# Run the setup script
run.bat
```
This automatically:
- Creates virtual environment
- Installs dependencies
- Launches the application

### Option 2: Manual Installation

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Option 3: Docker (if configured)
```bash
# Future enhancement - currently uses native environment
```

---

## 📖 Usage Guide

### Basic Usage

```bash
# Method 1: Direct launch
python src/app.py

# Method 2: With splash screen
python launcher.py

# Method 3: Windows batch
launcher.bat
```

### Command-Line Alternative

For script automation, you can run the model directly:
```bash
cd model
TwoConnectedTanks.bat -startTime=0 -stopTime=100
```

### GUI Walkthrough

#### Main Window Components

1. **Executable Path Section**
   - Text field shows selected executable
   - "Browse" button opens file selection dialog
   - Validates file exists before execution

2. **Time Configuration**
   - **Start Time**: Simulation begins at this point (seconds)
   - **Stop Time**: Simulation ends at this point (seconds)
   - Both support decimal values (e.g., 5.5, 10.25)
   - Validation: Start Time must be < Stop Time

3. **Control Buttons**
   - **START**: Begins simulation in background thread
   - **STOP**: Terminates running simulation
   - Buttons intelligently enable/disable based on state

4. **Output Log**
   - Real-time simulation output display
   - Monospace font for readable formatting
   - Auto-scrolls to show latest output
   - Distinguishes normal output from errors

5. **Status Indicator**
   - Shows current application state
   - Color-coded: Green (ready), Blue (running), Green (done)

### Example Scenarios

#### Scenario 1: Simple 100-Second Simulation
```
1. Select: model/TwoConnectedTanks.exe
2. Set Start Time: 0
3. Set Stop Time: 100
4. Click START
5. Wait for "✓ Simulation completed successfully!" message
```

#### Scenario 2: Partial Simulation (Skip Initial Transient)
```
1. Select executable
2. Set Start Time: 10     (Skip first 10 seconds)
3. Set Stop Time: 50      (Run for 40 seconds)
4. Click START
```

#### Scenario 3: Stopping Early
```
1. Start simulation as normal
2. Wait a few seconds
3. Click STOP button
4. See "[Stopping...]" message
5. Process terminates gracefully
```

---

## 🏗️ Architecture & Design

### MVC Architecture

The application follows Model-View-Controller principles:

- **Model**: `WorkerThread` (simulation execution logic)
- **View**: `SimpleSimulator` (PyQt6 GUI components)
- **Controller**: Signal/slot connections (Qt's event system)

### Threading Model

```
Main UI Thread (never blocks)
└── WorkerThread (background execution)
    ├── Spawns subprocess (OpenModelica .exe)
    ├── Captures stdout/stderr
    └── Emits signals to main thread
```

This ensures **responsive UI** during long simulations.

### Configuration Management

All hardcoded values are centralized in `src/config.py`:

```python
from src.config import SimulatorConfig

config = SimulatorConfig()
print(config.WINDOW_WIDTH)        # 700
print(config.DEFAULT_START_TIME)  # 5.1
```

Benefits:
- ✅ Easy customization without code changes
- ✅ Type-safe configuration
- ✅ Input validation methods included
- ✅ Scalable to file-based configuration

### Signal/Slot Communication

Qt uses signals and slots for thread-safe communication:

```python
# From WorkerThread
self.output.emit(text)      # Send to main thread
self.finished.emit()         # Notify completion

# In MainWindow
self.worker.output.connect(self.append_output)
self.worker.finished.connect(self.on_simulation_finished)
```

---

## 🎯 Code Quality

### Type Hints (PEP 484)

Every function has type annotations:

```python
def run_simulation(self) -> None:
    """Execute simulation with validated parameters."""
    exe_path = self.exe_input.text().strip()
    start_time: float = self.start_input.value()
    stop_time: float = self.stop_input.value()
```

### PEP 8 Compliance

- ✅ 4-space indentation
- ✅ Line length ≤ 100 characters
- ✅ Proper import organization
- ✅ Naming conventions followed

### Docstring Coverage

Every class and method includes:
- **Description**: Purpose of the code
- **Args**: Parameter documentation with types
- **Returns**: Return type and meaning
- **Raises**: Exceptions that can be raised
- **Examples**: Usage examples where applicable

### Error Handling

```python
try:
    # Execute simulation
    self.process = subprocess.Popen(...)
    
except FileNotFoundError as e:
    self.output.emit(f"⚠️  File not found: {e}")
    
except PermissionError as e:
    self.output.emit(f"⚠️  Permission denied: {e}")
    
except Exception as e:
    self.output.emit(f"⚠️  Unexpected error: {e}")
```

### Logging

Debug issues easily with built-in logging:

```python
python src/app.py 2>&1 | grep "ERROR"    # See errors
python src/app.py 2>&1 | grep "INFO"     # See operations
```

---

## � Building Standalone Executable

Convert the application to a standalone `.exe` that doesn't require Python installation.

### Requirements
- Python 3.8+ (must be in PATH)
- Dependencies installed: `pip install -r requirements.txt`
- Virtual environment activated: `.venv\Scripts\activate.bat`

### Build Steps

#### Option 1: Automated Build (Recommended)
```bash
cd IITB_Project
build_exe.bat
```

This automatically:
1. Kills any running instances of the previous exe
2. Creates virtual environment (if needed)
3. Installs all dependencies
4. Installs PyInstaller
5. Builds the executable directly from `src/app.py`
6. Verifies the result

**Output**: `dist/OpenModelica Simulator.exe` (~100-150 MB, no Python needed)

#### Option 2: Manual Build
```bash
# Activate environment
.venv\Scripts\activate.bat

# Install PyInstaller
pip install pyinstaller

# Build directly from app.py
pyinstaller --onefile --windowed --name "OpenModelica Simulator" ^
    --add-data "src;src" --add-data "model;model" ^
    --hidden-import=PyQt6 src/app.py
```

### Running the Built Executable

```bash
# Method 1: Double-click from File Explorer
dist/OpenModelica Simulator.exe

# Method 2: From command line
"dist/OpenModelica Simulator.exe"

# Method 3: Create desktop shortcut
Right-click exe → Send to → Desktop (create shortcut)
```

### First Launch

The first time you run the bundled exe:
- Extracts bundled files to temporary directory
- Takes 3-5 seconds longer than subsequent runs
- Shows the main GUI application directly

### Single Executable vs Source Code

| Aspect | Source Code | Built Exe |
|--------|----------|-----------|
| **Python Installation** | Required | Not needed |
| **Startup Time** | Fast ~1 sec | ~3-5 sec (first launch) |
| **Modifying Code** | Easy | Requires rebuild |
| **Distribution** | Harder | Easier (single file) |
| **File Size** | ~50 KB code | ~100-150 MB exe |
| **Model Configuration** | In model/ folder | Editable |

### Build Troubleshooting

**Issue**: "PermissionError: Access is denied" during build
```bash
# Solution: Kill running exe and rebuild
taskkill /IM "OpenModelica Simulator.exe" /F
build_exe.bat
```

**Issue**: "Module not found" or "PyQt6 import error"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
pip install --upgrade pyinstaller PyQt6
build_exe.bat
```

**Issue**: Build completes but exe won't run
```bash
# The exe needs all bundled files extracted on first run
# This takes 5+ seconds - wait and check if it launches
# If still fails, check: build/OpenModelica Simulator/warn-*.txt
```

---

## �🔧 Troubleshooting

### Issue: "Application file not found" when using launcher

**Solution**: Ensure directory structure is intact
```bash
# Check files exist
ls -la src/app.py
ls -la model/TwoConnectedTanks.exe
```

### Issue: "Module not found: PyQt6"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
# Or manually:
pip install PyQt6>=6.7.1
```

### Issue: "Batch file not found" error

**Root Cause**: The batch wrapper isn't in the same directory as the .exe

**Solution**: 
- Ensure `TwoConnectedTanks.bat` is in `model/` directory
- Name must match executable: `TwoConnectedTanks.exe` ↔ `TwoConnectedTanks.bat`

### Issue: Simulation runs but produces no output

**Possible Causes**:
1. Model requires additional initialization files
2. Model path invalid in batch file
3. Model compilation incomplete

**Debug Steps**:
```bash
# Test model directly
cd model
TwoConnectedTanks.bat -startTime=0 -stopTime=10
# Should produce terminal output
```

### Issue: GUI freezes during simulation

**This should not happen** - file a bug if it does. Threading prevents freezing.

**Workaround**: 
- Click STOP button to terminate
- Restart application: `python src/app.py`

### Issue: "Permission denied" on Unix/Linux

**Solution**: Make executable
```bash
chmod +x model/TwoConnectedTanks.exe
chmod +x model/TwoConnectedTanks.bat
```

### Issue: Python version mismatch

**Error**: `SyntaxError: invalid syntax` (typically with f-strings or type hints)

**Solution**: Upgrade Python
```bash
python --version        # Check current
# Download Python 3.10+ from python.org
```

---

## 📚 API Documentation

### SimpleSimulator Class

Main GUI window application.

```python
from src.app import SimpleSimulator

window = SimpleSimulator()
window.show()
```

**Methods**:
- `init_ui()` → `None`: Build UI components
- `run_simulation()` → `None`: Start simulation
- `stop_simulation()` → `None`: Stop running simulation
- `append_output(text: str)` → `None`: Add text to output log

**Signals** (Qt):
- `output`: Emitted by WorkerThread
- `finished`: Emitted when simulation completes

---

### WorkerThread Class

Background execution thread.

```python
from src.app import WorkerThread
from pathlib import Path

thread = WorkerThread(
    bat_file=Path("model/TwoConnectedTanks.bat"),
    exe_path=Path("model/TwoConnectedTanks.exe"),
    start_time=0.0,
    stop_time=100.0
)
thread.output.connect(print_function)
thread.start()
```

**Methods**:
- `run()` → `None`: Execute simulation (called automatically)
- `stop()` → `None`: Terminate process

**Signals**:
- `output(str)`: Emits stdout/stderr lines
- `finished()`: Emitted on completion

---

### SimulatorConfig Class

Configuration management.

```python
from src.config import SimulatorConfig

config = SimulatorConfig()

# Access settings
print(config.WINDOW_WIDTH)
print(config.DEFAULT_START_TIME)

# Validate input
is_valid, msg = config.validate_time_range(0, 100)
```

**Methods**:
- `get_model_executable_path()` → `Path`: Default .exe location
- `validate_time_range(start, stop)` → `(bool, str)`: Validates time range

---

## 🤝 Contributing

### Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd IITB_Project

# Create feature branch
git checkout -b feature/your-feature

# Make changes, test locally
python src/app.py

# Commit with descriptive messages
git commit -m "feat: Add new feature description"
git push origin feature/your-feature
```

### Code Style

- Run tools: `black`, `pylint`, `mypy` (when added)
- Follow existing code patterns
- Add docstrings to all functions
- Include type hints

### Testing

```bash
# Run manual tests
python src/app.py

# Test configuration validation
python -c "from src.config import SimulatorConfig; print(SimulatorConfig.validate_time_range(0, 100))"
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review API documentation above
3. Check application logs: Enable logging in `src/app.py`

---

## 🎓 Educational Notes

This project demonstrates:
- ✅ **Object-Oriented Programming**: Classes, inheritance, encapsulation
- ✅ **Type Hinting**: Modern Python type annotations
- ✅ **Error Handling**: Try/except/finally patterns
- ✅ **Threading**: Qt threading and signals
- ✅ **GUI Development**: PyQt6 layout and widgets
- ✅ **Configuration Management**: Dataclass patterns
- ✅ **Code Documentation**: Comprehensive docstrings
- ✅ **Professional Practices**: Logging, error handling, validation

Suitable for learning intermediate to advanced Python concepts.

---

**Last Updated**: April 5, 2026 | **Version**: 2.1 | **Status**: Production Ready
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
