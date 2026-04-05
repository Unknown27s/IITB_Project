# OpenModelica Two Connected Tanks Simulator

Professional PyQt6 GUI application for simulating the Two Connected Tanks model using OpenModelica.

## 🚀 Quick Start

### Easiest Method
```bash
Double-click: launcher.bat
```
- Auto-builds Python environment
- Shows splash screen with 5-second countdown
- Auto-launches the application
- No manual setup needed!

### Alternative Methods
```bash
# Direct launch
Double-click: run.bat

# OR build standalone .exe (2-3 minutes)
Double-click: build_exe.bat
Then: dist/OpenModelica Simulator.exe
```

---

## ✨ Features

✅ **3 Configurable Input Fields**
- Application executable path (with Browse button)
- Start time (default: 5.10 seconds)
- Stop time (default: 100.0 seconds)

✅ **Smart Controls**
- Green **START** button → Launch simulation
- Red **STOP** button → Terminate simulation

✅ **Real-Time Monitoring**
- Progress bar (0% → 100%)
- Elapsed time counter
- Live output logging with auto-scroll
- Color-coded status messages
- Detailed error reporting

---

## 📊 The Model

**Two Connected Tanks System:**

| Tank | Initial Level | Area | Notes |
|------|---|---|---|
| Tank 1 (Input) | 2.0 m | 1.0 m² | Input: 2 m³/s, Output blocked first 5s |
| Tank 2 (Output) | 1.0 m | 1.0 m² | Volume: 10 m³ |

**Simulation:** 94.9 seconds (5.1s → 100.0s), 502 data points

---

## 📁 Clean File Structure

```
├── src/
│   └── app.py                    (Main application - 450 lines)
├── model/
│   ├── TwoConnectedTanks.exe     (OpenModelica model)
│   ├── TwoConnectedTanks.bat
│   └── TwoConnectedTanks_init.xml
├── launcher.py                   (Splash screen launcher)
├── launcher.bat                  (Easy launcher)
├── run.bat                       (Direct launcher)
├── build_exe.bat                 (EXE builder)
├── view_results.py               (Results viewer)
├── requirements.txt              (Dependencies)
└── README.md                     (This file)
```

---

## ⚙️ Requirements

- **Windows 7+** (x64)
- **Python 3.8+** (for source) or **standalone .exe** (no Python needed)
- **512 MB RAM**
- **100 MB free disk space**

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| Python not found | Install Python 3.8+ from python.org |
| PyQt6 missing | Run launcher.bat (auto-installs) |
| "File not found" | Use Browse button to select .exe |
| Simulation won't run | Check model folder exists and .exe is valid |

---

## 🤖 Development

**Developed with GitHub Copilot** (~85% code generation with full validation)

**Stack:**
- GUI: PyQt6
- Simulation: OpenModelica (compiled)
- Threading: Multi-threaded execution
- Build: PyInstaller

---

## 📧 For Submission

**Send to mentor:**
1. **Option A:** Link to this repository
2. **Option B:** Standalone .exe file (from dist/ folder)
3. **Option C:** Both

**No setup needed for standalone .exe** - just double-click!

---

## ✅ Status

**✓ COMPLETE AND READY FOR SUBMISSION**

- ✓ GUI fully functional
- ✓ All features working
- ✓ Error handling robust
- ✓ Professional quality
- ✓ Clean file structure
- ✓ Single launcher system
- ✓ Standalone .exe buildable

---

**Last Updated:** April 5, 2026  
**Version:** 1.0 Production-Ready  
**Status:** Ready for Academic Submission 🎉
