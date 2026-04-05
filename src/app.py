"""
OpenModelica Simulation GUI Application
Provides a user-friendly interface to run OpenModelica executable models
with configurable start and stop times.
"""

import sys
import os
import subprocess
import json
import traceback
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
    QGroupBox, QMessageBox, QSpinBox, QDoubleSpinBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon


class SimulationWorker(QThread):
    """Worker thread to run the simulation without blocking the GUI"""
    finished = pyqtSignal()
    output_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)  # Progress percentage 0-100

    def __init__(self, executable_path, start_time, stop_time):
        super().__init__()
        self.executable_path = executable_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.process = None
        self.total_duration = stop_time - start_time

    def run(self):
        """Execute the OpenModelica model"""
        try:
            # Validate inputs
            if not Path(self.executable_path).exists():
                self.error_occurred.emit(f"Executable not found: {self.executable_path}")
                return

            if self.start_time >= self.stop_time:
                self.error_occurred.emit("Start time must be less than stop time")
                return

            # Try to use batch file first (proper environment setup)
            exe_dir = os.path.dirname(self.executable_path)
            bat_file = os.path.join(exe_dir, "TwoConnectedTanks.bat")
            
            # Prefer batch file for better environment handling
            if os.path.exists(bat_file):
                command = [bat_file, f"-startTime={self.start_time}", f"-stopTime={self.stop_time}"]
                exec_label = "Batch File"
            else:
                command = [
                    self.executable_path,
                    f"-startTime={self.start_time}",
                    f"-stopTime={self.stop_time}"
                ]
                exec_label = "Direct Executable"

            self.output_received.emit(f"Starting simulation...\n")
            self.output_received.emit(f"Execution Mode: {exec_label}\n")
            self.output_received.emit(f"Command: {' '.join(command)}\n")
            self.output_received.emit(f"Start Time: {self.start_time}\n")
            self.output_received.emit(f"Stop Time: {self.stop_time}\n")
            self.output_received.emit(f"Simulation Duration: {self.total_duration:.1f} seconds\n")
            self.output_received.emit("-" * 50 + "\n")

            # Set up environment with proper PATH for OpenModelica runtime libraries
            env = os.environ.copy()
            bin_path = r"D:\Harish Kumar\bin"
            
            # Add bin directory to PATH if it exists
            if os.path.exists(bin_path):
                env['PATH'] = bin_path + os.pathsep + env.get('PATH', '')
                self.output_received.emit(f"Runtime path added: {bin_path}\n")

            # Emit progress
            self.progress_updated.emit(0)

            # Run the executable
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=exe_dir,
                env=env
            )

            # Read output
            stdout, stderr = self.process.communicate()

            if stdout:
                self.output_received.emit("STDOUT:\n")
                self.output_received.emit(stdout + "\n")

            if stderr:
                self.output_received.emit("STDERR:\n")
                self.output_received.emit(stderr + "\n")

            if self.process.returncode == 0:
                self.output_received.emit("-" * 50 + "\n")
                self.output_received.emit("Simulation completed successfully!\n")
                self.output_received.emit("Results saved to: model/TwoConnectedTanks_res.mat\n")
                self.progress_updated.emit(100)
            elif self.process.returncode is None or self.process.returncode == -15:
                self.output_received.emit("-" * 50 + "\n")
                self.output_received.emit("Simulation stopped by user.\n")
            else:
                self.error_occurred.emit(f"Simulation failed with return code: {self.process.returncode}")

        except FileNotFoundError:
            self.error_occurred.emit("Executable file not found")
        except PermissionError:
            self.error_occurred.emit("Permission denied: Cannot execute the file")
        except Exception as e:
            self.error_occurred.emit(f"Error occurred: {str(e)}")
        finally:
            self.finished.emit()

    def stop(self):
        """Stop the running process"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()


class ModelSimulatorGUI(QMainWindow):
    """Main GUI Application for OpenModelica Model Simulation"""

    def __init__(self):
        super().__init__()
        self.simulation_worker = None
        self.elapsed_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("OpenModelica Model Simulator")
        self.setGeometry(100, 100, 900, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("OpenModelica Model Simulation")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Input Group
        input_group = QGroupBox("Simulation Configuration")
        input_layout = QVBoxLayout()

        # Row 1: Executable Selection
        exec_layout = QHBoxLayout()
        exec_label = QLabel("Application to Launch:")
        exec_label.setMinimumWidth(150)
        self.exec_input = QLineEdit()
        self.exec_input.setPlaceholderText("Select or enter the path to the executable...")
        self.exec_input.setText(self.get_default_executable())
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_executable)
        exec_layout.addWidget(exec_label)
        exec_layout.addWidget(self.exec_input)
        exec_layout.addWidget(browse_btn)
        input_layout.addLayout(exec_layout)

        # Row 2: Start Time
        start_layout = QHBoxLayout()
        start_label = QLabel("Start Time:")
        start_label.setMinimumWidth(150)
        self.start_time_input = QDoubleSpinBox()
        self.start_time_input.setMinimum(0.0)
        self.start_time_input.setMaximum(1000000.0)
        self.start_time_input.setValue(5.1)
        self.start_time_input.setDecimals(2)
        self.start_time_input.setSuffix(" seconds")
        start_info_label = QLabel("(Model: Flow disabled 0-5s, enabled after 5s)")
        start_info_label.setStyleSheet("color: gray; font-size: 9px;")
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_time_input)
        start_layout.addWidget(start_info_label)
        start_layout.addStretch()
        input_layout.addLayout(start_layout)

        # Row 3: Stop Time
        stop_layout = QHBoxLayout()
        stop_label = QLabel("Stop Time:")
        stop_label.setMinimumWidth(150)
        self.stop_time_input = QDoubleSpinBox()
        self.stop_time_input.setMinimum(0.0)
        self.stop_time_input.setMaximum(1000000.0)
        self.stop_time_input.setValue(100.0)
        self.stop_time_input.setDecimals(2)
        self.stop_time_input.setSuffix(" seconds")
        stop_layout.addWidget(stop_label)
        stop_layout.addWidget(self.stop_time_input)
        stop_layout.addStretch()
        input_layout.addLayout(stop_layout)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Control Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # START Button
        self.start_btn = QPushButton("▶ START")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setMinimumWidth(120)
        start_font = QFont()
        start_font.setPointSize(11)
        start_font.setBold(True)
        self.start_btn.setFont(start_font)
        self.start_btn.clicked.connect(self.execute_simulation)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        # STOP Button
        self.stop_btn = QPushButton("⏹ STOP")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setMinimumWidth(120)
        stop_font = QFont()
        stop_font.setPointSize(11)
        stop_font.setBold(True)
        self.stop_btn.setFont(stop_font)
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover:!disabled {
                background-color: #c82333;
            }
            QPushButton:pressed:!disabled {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid gray;
                border-radius: 4px;
                text-align: center;
                color: black;
            }
            QProgressBar::chunk {
                background-color: #28a745;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Output Group
        output_group = QGroupBox("Execution Output & Log")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 9))
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # Elapsed Time Label
        self.elapsed_label = QLabel("⏱️ Elapsed Time: 0s")
        self.elapsed_label.setStyleSheet("color: blue; font-weight: bold; font-size: 10px;")
        main_layout.addWidget(self.elapsed_label)

        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: green;")
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

    def get_default_executable(self):
        """Get the default executable path from the model folder"""
        model_dir = Path(__file__).parent.parent / "model"
        exe_path = model_dir / "TwoConnectedTanks.exe"
        if exe_path.exists():
            return str(exe_path)
        return ""

    def browse_executable(self):
        """Open file dialog to select executable"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select OpenModelica Executable",
            os.path.dirname(self.exec_input.text()) or str(Path.home()),
            "Executable Files (*.exe);;All Files (*)"
        )
        if file_path:
            self.exec_input.setText(file_path)

    def execute_simulation(self):
        """Execute the simulation"""
        # Validate inputs
        exec_path = self.exec_input.text().strip()
        if not exec_path:
            QMessageBox.warning(self, "Input Error", "Please select an executable")
            return

        start_time = self.start_time_input.value()
        stop_time = self.stop_time_input.value()

        if start_time >= stop_time:
            QMessageBox.warning(self, "Input Error", "Start time must be less than stop time")
            return

        # Disable START button, enable STOP button, and update status
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Running simulation...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        self.output_text.clear()
        self.progress_bar.setValue(0)
        
        # Start elapsed time counter
        self.elapsed_time = 0
        self.elapsed_label.setText("⏱️ Elapsed Time: 0s")
        self.timer.start(1000)  # Update every 1 second

        # Create and start worker thread
        self.simulation_worker = SimulationWorker(exec_path, start_time, stop_time)
        self.simulation_worker.output_received.connect(self.append_output)
        self.simulation_worker.error_occurred.connect(self.handle_error)
        self.simulation_worker.progress_updated.connect(self.progress_bar.setValue)
        self.simulation_worker.finished.connect(self.simulation_finished)
        self.simulation_worker.start()

    def stop_simulation(self):
        """Stop the running simulation"""
        if self.simulation_worker and self.simulation_worker.isRunning():
            self.output_text.append("\n[USER] Stopping simulation...\n")
            self.simulation_worker.stop()
            self.stop_btn.setEnabled(False)
            self.status_label.setText("Stopping simulation...")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.timer.stop()

    def append_output(self, text):
        """Append text to output area"""
        self.output_text.append(text)
        # Auto-scroll to bottom
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def handle_error(self, error_message):
        """Handle errors from simulation"""
        # Stop elapsed time counter
        self.timer.stop()
        
        # Re-enable START button, disable STOP button
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.status_label.setText(f"❌ Error: {error_message}")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.append_output(f"\n{'!'*50}\nERROR: {error_message}\n{'!'*50}\n")
        QMessageBox.critical(self, "Simulation Error", error_message)

    def simulation_finished(self):
        """Called when simulation finishes"""
        # Stop elapsed time counter
        self.timer.stop()
        
        # Re-enable START button, disable STOP button
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(100)
        
        # Update status based on output
        output_text = self.output_text.toPlainText()
        if "successfully" in output_text.lower():
            self.status_label.setText("✓ Simulation completed successfully")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        elif "stopped" in output_text.lower() or "ERROR" in output_text:
            self.status_label.setText("⚠ Simulation stopped or failed")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.status_label.setText("Simulation completed")
            self.status_label.setStyleSheet("color: gray; font-weight: bold;")

    def update_elapsed_time(self):
        """Update the elapsed time label"""
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        
        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"
        
        self.elapsed_label.setText(f"⏱️ Elapsed Time: {time_str}")


def main():
    """Main entry point"""
    try:
        app = QApplication(sys.argv)
        gui = ModelSimulatorGUI()
        gui.show()
        sys.exit(app.exec())
    except Exception as e:
        # Log error to file
        error_log = Path(__file__).parent.parent / "error_log.txt"
        try:
            with open(error_log, "w") as f:
                f.write(f"Error at {datetime.now()}\n")
                f.write(f"Error: {str(e)}\n")
                f.write(f"Type: {type(e).__name__}\n")
                f.write(f"\nTraceback:\n{traceback.format_exc()}")
        except:
            pass
        
        # Try to show error in message box (don't re-import QApplication)
        try:
            existing_app = QApplication.instance()
            if existing_app is None:
                existing_app = QApplication(sys.argv)
            
            QMessageBox.critical(
                None,
                "Application Error",
                f"An error occurred:\n\n{str(e)}\n\nCheck error_log.txt for details."
            )
        except:
            print(f"ERROR: {str(e)}", file=sys.stderr)
            print(f"See error_log.txt in the project root for details.")


if __name__ == "__main__":
    main()
