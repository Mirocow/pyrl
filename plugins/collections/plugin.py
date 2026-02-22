# FILE: plugins/collections/plugin.py
"""
Collections Plugin for Pyrl
Provides advanced collection manipulation functions
"""

from pyrl_plugin_system import PluginBase
from collections import Counter


class CollectionsPlugin(PluginBase):
    """Collection manipulation functions"""
    
    NAME = "collections"
    VERSION = "1.0.0"
    DESCRIPTION = "Advanced collection manipulation functions"
    AUTHOR = "Pyrl Ecosystem Team"
    
    def on_load(self):
        """Register collection functions"""
        self.register_function("flatten", self._flatten)
        self.register_function("unique", self._unique)
        self.register_function("intersection", self._intersection)
        self.register_function("difference", self._difference)
        self.register_function("union", self._union)
        self.register_function("zip_arrays", self._zip_arrays)
        self.register_function("chunk", self._chunk)
        self.register_function("count_by", self._count_by)
        self.register_function("find", self._find)
        self.register_function("find_index", self._find_index)
        self.register_function("every", self._every)
        self.register_function("some", self._some)
        self.register_function("take", self._take)
        self.register_function("drop", self._drop)
        self.register_function("without", self._without)
        self.log("Collections functions loaded")
    
    def _flatten(self, arr, depth=1):
        """Flatten nested array"""
        result = []
        for item in arr:
            if isinstance(item, list) and depth > 0:
                result.extend(self._flatten(item, depth - 1))
            else:
                result.append(item)
        return result
    
    def _unique(self, arr):
        """Remove duplicates from array"""
        seen = []
        result = []
        for item in arr:
            # Use JSON for complex types
            import json
            key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            if key not in seen:
                seen.append(key)
                result.append(item)
        return result
    
    def _intersection(self, *arrays):
        """Get intersection of arrays"""
        if not arrays:
            return []
        result = set(arrays[0])
        for arr in arrays[1:]:
            result &= set(arr)
        return list(result)
    
    def _difference(self, *arrays):
        """Get difference of arrays"""
        if not arrays:
            return []
        result = set(arrays[0])
        for arr in arrays[1:]:
            result -= set(arr)
        return list(result)
    
    def _union(self, *arrays):
        """Get union of arrays"""
        result = set()
        for arr in arrays:
            result |= set(arr)
        return list(result)
    
    def _zip_arrays(self, *arrays):
        """Zip arrays together"""
        return list(zip(*arrays))
    
    def _chunk(self, arr, size):
        """Split array into chunks"""
        return [arr[i:i + size] for i in range(0, len(arr), size)]
    
    def _count_by(self, arr, key_func=None):
        """Count occurrences in array"""
        if key_func is None:
            return dict(Counter(arr))
        # If key_func is a string, use it as a key for dicts
        if isinstance(key_func, str):
            counted = {}
            for item in arr:
                if isinstance(item, dict):
                    k = item.get(key_func)
                    counted[k] = counted.get(k, 0) + 1
            return counted
        return dict(Counter(arr))
    
    def _find(self, arr, predicate):
        """Find first matching element (predicate as value for simple comparison)"""
        for item in arr:
            if isinstance(predicate, dict):
                if isinstance(item, dict):
                    match = all(item.get(k) == v for k, v in predicate.items())
                    if match:
                        return item
            elif item == predicate:
                return item
        return None
    
    def _find_index(self, arr, predicate):
        """Find index of first matching element"""
        for i, item in enumerate(arr):
            if isinstance(predicate, dict):
                if isinstance(item, dict):
                    match = all(item.get(k) == v for k, v in predicate.items())
                    if match:
                        return i
            elif item == predicate:
                return i
        return -1
    
    def _every(self, arr, predicate=None):
        """Check if all elements pass predicate"""
        if predicate is None:
            return all(arr)
        for item in arr:
            if isinstance(predicate, dict):
                if isinstance(item, dict):
                    if not all(item.get(k) == v for k, v in predicate.items()):
                        return False
            elif item != predicate:
                return False
        return True
    
    def _some(self, arr, predicate=None):
        """Check if any element passes predicate"""
        if predicate is None:
            return any(arr)
        for item in arr:
            if isinstance(predicate, dict):
                if isinstance(item, dict):
                    if all(item.get(k) == v for k, v in predicate.items()):
                        return True
            elif item == predicate:
                return True
        return False
    
    def _take(self, arr, n):
        """Take first n elements"""
        return arr[:n]
    
    def _drop(self, arr, n):
        """Drop first n elements"""
        return arr[n:]
    
    def _without(self, arr, *values):
        """Remove values from array"""
        return [item for item in arr if item not in values]


# Export plugin class
plugin_class = CollectionsPlugin
