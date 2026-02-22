"""
Pyrl Language Server
FastAPI-based server for the Pyrl language interpreter.

Provides REST API endpoints for:
- Code execution
- Tokenization
- AST parsing
- Variable management
- Health monitoring

Usage:
    # Development mode
    python pyrl_server.py
    
    # Production mode with uvicorn
    uvicorn pyrl_server:app --host 0.0.0.0 --port 8000

Endpoints:
    GET  /              - Server info
    GET  /health        - Health check
    POST /execute       - Execute Pyrl code
    POST /tokenize      - Tokenize code
    POST /parse         - Parse code to AST
    POST /reset         - Reset VM state
    GET  /variables     - Get all variables
    GET  /config        - Get server configuration
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.vm import PyrlVM
from src.core.lexer import tokenize
from src.core.parser import parse
from src.core.exceptions import PyrlError
from src.config import get_config


# ===========================================
# Configuration
# ===========================================

config = get_config()

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pyrl-server")


# ===========================================
# FastAPI Application
# ===========================================

app = FastAPI(
    title="Pyrl Language Server",
    description="""
A hybrid Python-Perl inspired language interpreter server.

## Features
- **Sigil Variables**: $scalar, @array, %hash, &function
- **Python-style Syntax**: Indentation-based blocks
- **Dynamic Typing**: Runtime type checking
- **Built-in Functions**: Rich standard library

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


class VariableResponse(BaseModel):
    """Response model for variable listing."""
    variables: Dict[str, Any] = Field(..., description="All variables")
    count: int = Field(..., description="Number of variables")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="Server version")
    uptime_seconds: float = Field(..., description="Server uptime")


# ===========================================
# VM Manager
# ===========================================

class VMManager:
    """Manages Pyrl VM instances."""
    
    def __init__(self):
        self.vm = PyrlVM(debug=config.debug)
        self.start_time = datetime.now()
        self.request_count = 0
    
    def get_vm(self) -> PyrlVM:
        """Get the current VM instance."""
        return self.vm
    
    def reset(self) -> None:
        """Reset the VM."""
        self.vm.reset()
    
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
    <title>Pyrl Language Server</title>
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
    <h1>🚀 Pyrl Language Server</h1>
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
        uptime=vm_manager.uptime()
    )


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    """
    Execute Pyrl code.
    
    - **code**: Pyrl source code to execute
    - **reset**: Reset VM before execution (default: false)
    - **timeout**: Execution timeout in seconds (default: 30)
    """
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
            variables=vm.get_globals()
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
    """
    Tokenize Pyrl code.
    
    Returns a list of tokens with their types, values, and positions.
    """
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
    """
    Parse Pyrl code to AST.
    
    Returns the abstract syntax tree representation.
    """
    try:
        tokens = tokenize(request.code)
        ast = parse(tokens)
        
        # Convert AST to dict
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
    """Reset the VM state, clearing all variables."""
    vm_manager.reset()
    return {"status": "reset", "message": "VM state cleared"}


@app.get("/variables", response_model=VariableResponse)
async def get_variables():
    """Get all current variables in the VM."""
    vm = vm_manager.get_vm()
    variables = vm.get_globals()
    
    # Filter out built-in constants
    filtered = {
        k: v for k, v in variables.items()
        if k not in ('True', 'False', 'None', 'PI', 'E', 'INF', 'NAN')
        and not k.startswith('_')
    }
    
    return VariableResponse(
        variables=filtered,
        count=len(filtered)
    )


@app.get("/config")
async def get_config_endpoint():
    """Get server configuration."""
    return {
        "debug": config.debug,
        "log_level": config.log_level,
        "data_dir": str(config.data_dir),
        "models_dir": str(config.models_dir),
        "examples_dir": str(config.examples_dir),
        "server": {
            "host": config.server_host,
            "port": config.server_port
        }
    }


@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    return {
        "uptime_seconds": vm_manager.uptime(),
        "request_count": vm_manager.request_count,
        "variables_count": len(vm_manager.get_vm().get_globals())
    }


# ===========================================
# Startup/Shutdown Events
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Run on server startup."""
    logger.info(f"Pyrl Server starting on {config.server_host}:{config.server_port}")
    logger.info(f"Debug mode: {config.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown."""
    logger.info("Pyrl Server shutting down")


# ===========================================
# Main Entry Point
# ===========================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "pyrl_server:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.debug,
        log_level=config.log_level.lower()
    )
