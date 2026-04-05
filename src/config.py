"""
Configuration module for OpenModelica Simulator

This module defines all configuration constants and application settings
using a configuration class pattern. This follows OOP principles by
centralizing configuration management and making the application more
maintainable and testable.

Example:
    >>> config = SimulatorConfig()
    >>> print(config.WINDOW_WIDTH)
    700
    >>> print(config.DEFAULT_START_TIME)
    5.1
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class SimulatorConfig:
    """
    Configuration class for OpenModelica Simulator application.
    
    This class uses Python dataclass to manage all application settings
    including UI dimensions, default values, timing parameters, and
    styling. Centralizing configuration here improves:
    - Code maintainability
    - Testability (easy to mock different configs)
    - Scalability (settings can be loaded from files)
    
    Attributes:
        WINDOW_WIDTH (int): Main window width in pixels
        WINDOW_HEIGHT (int): Main window height in pixels
        WINDOW_X_POS (int): Initial window X position
        WINDOW_Y_POS (int): Initial window Y position
        WINDOW_TITLE (str): Main application window title
        
        DEFAULT_START_TIME (float): Default simulation start time (seconds)
        DEFAULT_STOP_TIME (float): Default simulation stop time (seconds)
        MIN_TIME_VALUE (float): Minimum allowed time value
        MAX_TIME_VALUE (float): Maximum allowed time value
        TIME_DECIMALS (int): Decimal places for time input fields
        
        BUTTON_MIN_HEIGHT (int): Minimum height for control buttons (pixels)
        BUTTON_FONT_SIZE (int): Font size for buttons
        TITLE_FONT_SIZE (int): Font size for title text
        OUTPUT_FONT_NAME (str): Font family for output display
        OUTPUT_FONT_SIZE (int): Font size for output text
        
        SPLASH_WIDTH (int): Splash screen width (pixels)
        SPLASH_HEIGHT (int): Splash screen height (pixels)
        SPLASH_X_POS (int): Splash screen X position
        SPLASH_Y_POS (int): Splash screen Y position
        AUTO_CLOSE_SECONDS (int): Splash auto-close timeout (seconds)
    """
    
    # Window configuration
    WINDOW_WIDTH: int = 700
    WINDOW_HEIGHT: int = 500
    WINDOW_X_POS: int = 100
    WINDOW_Y_POS: int = 100
    WINDOW_TITLE: str = "OpenModelica Simulator"
    
    # Simulation time defaults
    DEFAULT_START_TIME: float = 5.1
    DEFAULT_STOP_TIME: float = 100.0
    MIN_TIME_VALUE: float = 0.0
    MAX_TIME_VALUE: float = 999999.0
    TIME_DECIMALS: int = 2
    
    # UI component sizing
    BUTTON_MIN_HEIGHT: int = 40
    BUTTON_FONT_SIZE: int = 10
    TITLE_FONT_SIZE: int = 12
    OUTPUT_FONT_NAME: str = "Courier"
    OUTPUT_FONT_SIZE: int = 9
    
    # Splash screen
    SPLASH_WIDTH: int = 400
    SPLASH_HEIGHT: int = 300
    SPLASH_X_POS: int = 500
    SPLASH_Y_POS: int = 300
    AUTO_CLOSE_SECONDS: int = 5
    
    # Styling
    LAUNCH_BUTTON_STYLE: str = """
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
    """
    
    SPLASH_BACKGROUND: str = """
        QDialog {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    """

    @classmethod
    def get_model_executable_path(cls) -> Path:
        """
        Get the default path to the OpenModelica executable.
        
        Returns:
            Path: Path to TwoConnectedTanks.exe relative to project structure
            
        Example:
            >>> exe_path = SimulatorConfig.get_model_executable_path()
            >>> print(exe_path.name)
            'TwoConnectedTanks.exe'
        """
        # Navigate from src/config.py -> model/TwoConnectedTanks.exe
        exe = Path(__file__).parent.parent / "model" / "TwoConnectedTanks.exe"
        return exe

    @classmethod
    def validate_time_range(cls, start_time: float, stop_time: float) -> Tuple[bool, str]:
        """
        Validate simulation time range.
        
        Ensures that:
        - start_time < stop_time
        - Both times are within allowed range
        
        Args:
            start_time (float): Simulation start time in seconds
            stop_time (float): Simulation stop time in seconds
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
            
        Example:
            >>> is_valid, msg = SimulatorConfig.validate_time_range(0, 10)
            >>> print(is_valid)
            True
            >>> is_valid, msg = SimulatorConfig.validate_time_range(10, 5)
            >>> print(is_valid, msg)
            False "Start time must be less than stop time"
        """
        if start_time >= stop_time:
            return False, "Start time must be less than stop time"
        
        if start_time < cls.MIN_TIME_VALUE or stop_time > cls.MAX_TIME_VALUE:
            return False, f"Time values must be between {cls.MIN_TIME_VALUE} and {cls.MAX_TIME_VALUE}"
        
        return True, ""


# Default configuration instance
DEFAULT_CONFIG = SimulatorConfig()
