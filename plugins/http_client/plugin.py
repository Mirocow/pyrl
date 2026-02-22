# FILE: plugins/http_client/plugin.py
"""
HTTP Client Plugin for Pyrl
Provides HTTP request functions
"""

from pyrl_plugin_system import PluginBase
import urllib.request
import urllib.parse
import json


class HTTPClientPlugin(PluginBase):
    """HTTP client functions"""
    
    NAME = "http_client"
    VERSION = "1.0.0"
    DESCRIPTION = "HTTP client functions for API calls"
    AUTHOR = "Pyrl Ecosystem Team"
    
    def on_load(self):
        """Register HTTP functions"""
        self.register_function("http_get", self._get)
        self.register_function("http_post", self._post)
        self.register_function("http_put", self._put)
        self.register_function("http_delete", self._delete)
        self.register_function("json_parse", self._json_parse)
        self.register_function("json_stringify", self._json_stringify)
        self.register_function("url_encode", self._url_encode)
        self.register_function("url_decode", self._url_decode)
        self.log("HTTP client functions loaded")
    
    def _get(self, url, headers=None):
        """HTTP GET request"""
        req = urllib.request.Request(url, method='GET')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    
    def _post(self, url, data, headers=None):
        """HTTP POST request"""
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    
    def _put(self, url, data, headers=None):
        """HTTP PUT request"""
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method='PUT')
        req.add_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    
    def _delete(self, url, headers=None):
        """HTTP DELETE request"""
        req = urllib.request.Request(url, method='DELETE')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    
    def _json_parse(self, s):
        """Parse JSON string"""
        return json.loads(s)
    
    def _json_stringify(self, obj, indent=None):
        """Convert object to JSON string"""
        if indent:
            return json.dumps(obj, indent=indent, ensure_ascii=False)
        return json.dumps(obj, ensure_ascii=False)
    
    def _url_encode(self, s):
        """URL encode string"""
        return urllib.parse.quote(s)
    
    def _url_decode(self, s):
        """URL decode string"""
        return urllib.parse.unquote(s)


# Export plugin class
plugin_class = HTTPClientPlugin
