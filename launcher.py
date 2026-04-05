"""
OpenModelica Simulator - Application Launcher Module

This module provides a splash screen and launcher interface for the
OpenModelica Simulator application. It displays a professional splash
screen with automatic launch capability and manual launch button.

Features:
    - Splash screen with gradient background
    - Automatic launch countdown (5 seconds)
    - Manual launch button for immediate startup
    - Error handling for missing application files
    - Cross-platform support (Windows, Linux, macOS)

The launcher can be used as an optional entry point to provide a
polished startup experience before the main application window appears.

Example:
    >>> python launcher.py
    
This displays the splash screen with countdown and launches the main
application from src/app.py.

Author: IIT Bombay Project Series
License: MIT
"""

import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SplashScreen(QDialog):
    """
    Splash screen and launcher window for OpenModelica Simulator.
    
    This dialog displays a professional splash screen with application
    branding and provides two methods to start the main application:
    1. Click "Launch Application" button for immediate start
    2. Wait for automatic launch countdown (default: 5 seconds)
    
    The splash screen features:
    - Gradient purple background
    - Application logo and title
    - Description text
    - Countdown timer for auto-launch
    - Manual launch button
    
    Attributes:
        timer (QTimer): Timer for countdown auto-launch
        auto_close_counter (int): Countdown value in seconds
        auto_label (QLabel): Label showing countdown status
        
    Example:
        >>> app = QApplication(sys.argv)
        >>> splash = SplashScreen()
        >>> splash.show()
        >>> sys.exit(app.exec())
    """
    
    # Configuration constants
    AUTO_LAUNCH_SECONDS = 5
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300
    WINDOW_X_POS = 500
    WINDOW_Y_POS = 300
    TITLE_FONT_SIZE = 24
    SUBTITLE_FONT_SIZE = 14
    DESC_FONT_SIZE = 10
    BUTTON_FONT_SIZE = 12
    BUTTON_HEIGHT = 50
    
    def __init__(self) -> None:
        """
        Initialize the splash screen window.
        
        Sets up UI components and starts the auto-launch countdown timer.
        
        Returns:
            None
        """
        super().__init__()
        self.timer = QTimer()
        self.auto_close_counter = self.AUTO_LAUNCH_SECONDS
        self.init_ui()
        
        logger.info("SplashScreen initialized")
    
    def init_ui(self) -> None:
        """
        Build and configure the splash screen UI.
        
        Creates all visual elements including:
        - Window properties and geometry
        - Title and subtitle labels
        - Description text
        - Launch button with styling
        - Auto-launch countdown label
        
        Returns:
            None
        """
        # Configure window
        self.setWindowTitle("OpenModelica Simulator Launcher")
        self.setGeometry(
            self.WINDOW_X_POS,
            self.WINDOW_Y_POS,
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT
        )
        self.setStyleSheet("""
            QDialog {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
        """)
        
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # ===== TITLE SECTION =====
        title = QLabel("OpenModelica")
        title_font = QFont()
        title_font.setPointSize(self.TITLE_FONT_SIZE)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # ===== SUBTITLE SECTION =====
        subtitle = QLabel("Model Simulator")
        subtitle_font = QFont()
        subtitle_font.setPointSize(self.SUBTITLE_FONT_SIZE)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #ddd;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # ===== DESCRIPTION SECTION =====
        description_text = (
            "Two Connected Tanks Simulation\n\n"
            "Click 'Launch Application' to start immediately\n"
            "or wait for automatic launch"
        )
        desc = QLabel(description_text)
        desc_font = QFont()
        desc_font.setPointSize(self.DESC_FONT_SIZE)
        desc.setFont(desc_font)
        desc.setStyleSheet("color: #fff;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # ===== LAUNCH BUTTON SECTION =====
        launch_btn = QPushButton("▶ LAUNCH APPLICATION")
        launch_btn.setMinimumHeight(self.BUTTON_HEIGHT)
        launch_font = QFont()
        launch_font.setPointSize(self.BUTTON_FONT_SIZE)
        launch_font.setBold(True)
        launch_btn.setFont(launch_font)
        launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #667eea;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        launch_btn.clicked.connect(self._launch_main_app)
        layout.addWidget(launch_btn)
        
        # ===== AUTO-LAUNCH COUNTDOWN SECTION =====
        self.auto_label = QLabel(f"Auto-launching in {self.AUTO_LAUNCH_SECONDS}s...")
        auto_font = QFont()
        auto_font.setPointSize(9)
        self.auto_label.setFont(auto_font)
        self.auto_label.setStyleSheet("color: #ccc;")
        self.auto_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.auto_label)
        
        self.setLayout(layout)
        
        # Start auto-launch countdown timer
        self.timer.timeout.connect(self._on_countdown_tick)
        self.timer.start(1000)  # Fire every 1000ms (1 second)
        
        logger.info(f"Splash screen UI created, starting {self.AUTO_LAUNCH_SECONDS}s countdown")
    
    def _on_countdown_tick(self) -> None:
        """
        Handle countdown timer tick.
        
        Updates the countdown label and launches the application when
        the countdown reaches zero.
        
        Returns:
            None
            
        Note:
            This method is automatically called by the QTimer at 1-second
            intervals until the countdown expires.
        """
        self.auto_close_counter -= 1
        
        if self.auto_close_counter > 0:
            self.auto_label.setText(f"Auto-launching in {self.auto_close_counter}s...")
        else:
            self.auto_label.setText("Launching...")
            self.timer.stop()
            logger.info("Auto-launch countdown expired, launching application")
            self._launch_main_app()
    
    def _launch_main_app(self) -> None:
        """
        Launch the main application.
        
        When running from source (development), spawns a subprocess.
        When running as bundled exe, directly imports and runs the app.
        
        Returns:
            None
        """
        self.timer.stop()
        
        logger.info("Launching main application...")
        
        is_bundled = getattr(sys, 'frozen', False)
        
        if is_bundled:
            # BUNDLED EXE: Directly import and run app in same process
            # This is more reliable than spawning subprocess
            try:
                logger.info("Running in bundled mode - importing app directly")
                # Add src to path if needed
                src_path = Path(sys._MEIPASS) / "src"
                if str(src_path) not in sys.path:
                    sys.path.insert(0, str(src_path))
                    logger.info(f"Added to sys.path: {src_path}")
                
                # Import and run the main application
                from app import main as app_main
                logger.info("Successfully imported app.main")
                self.close()  # Close splash screen
                app_main()  # Run main application
                
            except ImportError as e:
                error_msg = (
                    f"Failed to import application module:\n{str(e)}\n\n"
                    f"Tried to import 'app' from: {Path(sys._MEIPASS) / 'src'}\n\n"
                    f"Solutions:\n"
                    f"1. Rebuild the executable: build_exe.bat\n"
                    f"2. Ensure src/app.py exists in the project"
                )
                logger.error(error_msg)
                QMessageBox.critical(self, "Import Error", error_msg)
                
            except Exception as e:
                error_msg = f"Failed to launch application:\n{type(e).__name__}: {str(e)}"
                logger.exception(error_msg)
                QMessageBox.critical(self, "Launch Error", error_msg)
        
        else:
            # DEVELOPMENT MODE: Spawn subprocess to run Python file
            logger.info("Running in development mode - spawning subprocess")
            self._launch_subprocess()

    def _launch_subprocess(self) -> None:
        """
        Launch app.py in a separate subprocess (development mode only).
        
        Used when running from Python source (not bundled).
        
        Returns:
            None
        """
        base_dir = Path(__file__).parent
        app_file = base_dir / "src" / "app.py"
        
        logger.info(f"Attempting to launch subprocess: {app_file}")
        
        if not app_file.exists():
            error_msg = (
                f"Application file not found:\n{app_file}\n\n"
                f"Expected location: src/app.py\n"
                f"Base directory: {base_dir}\n\n"
                f"Solutions:\n"
                f"1. Check that src/app.py exists\n"
                f"2. Verify file structure is intact\n"
                f"3. Ensure you're running from project root"
            )
            logger.error(error_msg)
            QMessageBox.critical(self, "File Not Found", error_msg)
            return
        
        try:
            subprocess.Popen(
                [sys.executable, str(app_file)],
                cwd=str(base_dir)
            )
            logger.info("Subprocess launched successfully")
            self.close()
            
        except FileNotFoundError as e:
            error_msg = f"Python executable not found:\n{str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Python Not Found", error_msg)
            
        except Exception as e:
            error_msg = f"Failed to launch application:\n{type(e).__name__}: {str(e)}"
            logger.exception(error_msg)
            QMessageBox.critical(self, "Launch Error", error_msg)


def main() -> int:
    """
    Main entry point for the launcher application.
    
    Creates the Qt application and splash screen, then starts the
    event loop. This should be called when launcher.py is run directly.
    
    Returns:
        int: Exit code from Qt application event loop
        (0 on success, 1 on fatal error)
        
    Example:
        >>> if __name__ == "__main__":
        ...     sys.exit(main())
    """
    logger.info("=" * 70)
    logger.info("OpenModelica Simulator Launcher Started")
    logger.info("=" * 70)
    
    try:
        app = QApplication(sys.argv)
        splash = SplashScreen()
        splash.show()
        
        logger.info("Splash screen displayed, entering event loop")
        exit_code = app.exec()
        logger.info(f"Launcher exiting with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.critical(f"Fatal error in launcher main(): {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    """
    Script entry point.
    
    When this file is executed directly, run the main launcher.
    """
    exit_code = main()
    sys.exit(exit_code)
