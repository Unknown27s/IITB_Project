"""
OpenModelica Simulator - Application Launcher
Simple wrapper to launch the main application with splash screen

Original development with GitHub Copilot
Professional launcher system with splash screen and countdown
"""

import sys
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor
from PyQt6.QtCore import QSize


class SplashScreen(QDialog):
    """Splash screen / launcher window"""
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.auto_close_counter = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize the launcher UI"""
        self.setWindowTitle("OpenModelica Simulator Launcher")
        self.setGeometry(500, 300, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
        """)
        self.setWindowIcon(QIcon.fromTheme("system-run"))
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("OpenModelica")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Model Simulator")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #ddd;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Spacer
        layout.addSpacing(20)
        
        # Description
        desc = QLabel(
            "Two Connected Tanks Simulation\n\n"
            "Click 'Launch' to start the application\n"
            "or wait 5 seconds for automatic launch"
        )
        desc_font = QFont()
        desc_font.setPointSize(10)
        desc.setFont(desc_font)
        desc.setStyleSheet("color: #fff;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Launch Button
        launch_btn = QPushButton("▶ LAUNCH APPLICATION")
        launch_btn.setMinimumHeight(50)
        launch_font = QFont()
        launch_font.setPointSize(12)
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
        launch_btn.clicked.connect(self.launch_app)
        layout.addWidget(launch_btn)
        
        # Auto-launch timer
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000)
        self.auto_close_counter = 5
        
        # Auto-launch label
        self.auto_label = QLabel("Auto-launching in 5s...")
        auto_font = QFont()
        auto_font.setPointSize(9)
        self.auto_label.setFont(auto_font)
        self.auto_label.setStyleSheet("color: #ccc;")
        self.auto_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.auto_label)
        
        self.setLayout(layout)
    
    def on_timer(self):
        """Timer callback for auto-launch countdown"""
        self.auto_close_counter -= 1
        self.auto_label.setText(f"Auto-launching in {self.auto_close_counter}s..." if self.auto_close_counter > 0 else "Launching...")
        
        if self.auto_close_counter <= 0:
            self.timer.stop()
            self.launch_app()
    
    def launch_app(self):
        """Launch the main application"""
        self.timer.stop()
        
        # Get the main app path
        app_file = Path(__file__).parent / "src" / "app.py"
        
        if not app_file.exists():
            QMessageBox.critical(
                self,
                "Error",
                f"Application file not found:\n{app_file}"
            )
            return
        
        try:
            # Launch the main app in a new process
            if sys.platform == "win32":
                # Windows
                subprocess.Popen(
                    [sys.executable, str(app_file)],
                    cwd=str(Path(__file__).parent)
                )
            else:
                # Linux/Mac
                subprocess.Popen(
                    [sys.executable, str(app_file)],
                    cwd=str(Path(__file__).parent)
                )
            
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Launch Error",
                f"Failed to launch application:\n{str(e)}"
            )


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
