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
        Launch the main application in a new process.
        
        Locates the main application file (src/app.py) relative to this
        launcher script and starts it using the Python interpreter.
        This runs the application in a separate process so the launcher
        can exit independently.
        
        Returns:
            None
            
        Error Handling:
            - Shows error dialog if app.py file is not found
            - Shows error dialog if subprocess cannot be created
            - Logs all errors for debugging
        """
        self.timer.stop()
        
        # Get path to main application file
        app_file = Path(__file__).parent / "src" / "app.py"
        
        logger.info(f"Attempting to launch: {app_file}")
        
        # Verify app file exists
        if not app_file.exists():
            error_msg = f"Application file not found:\n{app_file}\n\nExpected location: src/app.py"
            logger.error(error_msg)
            QMessageBox.critical(
                self,
                "Application Not Found",
                error_msg
            )
            return
        
        try:
            # Launch in new process
            subprocess.Popen(
                [sys.executable, str(app_file)],
                cwd=str(app_file.parent.parent)
            )
            logger.info("Main application launched successfully")
            self.close()
            
        except FileNotFoundError as e:
            error_msg = f"Python executable not found:\n{str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Python Not Found", error_msg)
            
        except PermissionError as e:
            error_msg = f"Permission denied when launching application:\n{str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Permission Error", error_msg)
            
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
