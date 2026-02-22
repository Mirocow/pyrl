#!/usr/bin/env python3
"""
Pyrl API Server - Standalone Docker-ready API server.

This module provides a complete standalone API server for Pyrl,
optimized for Docker deployment with all dependencies bundled.

Usage:
    python api_server.py
    python api_server.py --port 8080
    python api_server.py --host 0.0.0.0 --port 8000 --workers 4

Environment Variables:
    PYRL_HOST         - Server host (default: 0.0.0.0)
    PYRL_PORT         - Server port (default: 8000)
    PYRL_DEBUG        - Debug mode (default: false)
    PYRL_LOG_LEVEL    - Log level (default: info)
    PYRL_WORKERS      - Number of workers (default: 1)
    PYRL_PLUGINS_PATH - Path to plugins (optional)
"""
import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, HTMLResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "fastapi", "uvicorn", "pydantic"])
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, HTMLResponse
    from pydantic import BaseModel, Field
    import uvicorn

from src.core.vm import PyrlVM
from src.core.lexer import tokenize
from src.core.parser import parse
from src.core.exceptions import PyrlError
from src.core.builtins import load_builtin_plugins, get_loaded_plugins


# ===========================================
# Configuration
# ===========================================

class Config:
    """Server configuration from environment."""
    
    def __init__(self):
        self.host = os.getenv('PYRL_HOST', '0.0.0.0')
        self.port = int(os.getenv('PYRL_PORT', '8000'))
        self.debug = os.getenv('PYRL_DEBUG', 'false').lower() == 'true'
        self.log_level = os.getenv('PYRL_LOG_LEVEL', 'info')
        self.workers = int(os.getenv('PYRL_WORKERS', '1'))
        self.plugins_path = os.getenv('PYRL_PLUGINS_PATH', '')


config = Config()

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pyrl-api-server")


# ===========================================
# Request/Response Models
# ===========================================

class ExecuteRequest(BaseModel):
    """Request model for code execution."""
    code: str = Field(..., description="Pyrl source code to execute")
    reset: bool = Field(False, description="Reset VM before execution")
    timeout: int = Field(30, description="Execution timeout in seconds", ge=1, le=300)


class ExecuteResponse(BaseModel):
    """Response model for code execution."""
    success: bool = Field(..., description="Whether execution succeeded")
    result: Optional[str] = Field(None, description="String representation of result")
    output: str = Field("", description="Captured stdout output")
    error: Optional[str] = Field(None, description="Error message if failed")
    error_type: Optional[str] = Field(None, description="Error type if failed")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Current variables")
    execution_time_ms: float = Field(0, description="Execution time in milliseconds")


class TokenizeRequest(BaseModel):
    """Request model for tokenization."""
    code: str = Field(..., description="Pyrl source code to tokenize")


class TokenizeResponse(BaseModel):
    """Response model for tokenization."""
    tokens: List[Dict[str, Any]] = Field(..., description="List of tokens")
    count: int = Field(..., description="Number of tokens")


class ParseRequest(BaseModel):
    """Request model for parsing."""
    code: str = Field(..., description="Pyrl source code to parse")


class ParseResponse(BaseModel):
    """Response model for parsing."""
    ast: Dict[str, Any] = Field(..., description="AST representation")
    statements_count: int = Field(..., description="Number of statements")


class PluginLoadRequest(BaseModel):
    """Request model for loading a plugin."""
    name: str = Field(..., description="Plugin name to load")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="Server version")
    uptime_seconds: float = Field(..., description="Server uptime")
    plugins_loaded: int = Field(..., description="Number of loaded plugins")


# ===========================================
# FastAPI Application
# ===========================================

app = FastAPI(
    title="Pyrl API Server",
    description="""
A hybrid Python-Perl inspired language interpreter server.

## Features
- **Sigil Variables**: $scalar, @array, %hash, &function
- **Python-style Syntax**: Indentation-based blocks
- **Dynamic Typing**: Runtime type checking
- **Built-in Functions**: Rich standard library
- **Plugin System**: Extensible architecture
- **HTTP/JSON**: Built-in web request support

## Quick Start
```python
# Execute code
POST /execute
{
    "code": "$x = 10\\nprint($x)"
}

# Tokenize code
POST /tokenize
{
    "code": "$x = 10"
}
```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================
# VM Manager
# ===========================================

class VMManager:
    """Manages Pyrl VM instances."""
    
    def __init__(self):
        self.vm = PyrlVM(debug=config.debug)
        self.start_time = datetime.now()
        self.request_count = 0
        # Load built-in plugins
        load_builtin_plugins(self.vm.env)
    
    def get_vm(self) -> PyrlVM:
        """Get the current VM instance."""
        return self.vm
    
    def reset(self) -> None:
        """Reset the VM."""
        self.vm.reset()
        load_builtin_plugins(self.vm.env)
    
    def uptime(self) -> float:
        """Get server uptime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    def increment_requests(self) -> int:
        """Increment and return request count."""
        self.request_count += 1
        return self.request_count


vm_manager = VMManager()


# ===========================================
# Exception Handlers
# ===========================================

@app.exception_handler(PyrlError)
async def pyrl_exception_handler(request: Request, exc: PyrlError):
    """Handle Pyrl-specific exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "error_type": type(exc).__name__
        }
    )


# ===========================================
# Routes
# ===========================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with server info."""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Pyrl API Server</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
        }
        h1 { color: #00d4ff; }
        h2 { color: #00ff88; margin-top: 30px; }
        code {
            background: #16213e;
            padding: 2px 6px;
            border-radius: 4px;
            color: #ff6b6b;
        }
        pre {
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }
        .endpoint {
            background: #0f3460;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .method {
            font-weight: bold;
            color: #00d4ff;
        }
        a { color: #00d4ff; }
    </style>
</head>
<body>
    <h1>Pyrl API Server</h1>
    <p>A hybrid Python-Perl inspired language interpreter.</p>
    
    <h2>Quick Start</h2>
    <pre>
curl -X POST http://localhost:8000/execute \\
    -H "Content-Type: application/json" \\
    -d '{"code": "$x = 10\\nprint($x)"}'
    </pre>
    
    <h2>API Endpoints</h2>
    <div class="endpoint"><span class="method">GET</span> /health - Health check</div>
    <div class="endpoint"><span class="method">POST</span> /execute - Execute Pyrl code</div>
    <div class="endpoint"><span class="method">POST</span> /tokenize - Tokenize code</div>
    <div class="endpoint"><span class="method">POST</span> /parse - Parse code to AST</div>
    <div class="endpoint"><span class="method">POST</span> /reset - Reset VM state</div>
    <div class="endpoint"><span class="method">GET</span> /variables - Get all variables</div>
    <div class="endpoint"><span class="method">GET</span> /plugins - Get loaded plugins</div>
    <div class="endpoint"><span class="method">POST</span> /plugins/load - Load a plugin</div>
    <div class="endpoint"><span class="method">GET</span> /config - Get configuration</div>
    
    <h2>Documentation</h2>
    <p><a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
    
    <h2>Features</h2>
    <ul>
        <li><code>$scalar</code> - Scalar variables</li>
        <li><code>@array</code> - Array variables</li>
        <li><code>%hash</code> - Hash/dict variables</li>
        <li><code>&func</code> - Function references</li>
    </ul>
</body>
</html>
    """
    return HTMLResponse(content=html)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=vm_manager.uptime(),
        plugins_loaded=len(get_loaded_plugins())
    )


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    """Execute Pyrl code."""
    import time
    import io
    from contextlib import redirect_stdout
    
    vm = vm_manager.get_vm()
    
    if request.reset:
        vm.reset()
    
    start_time = time.time()
    output_buffer = io.StringIO()
    
    try:
        with redirect_stdout(output_buffer):
            result = vm.run(request.code)
        
        execution_time = (time.time() - start_time) * 1000
        
        return ExecuteResponse(
            success=True,
            result=str(result) if result is not None else None,
            output=output_buffer.getvalue(),
            variables=vm.get_globals(),
            execution_time_ms=execution_time
        )
        
    except PyrlError as e:
        execution_time = (time.time() - start_time) * 1000
        logger.warning(f"Pyrl execution error: {e}")
        
        return ExecuteResponse(
            success=False,
            output=output_buffer.getvalue(),
            error=str(e),
            error_type=type(e).__name__,
            variables=vm.get_globals(),
            execution_time_ms=execution_time
        )
    
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.error(f"Execution error: {e}", exc_info=True)
        
        return ExecuteResponse(
            success=False,
            output=output_buffer.getvalue(),
            error=str(e),
            error_type=type(e).__name__,
            variables=vm.get_globals(),
            execution_time_ms=execution_time
        )


@app.post("/tokenize", response_model=TokenizeResponse)
async def tokenize_code(request: TokenizeRequest):
    """Tokenize Pyrl code."""
    try:
        tokens = tokenize(request.code)
        
        token_list = [
            {
                "type": t.type.value,
                "value": t.value,
                "line": t.line,
                "column": t.column
            }
            for t in tokens
        ]
        
        return TokenizeResponse(
            tokens=token_list,
            count=len(token_list)
        )
        
    except PyrlError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/parse", response_model=ParseResponse)
async def parse_code(request: ParseRequest):
    """Parse Pyrl code to AST."""
    try:
        tokens = tokenize(request.code)
        ast = parse(tokens)
        
        def ast_to_dict(node):
            if hasattr(node, '__dataclass_fields__'):
                result = {"type": type(node).__name__}
                for field in node.__dataclass_fields__:
                    value = getattr(node, field)
                    if isinstance(value, list):
                        result[field] = [ast_to_dict(item) for item in value]
                    elif hasattr(value, '__dataclass_fields__'):
                        result[field] = ast_to_dict(value)
                    else:
                        result[field] = value
                return result
            return str(node)
        
        ast_dict = ast_to_dict(ast)
        
        return ParseResponse(
            ast=ast_dict,
            statements_count=len(ast.statements)
        )
        
    except PyrlError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset")
async def reset():
    """Reset the VM state."""
    vm_manager.reset()
    return {"status": "reset", "message": "VM state cleared"}


@app.get("/variables")
async def get_variables():
    """Get all current variables in the VM."""
    vm = vm_manager.get_vm()
    variables = vm.get_globals()
    
    filtered = {
        k: str(v) for k, v in variables.items()
        if k not in ('True', 'False', 'None', 'PI', 'E', 'INF', 'NAN')
        and not k.startswith('_')
    }
    
    return {
        "variables": filtered,
        "count": len(filtered)
    }


@app.get("/plugins")
async def get_plugins():
    """Get all loaded plugins."""
    plugins = get_loaded_plugins()
    return {
        "plugins": plugins,
        "count": len(plugins)
    }


@app.post("/plugins/load")
async def load_plugin(request: PluginLoadRequest):
    """Load a plugin by name."""
    try:
        from src.core.builtins import _plugin_loader
        exports = _plugin_loader.load_plugin(request.name)
        
        # Register in VM environment
        for name, value in exports.items():
            full_name = f"{request.name}_{name}"
            vm_manager.get_vm().env.define(full_name, value)
        
        return {
            "status": "loaded",
            "plugin": request.name,
            "exports": list(exports.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/config")
async def get_config():
    """Get server configuration."""
    return {
        "host": config.host,
        "port": config.port,
        "debug": config.debug,
        "log_level": config.log_level,
        "workers": config.workers,
        "plugins_path": config.plugins_path
    }


@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    return {
        "uptime_seconds": vm_manager.uptime(),
        "request_count": vm_manager.request_count,
        "variables_count": len(vm_manager.get_vm().get_globals()),
        "plugins_count": len(get_loaded_plugins())
    }


# ===========================================
# Startup/Shutdown Events
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Run on server startup."""
    logger.info(f"Pyrl API Server starting on {config.host}:{config.port}")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"Loaded plugins: {list(get_loaded_plugins().keys())}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown."""
    logger.info("Pyrl API Server shutting down")


# ===========================================
# Main Entry Point
# ===========================================

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Pyrl API Server')
    parser.add_argument('--host', default=config.host, help='Server host')
    parser.add_argument('--port', type=int, default=config.port, help='Server port')
    parser.add_argument('--workers', type=int, default=config.workers, help='Number of workers')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--log-level', default=config.log_level, help='Log level')
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    uvicorn.run(
        "api_server:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        reload=args.debug,
        log_level=args.log_level.lower()
    )


if __name__ == "__main__":
    main()
