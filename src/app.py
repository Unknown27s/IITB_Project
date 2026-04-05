"""
OpenModelica Simulator - Main Application Module

A PyQt6-based graphical user interface for executing OpenModelica
simulation models with configurable start and stop times.

This module implements a complete MVC-style GUI application using:
- QThread for non-blocking simulation execution
- Signals/slots for thread-safe communication
- Configuration management via config.py
- Comprehensive error handling and validation
- Proper type hints and documentation

Version: 2.1 (Enhanced with type hints and OOP improvements)
- Full type annotations
- Configuration class pattern
- Improved error handling
- Enhanced logging and debugging
- Better docstrings and API documentation

Author: IIT Bombay Project Series
License: MIT
"""

import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox,
    QDoubleSpinBox, QScrollBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from config import SimulatorConfig

# Configure logging for debugging and error tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkerThread(QThread):
    """
    Worker thread for executing OpenModelica simulations without blocking the GUI.
    
    This class runs the simulation in a background thread using Qt's signal/slot
    mechanism to safely communicate results back to the main GUI thread. This
    prevents the UI from freezing during long-running simulations.
    
    Qt Signals:
        output (pyqtSignal[str]): Emitted when simulation produces output.
            The signal carries text to be displayed in the output log.
        
        finished (pyqtSignal): Emitted when simulation execution completes
            (either successfully or with an error).
    
    Attributes:
        bat_file (Path): Path to batch file that executes the model
        exe_path (Path): Path to OpenModelica executable
        start_time (float): Simulation start time in seconds
        stop_time (float): Simulation stop time in seconds
        process (Optional[subprocess.Popen]): Reference to running process
    
    Example:
        >>> thread = WorkerThread(
        ...     bat_file=Path("model/TwoConnectedTanks.bat"),
        ...     exe_path=Path("model/TwoConnectedTanks.exe"),
        ...     start_time=0.0,
        ...     stop_time=100.0
        ... )
        >>> thread.output.connect(print_output)  # Connect signal
        >>> thread.start()  # Begin execution
    """
    
    # Define signals at class level (required by PyQt6)
    output = pyqtSignal(str)  # Emits text output
    finished = pyqtSignal()   # Emits when simulation completes

    def __init__(
        self,
        bat_file: Path,
        exe_path: Path,
        start_time: float,
        stop_time: float
    ) -> None:
        """
        Initialize worker thread with simulation parameters.
        
        Args:
            bat_file (Path): Path to batch file wrapper for the executable
            exe_path (Path): Path to OpenModelica .exe file
            start_time (float): Simulation start time in seconds
            stop_time (float): Simulation stop time in seconds
            
        Raises:
            TypeError: If inputs are not of correct types
        """
        super().__init__()
        self.bat_file = bat_file
        self.exe_path = exe_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.process: Optional[subprocess.Popen] = None
        logger.info(f"WorkerThread initialized: {bat_file.name}")

    def run(self) -> None:
        """
        Execute the simulation in background thread.
        
        This method is automatically called when thread.start() is invoked.
        It builds the command line, executes the batch file, captures output,
        and emits signals to update the GUI.
        
        The command executed is:
            <bat_file> -startTime=<start> -stopTime=<stop>
        
        Returns:
            None: Signals are used to communicate results back to main thread
            
        Note:
            This method runs in a separate thread. All Qt operations must
            use signals/slots to communicate with the main GUI thread.
        """
        try:
            # Build command with time parameters
            cmd = [
                str(self.bat_file),
                f"-startTime={self.start_time}",
                f"-stopTime={self.stop_time}"
            ]

            # Get working directory from batch file location
            work_dir = str(self.bat_file.parent)
            
            logger.info(f"Starting simulation: {' '.join(cmd)}")

            # Emit startup information
            self.output.emit("▶ Starting simulation...\n")
            self.output.emit(f"  Start Time: {self.start_time}s\n")
            self.output.emit(f"  Stop Time:  {self.stop_time}s\n")
            self.output.emit("-" * 50 + "\n")

            # Execute the batch file
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=work_dir
            )

            # Wait for process and capture output
            stdout, stderr = self.process.communicate()

            # Emit captured output
            if stdout:
                self.output.emit(stdout)
            
            if stderr:
                self.output.emit("\n⚠️  ERROR OUTPUT:\n")
                self.output.emit(stderr)

            # Emit completion status
            if self.process.returncode == 0:
                self.output.emit("\n" + "=" * 50)
                self.output.emit("\n✓ Simulation completed successfully!\n")
                logger.info("Simulation completed successfully")
            else:
                self.output.emit("\n" + "=" * 50)
                self.output.emit(f"\n✗ Error: Process exited with code {self.process.returncode}\n")
                logger.error(f"Simulation failed with return code: {self.process.returncode}")

        except FileNotFoundError as e:
            error_msg = f"⚠️  ERROR: File not found\n{str(e)}\n"
            self.output.emit(error_msg)
            logger.error(f"FileNotFoundError: {e}")
            
        except PermissionError as e:
            error_msg = f"⚠️  ERROR: Permission denied\n{str(e)}\nMake sure the file is executable.\n"
            self.output.emit(error_msg)
            logger.error(f"PermissionError: {e}")
            
        except Exception as e:
            error_msg = f"⚠️  ERROR: An unexpected error occurred\n{type(e).__name__}: {str(e)}\n"
            self.output.emit(error_msg)
            logger.exception(f"Unexpected error during simulation: {e}")
            
        finally:
            # Always emit finished signal when thread completes
            self.finished.emit()
            logger.info("WorkerThread finished")

    def stop(self) -> None:
        """
        Terminate the running simulation process.
        
        This method safely stops the currently running simulation by
        calling terminate() on the subprocess. The process is given a
        short time to finish gracefully before being killed.
        
        Returns:
            None
            
        Note:
            This method is called from the main GUI thread when user
            clicks the STOP button, so it must be thread-safe.
        """
        if self.process and self.process.poll() is None:  # Check if still running
            logger.info("Stopping simulation process")
            self.process.terminate()
            try:
                # Wait up to 3 seconds for graceful shutdown
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # Force kill if doesn't terminate gracefully
                logger.warning("Process did not terminate gracefully, forcing kill")
                self.process.kill()
        else:
            logger.debug("No running process to stop")


class SimpleSimulator(QMainWindow):
    """
    Main application window for OpenModelica Simulator.
    
    This class implements the complete GUI for the simulator application,
    including controls for executable selection, time configuration, and
    an output display area. It follows MVC principles by:
    
    - Separating UI initialization (init_ui) from logic
    - Using Qt signals/slots for event handling
    - Delegating heavy computation to WorkerThread
    - Centralizing configuration via SimulatorConfig
    
    Attributes:
        config (SimulatorConfig): Application configuration instance
        worker (Optional[WorkerThread]): Reference to currently running worker thread
        exe_input (QLineEdit): Text input for executable path
        start_input (QDoubleSpinBox): Spinner for simulation start time
        stop_input (QDoubleSpinBox): Spinner for simulation stop time
        start_btn (QPushButton): Button to start simulation
        stop_btn (QPushButton): Button to stop simulation
        output_area (QTextEdit): Read-only text area for simulation output
        status_label (QLabel): Status display label
        
    Example:
        >>> app = QApplication(sys.argv)
        >>> simulator = SimpleSimulator()
        >>> simulator.show()
        >>> sys.exit(app.exec())
    """

    def __init__(self) -> None:
        """
        Initialize the main application window.
        
        Creates the main window and initializes all UI components
        using the configuration and build_ui methods.
        """
        super().__init__()
        self.config = SimulatorConfig()
        self.worker: Optional[WorkerThread] = None
        
        # Initialize UI
        self.init_ui()
        logger.info("SimpleSimulator initialized")

    def init_ui(self) -> None:
        """
        Build and configure the user interface.
        
        This method creates all UI elements including:
        - Window properties and layout
        - Input fields for executable path and time parameters
        - Control buttons (START/STOP)
        - Output log display
        - Status indicator
        
        All dimensions and styling are sourced from SimulatorConfig
        for easy customization.
        
        Returns:
            None
        """
        # Configure main window
        self.setWindowTitle(self.config.WINDOW_TITLE)
        self.setGeometry(
            self.config.WINDOW_X_POS,
            self.config.WINDOW_Y_POS,
            self.config.WINDOW_WIDTH,
            self.config.WINDOW_HEIGHT
        )

        # Create main layout
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("OpenModelica Model Simulator")
        title_font = QFont()
        title_font.setPointSize(self.config.TITLE_FONT_SIZE)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # ===== EXECUTABLE SELECTION SECTION =====
        exe_layout = QHBoxLayout()
        exe_layout.addWidget(QLabel("Executable Path:"))
        self.exe_input = QLineEdit()
        self.exe_input.setText(self._get_default_exe_path())
        exe_layout.addWidget(self.exe_input)
        
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_exe)
        exe_layout.addWidget(browse_btn)
        layout.addLayout(exe_layout)

        # ===== START TIME SECTION =====
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time (seconds):"))
        self.start_input = QDoubleSpinBox()
        self.start_input.setValue(self.config.DEFAULT_START_TIME)
        self.start_input.setMinimum(self.config.MIN_TIME_VALUE)
        self.start_input.setMaximum(self.config.MAX_TIME_VALUE)
        self.start_input.setDecimals(self.config.TIME_DECIMALS)
        start_layout.addWidget(self.start_input)
        start_layout.addStretch()
        layout.addLayout(start_layout)

        # ===== STOP TIME SECTION =====
        stop_layout = QHBoxLayout()
        stop_layout.addWidget(QLabel("Stop Time (seconds):"))
        self.stop_input = QDoubleSpinBox()
        self.stop_input.setValue(self.config.DEFAULT_STOP_TIME)
        self.stop_input.setMinimum(self.config.MIN_TIME_VALUE)
        self.stop_input.setMaximum(self.config.MAX_TIME_VALUE)
        self.stop_input.setDecimals(self.config.TIME_DECIMALS)
        stop_layout.addWidget(self.stop_input)
        stop_layout.addStretch()
        layout.addLayout(stop_layout)

        # ===== CONTROL BUTTONS SECTION =====
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ START SIMULATION")
        self.start_btn.setMinimumHeight(self.config.BUTTON_MIN_HEIGHT)
        self.start_btn.clicked.connect(self.run_simulation)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ STOP SIMULATION")
        self.stop_btn.setMinimumHeight(self.config.BUTTON_MIN_HEIGHT)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_simulation)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # ===== OUTPUT AREA SECTION =====
        output_label = QLabel("Simulation Output Log:")
        layout.addWidget(output_label)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        output_font = QFont(self.config.OUTPUT_FONT_NAME)
        output_font.setPointSize(self.config.OUTPUT_FONT_SIZE)
        self.output_area.setFont(output_font)
        layout.addWidget(self.output_area)

        # ===== STATUS SECTION =====
        self.status_label = QLabel("Ready to start simulation")
        self.status_label.setStyleSheet("color: green;")
        layout.addWidget(self.status_label)

        # Set central widget
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _get_default_exe_path(self) -> str:
        """
        Get the default path to the OpenModelica executable.
        
        This method uses the project structure to locate the default
        TwoConnectedTanks.exe file if it exists.
        
        Returns:
            str: String path to executable, or empty string if not found
            
        Note:
            The default location is: project_root/model/TwoConnectedTanks.exe
        """
        exe = self.config.get_model_executable_path()
        result = str(exe) if exe.exists() else ""
        logger.info(f"Default executable path: {result}")
        return result

    def browse_exe(self) -> None:
        """
        Open file browser dialog for executable selection.
        
        Allows user to navigate filesystem and select a .exe or any
        executable file. Updates exe_input field with selected path.
        
        Returns:
            None
        """
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select OpenModelica Executable",
            "",
            "Executables (*.exe);;Batch Files (*.bat);;All Files (*)"
        )
        if path:
            self.exe_input.setText(path)
            logger.info(f"User selected executable: {path}")

    def run_simulation(self) -> None:
        """
        Validate inputs and start simulation in worker thread.
        
        This method:
        1. Validates all user inputs (file existence, time range)
        2. Disables START button and enables STOP button
        3. Clears previous output
        4. Creates and starts WorkerThread with parameters
        5. Connects signal handlers for output and completion
        
        Returns:
            None
            
        Raises:
            None: Errors are shown to user via message boxes
        """
        logger.info("User initiated simulation")
        
        # Get and validate executable path
        exe_path_str = self.exe_input.text().strip()
        if not exe_path_str:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please select an executable file.\n\n"
                "Click the 'Browse' button to locate your .exe file."
            )
            logger.warning("Simulation start failed: no executable selected")
            return

        exe_path = Path(exe_path_str)
        if not exe_path.exists():
            QMessageBox.critical(
                self,
                "File Not Found",
                f"The selected file does not exist:\n{exe_path}\n\n"
                "Please check the path and try again."
            )
            logger.error(f"Executable file not found: {exe_path}")
            return

        if not exe_path.is_file():
            QMessageBox.warning(
                self,
                "Invalid Selection",
                f"The selected path is not a file:\n{exe_path}"
            )
            logger.warning(f"Selected path is not a file: {exe_path}")
            return

        # Get time parameters
        start_time = float(self.start_input.value())
        stop_time = float(self.stop_input.value())

        # Validate time range
        is_valid, error_msg = self.config.validate_time_range(start_time, stop_time)
        if not is_valid:
            QMessageBox.warning(
                self,
                "Time Range Error",
                f"{error_msg}\n\n"
                f"Start time: {start_time}s\n"
                f"Stop time:  {stop_time}s"
            )
            logger.warning(f"Invalid time range: start={start_time}, stop={stop_time}")
            return

        # Find corresponding batch file
        bat_path = exe_path.parent / (exe_path.stem + ".bat")
        if not bat_path.exists():
            QMessageBox.warning(
                self,
                "Batch File Not Found",
                f"Could not find batch wrapper file:\n{bat_path}\n\n"
                "The batch file must be in the same directory as the executable\n"
                "with the same filename (different extension)."
            )
            logger.error(f"Batch file not found: {bat_path}")
            return

        # Update UI for running state
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.output_area.clear()
        self.status_label.setText("Running simulation...")
        self.status_label.setStyleSheet("color: blue;")

        # Create and start worker thread
        self.worker = WorkerThread(bat_path, exe_path, start_time, stop_time)
        self.worker.output.connect(self.append_output)
        self.worker.finished.connect(self.on_simulation_finished)
        self.worker.start()
        logger.info(f"Simulation started: start_time={start_time}s, stop_time={stop_time}s")

    def stop_simulation(self) -> None:
        """
        Stop the currently running simulation.
        
        Sends termination signal to worker thread and updates
        UI to indicate stopping in progress.
        
        Returns:
            None
        """
        if self.worker and self.worker.isRunning():
            logger.info("User requested simulation stop")
            self.worker.stop()
            self.output_area.append("\n⏹ Stopping simulation...\n")
            self.stop_btn.setEnabled(False)
        else:
            logger.debug("Stop requested but no simulation running")

    def append_output(self, text: str) -> None:
        """
        Append text to the output log display.
        
        This method is connected to the worker thread's output signal.
        It appends text and automatically scrolls to the latest output.
        
        Args:
            text (str): Text to append to output display
            
        Returns:
            None
            
        Note:
            Called automatically via Qt signal connection whenever
            WorkerThread emits output signal.
        """
        self.output_area.append(text)
        # Auto-scroll to bottom
        scrollbar = self.output_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_simulation_finished(self) -> None:
        """
        Handle simulation completion.
        
        Called automatically via Qt signal when worker thread finishes.
        Updates UI buttons and status display.
        
        Returns:
            None
            
        Note:
            This method restores the UI to idle state, allowing the
            user to run another simulation or modify parameters.
        """
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Simulation completed - Ready for next run")
        self.status_label.setStyleSheet("color: green;")
        logger.info("Simulation completed, UI restored to idle state")


def main() -> int:
    """
    Main entry point for the OpenModelica Simulator application.
    
    Initializes the Qt application and main window, then starts
    the event loop.
    
    Returns:
        int: Exit code from Qt application event loop
        (0 on successful exit, non-zero on error)
        
    Example:
        >>> import sys
        >>> exit_code = main()
        >>> sys.exit(exit_code)
    """
    logger.info("=" * 60)
    logger.info("OpenModelica Simulator Application Started")
    logger.info("=" * 60)
    
    try:
        app = QApplication(sys.argv)
        window = SimpleSimulator()
        window.show()
        logger.info("Main window displayed, entering event loop")
        exit_code = app.exec()
        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code
    except Exception as e:
        logger.critical(f"Fatal error in main(): {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    """
    Script entry point.
    
    When this file is run directly (not imported), execute the main()
    function and exit with its return code.
    """
    exit_code = main()
    sys.exit(exit_code)
