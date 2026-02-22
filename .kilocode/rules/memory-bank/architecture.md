# Architecture: Pyrl Authentication System

## System Components

### User Database (%users)
- Hash-based storage for user accounts
- Contains username as key with password, email, and role as values
- Predefined admin account with administrator role
- Regular user accounts with standard user role

### Session Management (%active_sessions)
- Hash-based storage for active user sessions
- Maps session ID to user information and login time
- Tracks user roles during active sessions

### Core Functions
- `&login(username, password)`: Authenticates users and creates sessions
- `&logout(session_id)`: Terminates active sessions
- `&register(username, email, password)`: Creates new user accounts
- `&hash_password(password)`: Secures passwords (to be implemented)
- `&time()`: Generates timestamps for session tracking

### Vue Component
- LoginForm component for user interface
- Provides fields for username and password input
- Handles form submission for authentication

## Data Flow
1. User registration stores validated credentials in user database
2. Login validates credentials and creates session entries
3. Session IDs track authenticated users during their visit
4. Logout removes session entries to end user access