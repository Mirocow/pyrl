"""
Pyrl VM Database Built-in Functions

SQLite database built-in functions for the Pyrl language including:
- Connection management (db_connect, db_close)
- Query execution (db_execute, db_query, db_query_one)
- Transaction support (db_begin, db_commit, db_rollback)
- Introspection (db_tables)
"""
from typing import Any, Dict, List, Optional

from .exceptions import PyrlRuntimeError


# Store for database connections
_db_connections: Dict[int, Any] = {}

# Store for built-in functions
DB_BUILTINS: Dict[str, callable] = {}


def db_builtin(name: str):
    """Decorator to register database built-in functions."""
    def decorator(func: callable) -> callable:
        DB_BUILTINS[name] = func
        return func
    return decorator


# ===========================================
# Connection Management
# ===========================================

@db_builtin('db_connect')
def pyrl_db_connect(filename: str = ":memory:"):
    """Connect to SQLite database.
    
    Creates a new SQLite database connection. By default, creates an
    in-memory database that is not persisted to disk.
    
    Args:
        filename: Path to database file (default: in-memory database)
    
    Returns:
        Database connection handle (integer id)
        
    Example:
        $db = db_connect("myapp.db")
        $mem_db = db_connect()  # in-memory database
    """
    import sqlite3
    conn = sqlite3.connect(filename, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable row access by column name
    handle = id(conn)
    _db_connections[handle] = {
        'connection': conn,
        'cursor': conn.cursor(),
        'filename': filename
    }
    return handle


@db_builtin('db_close')
def pyrl_db_close(handle: int):
    """Close database connection.
    
    Args:
        handle: Database connection handle to close
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].close()
        del _db_connections[handle]
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ===========================================
# Query Execution
# ===========================================

@db_builtin('db_execute')
def pyrl_db_execute(handle: int, sql: str, params: List = None):
    """Execute SQL statement.
    
    Executes SQL statements like INSERT, UPDATE, DELETE, CREATE TABLE, etc.
    For SELECT queries, use db_query or db_query_one instead.
    
    Args:
        handle: Database connection handle from db_connect
        sql: SQL statement to execute
        params: Optional list of parameters for parameterized queries
    
    Returns:
        Dict with 'success', 'rowcount', 'lastrowid' or 'error'
        
    Example:
        $result = db_execute($db, "INSERT INTO users (name, email) VALUES (?, ?)", ["Alice", "alice@example.com"])
        print($result["lastrowid"])  # prints the new row id
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    conn = db['connection']
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return {
            'success': True,
            'rowcount': cursor.rowcount,
            'lastrowid': cursor.lastrowid
        }
    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}


@db_builtin('db_query')
def pyrl_db_query(handle: int, sql: str, params: List = None):
    """Execute SELECT query and fetch all results.
    
    Args:
        handle: Database connection handle from db_connect
        sql: SELECT SQL statement
        params: Optional list of parameters for parameterized queries
    
    Returns:
        Dict with 'success', 'rows' (list of dicts) or 'error'
        
    Example:
        $result = db_query($db, "SELECT * FROM users WHERE active = ?", [1])
        for $row in $result["rows"]:
            print($row["name"])
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        rows = cursor.fetchall()
        # Convert sqlite3.Row to dict
        result_rows = []
        for row in rows:
            result_rows.append(dict(row))
        
        return {'success': True, 'rows': result_rows}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@db_builtin('db_query_one')
def pyrl_db_query_one(handle: int, sql: str, params: List = None):
    """Execute SELECT query and fetch one result.
    
    Args:
        handle: Database connection handle from db_connect
        sql: SELECT SQL statement
        params: Optional list of parameters
    
    Returns:
        Dict with 'success', 'row' (dict or None) or 'error'
        
    Example:
        $result = db_query_one($db, "SELECT * FROM users WHERE id = ?", [1])
        if $result["row"] != None:
            print($result["row"]["name"])
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        row = cursor.fetchone()
        if row:
            return {'success': True, 'row': dict(row)}
        return {'success': True, 'row': None}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ===========================================
# Transaction Support
# ===========================================

@db_builtin('db_begin')
def pyrl_db_begin(handle: int):
    """Begin a database transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].execute("BEGIN")
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@db_builtin('db_commit')
def pyrl_db_commit(handle: int):
    """Commit current transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@db_builtin('db_rollback')
def pyrl_db_rollback(handle: int):
    """Rollback current transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].rollback()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ===========================================
# Introspection
# ===========================================

@db_builtin('db_tables')
def pyrl_db_tables(handle: int):
    """Get list of all tables in database.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success', 'tables' (list of table names) or 'error'
        
    Example:
        $result = db_tables($db)
        print($result["tables"])  # ["users", "sessions", ...]
    """
    result = pyrl_db_query(handle, 
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    if result['success']:
        tables = [row['name'] for row in result['rows']]
        return {'success': True, 'tables': tables}
    return result


# ===========================================
# Utility Functions
# ===========================================

def get_connection(handle: int) -> Optional[Dict]:
    """Get connection info by handle.
    
    Internal utility function to retrieve connection data.
    
    Args:
        handle: Database connection handle
        
    Returns:
        Connection dict or None if not found
    """
    return _db_connections.get(handle)


def close_all_connections():
    """Close all database connections.
    
    Utility function to clean up all open connections.
    Typically called during application shutdown.
    """
    global _db_connections
    for handle, db in list(_db_connections.items()):
        try:
            db['connection'].close()
        except:
            pass
    _db_connections = {}
