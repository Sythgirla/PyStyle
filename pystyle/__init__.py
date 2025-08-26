"""
PyStyle - Dynamic Editing of Styles and Colors in Python TK+TTK.
"""
from .core import StyleFactory, bodyFont, headerFont, buttonFont, optionFont
from .settings_app import launch_settings

__version__ = "1.0.0"
__author__ = "Sythgirla"
__all__ = ['StyleFactory',
           'bodyFont', 'headerFont', 'buttonFont', 'optionFont',
           'launch_settings',]