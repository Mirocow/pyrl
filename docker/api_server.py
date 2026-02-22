# FILE: docker/api_server.py
"""
Pyrl API Server
FastAPI-based REST API for Pyrl code execution

Endpoints:
- POST /execute - Execute Pyrl code
- POST /test - Run tests
- POST /generate - AI code generation
- GET /plugins - List available plugins
- GET /health - Health check
"""

import sys
import os
sys.path.insert(0, '/app/src')

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import traceback

from pyrl_vm import PyrlVM, PyrlSyntaxError, PyrlRuntimeError
from pyrl_plugin_system import PluginManager, load_builtin_plugins
from pyrl_ai import PyrlAI


# Initialize FastAPI app
app = FastAPI(
    title="Pyrl API",
    description="REST API for Pyrl code execution and AI generation",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ExecuteRequest(BaseModel):
    code: str
    reset: bool = False


class ExecuteResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    memory: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TestRequest(BaseModel):
    code: str


class TestResponse(BaseModel):
    total: int
    passed: int
    failed: int
    success_rate: float
    results: List[Dict[str, Any]]


class GenerateRequest(BaseModel):
    prompt: str
    context: Optional[str] = None


class GenerateResponse(BaseModel):
    success: bool
    code: str
    explanation: str
    plugins_needed: List[str]


class PluginInfo(BaseModel):
    name: str
    version: str
    description: str
    functions: List[str]


# Global instances
vm = None
ai = None
plugin_manager = None


def get_vm() -> PyrlVM:
    """Get or create VM instance"""
    global vm, plugin_manager
    
    if vm is None:
        vm = PyrlVM()
        plugin_manager = PluginManager(vm)
        load_builtin_plugins(plugin_manager)
    
    return vm


def get_ai() -> PyrlAI:
    """Get or create AI instance"""
    global ai, vm
    
    if ai is None:
        vm_instance = get_vm()
        ai = PyrlAI(vm_instance)
    
    return ai


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Pyrl API",
        "version": "2.0.0",
        "endpoints": ["/execute", "/test", "/generate", "/plugins", "/health"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "plugins_loaded": plugin_manager is not None
    }


@app.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """Execute Pyrl code"""
    try:
        vm_instance = get_vm()
        
        if request.reset:
            vm_instance.reset()
        
        result = vm_instance.execute(request.code)
        
        # Get memory state
        memory = {
            "scalars": vm_instance.memory['scalars'],
            "arrays": {k: v for k, v in vm_instance.memory['arrays'].items()},
            "hashes": {k: v for k, v in vm_instance.memory['hashes'].items()},
        }
        
        return ExecuteResponse(
            success=True,
            result=str(result) if result else None,
            memory=memory
        )
    
    except PyrlSyntaxError as e:
        return ExecuteResponse(
            success=False,
            error=f"Syntax Error: {str(e)}"
        )
    
    except PyrlRuntimeError as e:
        return ExecuteResponse(
            success=False,
            error=f"Runtime Error: {str(e)}"
        )
    
    except Exception as e:
        return ExecuteResponse(
            success=False,
            error=f"Error: {str(e)}\n{traceback.format_exc()}"
        )


@app.post("/test", response_model=TestResponse)
async def run_tests(request: TestRequest):
    """Run Pyrl tests"""
    try:
        vm_instance = get_vm()
        vm_instance.reset()
        
        results = vm_instance.run_tests(request.code)
        summary = vm_instance.get_test_summary()
        
        return TestResponse(
            total=summary['total'],
            passed=summary['passed'],
            failed=summary['failed'],
            success_rate=summary['success_rate'],
            results=[
                {
                    "name": r.name,
                    "success": r.success,
                    "message": r.message,
                    "expected": r.expected,
                    "actual": r.actual
                }
                for r in results
            ]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """Generate Pyrl code from natural language"""
    try:
        ai_instance = get_ai()
        result = ai_instance.generate_code(request.prompt)
        
        return GenerateResponse(
            success=result.success,
            code=result.code,
            explanation=result.explanation,
            plugins_needed=result.plugins_needed
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/plugins", response_model=List[PluginInfo])
async def list_plugins():
    """List available plugins"""
    global plugin_manager
    
    if plugin_manager is None:
        get_vm()
    
    plugins = []
    for plugin in plugin_manager.list_plugins():
        plugins.append(PluginInfo(
            name=plugin.name,
            version=plugin.version,
            description=plugin.description,
            functions=list(plugin.functions) if hasattr(plugin, 'functions') else []
        ))
    
    return plugins


@app.get("/plugins/{plugin_name}")
async def get_plugin_info(plugin_name: str):
    """Get information about a specific plugin"""
    global plugin_manager
    
    if plugin_manager is None:
        get_vm()
    
    info = plugin_manager.get_plugin_info(plugin_name)
    if info is None:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    return {
        "name": info.name,
        "version": info.version,
        "description": info.description,
        "author": info.author,
        "state": info.state.value
    }


@app.post("/reset")
async def reset_vm():
    """Reset the VM state"""
    global vm
    if vm:
        vm.reset()
    return {"status": "reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
