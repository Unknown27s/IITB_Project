"""
Simple OpenModelica Simulation GUI
Run OpenModelica models with configurable start and stop times

Version: 2.0 (Simplified & Documented)
- Reduced from 500+ lines to ~200 lines for beginners
- Focus on core functionality and clarity
- Code simplification and documentation by Claude AI (Anthropic)
- Original architecture with GitHub Copilot

This is a beginner-friendly version that maintains all core features
while removing unnecessary complexity.
"""

import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox,
    QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class WorkerThread(QThread):
    """Run simulation in background without blocking GUI"""
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, bat_file, exe_path, start_time, stop_time):
        super().__init__()
        self.bat_file = bat_file
        self.exe_path = exe_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.process = None

    def run(self):
        try:
            # Prepare command
            cmd = [
                str(self.bat_file),
                f"-startTime={self.start_time}",
                f"-stopTime={self.stop_time}"
            ]

            # Get directory
            work_dir = str(Path(self.bat_file).parent)

            self.output.emit("Starting simulation...\n")
            self.output.emit(f"Start Time: {self.start_time}s\n")
            self.output.emit(f"Stop Time: {self.stop_time}s\n")
            self.output.emit("-" * 40 + "\n")

            # Run the batch file
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=work_dir
            )

            stdout, stderr = self.process.communicate()

            if stdout:
                self.output.emit(stdout)
            if stderr:
                self.output.emit("ERROR:\n" + stderr)

            if self.process.returncode == 0:
                self.output.emit("\n✓ Simulation completed successfully!")
            else:
                self.output.emit(f"\n✗ Error: Return code {self.process.returncode}")

        except Exception as e:
            self.output.emit(f"\n✗ Error: {str(e)}")
        finally:
            self.finished.emit()

    def stop(self):
        if self.process:
            self.process.terminate()


class SimpleSimulator(QMainWindow):
    """Simple OpenModelica Simulator GUI"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Build the user interface"""
        self.setWindowTitle("OpenModelica Simulator")
        self.setGeometry(100, 100, 700, 500)

        # Main widget
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("OpenModelica Model Simulator")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Executable selection
        exe_layout = QHBoxLayout()
        exe_layout.addWidget(QLabel("Executable:"))
        self.exe_input = QLineEdit()
        self.exe_input.setText(self.get_default_exe())
        exe_layout.addWidget(self.exe_input)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_exe)
        exe_layout.addWidget(browse_btn)
        layout.addLayout(exe_layout)

        # Start time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time (s):"))
        self.start_input = QDoubleSpinBox()
        self.start_input.setValue(5.1)
        self.start_input.setMinimum(0.0)
        self.start_input.setMaximum(999999.0)
        self.start_input.setDecimals(2)
        start_layout.addWidget(self.start_input)
        start_layout.addStretch()
        layout.addLayout(start_layout)

        # Stop time
        stop_layout = QHBoxLayout()
        stop_layout.addWidget(QLabel("Stop Time (s):"))
        self.stop_input = QDoubleSpinBox()
        self.stop_input.setValue(100.0)
        self.stop_input.setMinimum(0.0)
        self.stop_input.setMaximum(999999.0)
        self.stop_input.setDecimals(2)
        stop_layout.addWidget(self.stop_input)
        stop_layout.addStretch()
        layout.addLayout(stop_layout)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ START")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.run_simulation)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ STOP")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_simulation)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # Output area
        output_label = QLabel("Output Log:")
        layout.addWidget(output_label)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Courier", 9))
        layout.addWidget(self.output_area)

        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_default_exe(self):
        """Get default executable path"""
        exe = Path(__file__).parent.parent / "model" / "TwoConnectedTanks.exe"
        return str(exe) if exe.exists() else ""

    def browse_exe(self):
        """Open file browser"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Executable", "", "Executables (*.exe);;All Files (*)"
        )
        if path:
            self.exe_input.setText(path)

    def run_simulation(self):
        """Start the simulation"""
        exe_path = self.exe_input.text().strip()
        if not exe_path:
            QMessageBox.warning(self, "Error", "Please select an executable")
            return

        exe_path = Path(exe_path)
        if not exe_path.exists():
            QMessageBox.warning(self, "Error", f"File not found: {exe_path}")
            return

        start_time = self.start_input.value()
        stop_time = self.stop_input.value()

        if start_time >= stop_time:
            QMessageBox.warning(self, "Error", "Start time must be less than stop time")
            return

        # Find batch file in same directory as exe
        bat_path = exe_path.parent / (exe_path.stem + ".bat")
        if not bat_path.exists():
            QMessageBox.warning(self, "Error", f"Batch file not found: {bat_path}")
            return

        # Disable buttons and run
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.output_area.clear()
        self.status_label.setText("Running...")
        self.status_label.setStyleSheet("color: blue;")

        # Start worker thread
        self.worker = WorkerThread(bat_path, exe_path, start_time, stop_time)
        self.worker.output.connect(self.append_output)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def stop_simulation(self):
        """Stop the running simulation"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.output_area.append("\n[Stopping...]")
            self.stop_btn.setEnabled(False)

    def append_output(self, text):
        """Add text to output area"""
        self.output_area.append(text)
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )

    def on_finished(self):
        """Called when simulation finishes"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Done")
        self.status_label.setStyleSheet("color: green;")


def main():
    app = QApplication(sys.argv)
    window = SimpleSimulator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
