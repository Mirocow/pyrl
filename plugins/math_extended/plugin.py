# FILE: plugins/math_extended/plugin.py
"""
Math Extended Plugin for Pyrl
Provides advanced mathematical functions
"""

from pyrl_plugin_system import PluginBase
import math


class MathExtendedPlugin(PluginBase):
    """Extended mathematical functions"""
    
    NAME = "math_extended"
    VERSION = "1.0.0"
    DESCRIPTION = "Extended mathematical functions"
    AUTHOR = "Pyrl Ecosystem Team"
    
    def on_load(self):
        """Register math functions"""
        self.register_function("sqrt", self._sqrt)
        self.register_function("pow", self._pow)
        self.register_function("log", self._log)
        self.register_function("log10", self._log10)
        self.register_function("log2", self._log2)
        self.register_function("sin", self._sin)
        self.register_function("cos", self._cos)
        self.register_function("tan", self._tan)
        self.register_function("asin", self._asin)
        self.register_function("acos", self._acos)
        self.register_function("atan", self._atan)
        self.register_function("pi", self._pi)
        self.register_function("e", self._e)
        self.register_function("floor", self._floor)
        self.register_function("ceil", self._ceil)
        self.register_function("degrees", self._degrees)
        self.register_function("radians", self._radians)
        self.log("Math functions loaded")
    
    def _sqrt(self, x):
        """Square root"""
        return math.sqrt(x)
    
    def _pow(self, base, exp):
        """Power function"""
        return math.pow(base, exp)
    
    def _log(self, x, base=None):
        """Natural logarithm or logarithm with base"""
        if base:
            return math.log(x, base)
        return math.log(x)
    
    def _log10(self, x):
        """Base 10 logarithm"""
        return math.log10(x)
    
    def _log2(self, x):
        """Base 2 logarithm"""
        return math.log2(x)
    
    def _sin(self, x):
        """Sine function (radians)"""
        return math.sin(x)
    
    def _cos(self, x):
        """Cosine function (radians)"""
        return math.cos(x)
    
    def _tan(self, x):
        """Tangent function (radians)"""
        return math.tan(x)
    
    def _asin(self, x):
        """Arc sine"""
        return math.asin(x)
    
    def _acos(self, x):
        """Arc cosine"""
        return math.acos(x)
    
    def _atan(self, x):
        """Arc tangent"""
        return math.atan(x)
    
    def _pi(self):
        """Pi constant"""
        return math.pi
    
    def _e(self):
        """Euler's number"""
        return math.e
    
    def _floor(self, x):
        """Floor function"""
        return math.floor(x)
    
    def _ceil(self, x):
        """Ceiling function"""
        return math.ceil(x)
    
    def _degrees(self, x):
        """Convert radians to degrees"""
        return math.degrees(x)
    
    def _radians(self, x):
        """Convert degrees to radians"""
        return math.radians(x)


# Export plugin class
plugin_class = MathExtendedPlugin
