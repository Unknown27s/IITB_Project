# 🚀 OpenModelica Simulator - Launcher Guide

## Quick Start

### Option 1: Simple Launch (Recommended)
**Double-click `launcher.bat`**
- Automatically sets up Python environment
- Shows a splash screen
- Auto-launches the main application in 5 seconds
- Easy, beginner-friendly approach

### Option 2: Create Standalone Executable
**Run `build_exe.bat`**
- Creates `OpenModelica Simulator.exe` in the `dist/` folder
- Single file, no dependencies needed
- Can be run from anywhere
- Perfect for distribution/submission

```
Steps:
1. Double-click: build_exe.bat
2. Wait for build to complete (2-3 minutes)
3. Find: dist/OpenModelica Simulator.exe
4. Double-click to run!
```

### Option 3: Original Method
**Double-click `run.bat`**
- Direct launch of the GUI application
- Standard approach

---

## 🎯 What Each File Does

| File | Purpose |
|------|---------|
| `launcher.py` | Python launcher with splash screen |
| `launcher.bat` | Batch file to run launcher.py |
| `build_exe.bat` | Create standalone .exe file |
| `src/app.py` | Main GUI application |
| `run.bat` | Direct application launcher |

---

## 📦 For Submission/Distribution

**Best option:** Use the standalone .exe

```
1. Run: build_exe.bat
2. Wait for completion
3. Find: dist/OpenModelica Simulator.exe
4. Submit/Share this single file
```

The .exe includes everything needed - no Python installation required!

---

## 🎨 Launcher Features

✅ Beautiful purple gradient splash screen  
✅ Auto-launch countdown (5 seconds)  
✅ Manual launch button  
✅ Clean, professional appearance  
✅ Error handling & messages  

---

## 💡 Troubleshooting

**"Python not found"**
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

**"Failed to create .exe"**
- Run `build_exe.bat` again
- Make sure you have ~500MB free disk space

**Application won't start**
- Check that PyQt6 is installed
- Run `pip install PyQt6` in virtual environment

---

## 📧 For Your Mentor

You can now submit:
- Just the `launcher.bat` for easy testing
- Or the `.exe` file for even easier distribution

Both show:
1. ✅ Input fields (executable, start time, stop time)
2. ✅ START and STOP buttons
3. ✅ Real-time progress bar
4. ✅ Elapsed time timer
5. ✅ Working simulation results
