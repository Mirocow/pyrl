"""
Pyrl VM HTTP Built-in Functions

HTTP and web-related built-in functions for the Pyrl language including:
- HTTP requests (http_get, http_post)
- URL encoding/decoding (url_encode, url_decode)
- Form parsing (parse_form)
- HTTP response helpers (html_response, json_response, redirect)
- Cookie handling (parse_cookies)
- Environment variables (env_get, env_set)
"""
from typing import Any, Dict
import json
import os
import urllib.parse

from .exceptions import PyrlRuntimeError


# Store for built-in functions (will be imported into main builtins)
HTTP_BUILTINS: Dict[str, callable] = {}


def http_builtin(name: str):
    """Decorator to register HTTP built-in functions."""
    def decorator(func: callable) -> callable:
        HTTP_BUILTINS[name] = func
        return func
    return decorator


# ===========================================
# HTTP Request Functions
# ===========================================

@http_builtin('http_get')
def pyrl_http_get(url, timeout=30):
    """Make HTTP GET request.
    
    Args:
        url: URL to request
        timeout: Request timeout in seconds
        
    Returns:
        Dict with status, data, headers, ok
    """
    try:
        import requests
        response = requests.get(url, timeout=timeout)
        return {
            'status': response.status_code,
            'data': response.text,
            'headers': dict(response.headers),
            'ok': response.ok
        }
    except ImportError:
        raise PyrlRuntimeError("HTTP functions require 'requests' library")
    except Exception as e:
        return {'status': 0, 'error': str(e), 'ok': False}


@http_builtin('http_post')
def pyrl_http_post(url, data=None, timeout=30):
    """Make HTTP POST request.
    
    Args:
        url: URL to request
        data: POST data (dict or string)
        timeout: Request timeout in seconds
        
    Returns:
        Dict with status, data, headers, ok
    """
    try:
        import requests
        response = requests.post(url, data=data, timeout=timeout)
        return {
            'status': response.status_code,
            'data': response.text,
            'headers': dict(response.headers),
            'ok': response.ok
        }
    except ImportError:
        raise PyrlRuntimeError("HTTP functions require 'requests' library")
    except Exception as e:
        return {'status': 0, 'error': str(e), 'ok': False}


# ===========================================
# URL Functions
# ===========================================

@http_builtin('url_encode')
def pyrl_url_encode(s):
    """URL encode a string.
    
    Args:
        s: String to encode
        
    Returns:
        URL-encoded string
    """
    return urllib.parse.quote(str(s))


@http_builtin('url_decode')
def pyrl_url_decode(s):
    """URL decode a string.
    
    Args:
        s: URL-encoded string
        
    Returns:
        Decoded string
    """
    return urllib.parse.unquote(str(s))


@http_builtin('parse_form')
def pyrl_parse_form(data):
    """Parse URL-encoded form data into a hash.
    
    Args:
        data: URL-encoded form data string
        
    Returns:
        Dict with parsed key-value pairs
    """
    result = {}
    if data:
        pairs = data.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[urllib.parse.unquote(key)] = urllib.parse.unquote_plus(value)
    return result


# ===========================================
# HTTP Response Helpers
# ===========================================

@http_builtin('html_response')
def pyrl_html_response(content, status=200):
    """Create an HTML response.
    
    Args:
        content: HTML content string
        status: HTTP status code
        
    Returns:
        Response dict with status, headers, body
    """
    return {
        'status': status,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': content
    }


@http_builtin('json_response')
def pyrl_json_response(data, status=200):
    """Create a JSON response.
    
    Args:
        data: Data to serialize as JSON
        status: HTTP status code
        
    Returns:
        Response dict with status, headers, body
    """
    return {
        'status': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data, default=str)
    }


@http_builtin('redirect')
def pyrl_redirect(location, permanent=False):
    """Create a redirect response.
    
    Args:
        location: URL to redirect to
        permanent: If True, use 301 (permanent) redirect
        
    Returns:
        Response dict with status, headers, body
    """
    return {
        'status': 301 if permanent else 302,
        'headers': {'Location': location},
        'body': ''
    }


# ===========================================
# Cookie Functions
# ===========================================

@http_builtin('parse_cookies')
def pyrl_parse_cookies(cookie_header):
    """Parse Cookie header into a hash.
    
    Args:
        cookie_header: Cookie header string
        
    Returns:
        Dict with cookie names and values
    """
    result = {}
    if cookie_header:
        cookies = cookie_header.split(';')
        for cookie in cookies:
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                result[key.strip()] = value.strip()
    return result


# ===========================================
# Environment Functions
# ===========================================

@http_builtin('env_get')
def pyrl_env_get(name, default=None):
    """Get environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.environ.get(name, default)


@http_builtin('env_set')
def pyrl_env_set(name, value):
    """Set environment variable.
    
    Args:
        name: Environment variable name
        value: Value to set
        
    Returns:
        The value that was set
    """
    os.environ[name] = str(value)
    return value
