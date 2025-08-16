# FastAPI Template with Authentication and Single-Tenant Design

This project provides a robust FastAPI template featuring:

## Key Features

- **Router Class**: A structured approach to route endpoints
- **Base Controller**: Handles database connections and CRUD operations
- **Authentication System**: Complete auth flow with JWT tokens
- **Type Safety**: Fully typed codebase
- **Single-Tenant Design**: Implemented using the single tenant design pattern

## Project Structure

```
project/
├── app/
│   ├── auth/                  # Authentication module
│   │   ├── auth.py            # Auth class implementation
│   ├── controller/            # Controller layer
│   │   ├── base_controller.py # Base CRUD operations
│   ├── router/                # Routing layer
│   │   ├── base_router.py     # Base routing implementation
│   ├── models/                # Data models
│   ├── db/                    # Database configuration
│   ├── core/                  # Core configurations
│   └── main.py                # Main application entry point
```

## Authentication System

The `Auth` class provides:

- JWT token generation and validation
- Password hashing with bcrypt
- User login functionality
- User creation and management
- Password change/reset functionality
- Role-based access control

```python
# Example usage
auth = Auth()
token = auth.login(login_data, session)
current_user = auth.get_current_user(session, token)
```

## Base Controller

The `BaseController` implements common CRUD operations:

```python
class BaseController(Generic[T]):
    async def get(self, id) -> T | None
    async def create(self, data: T) -> T | bool
    async def update(self, id: int, data: T) -> T | bool
    async def delete(self, id) -> bool
    async def read(self) -> list[T]
    async def get_by_field(self, field: str, value: str) -> T
```

## Base Router

The `BaseRouter` provides standardized API endpoints:

```python
class BaseRouter(Generic[_ModelType, _CreateType]):
    # Automatically creates these endpoints:
    # GET /         - List all items
    # GET /{id}     - Get single item
    # POST /        - Create new item
    # PUT /{id}     - Update item
    # DELETE /{id}  - Delete item
```

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your database settings in `app/core/settings.py`
4. Run the application: `uvicorn app.main:app --reload`

## Dependencies

- FastAPI
- SQLModel
- Passlib
- Python-jose
- Uvicorn

## Design Patterns

This template implements the **Single-Tenant Design Pattern**, ensuring:

- Isolated database connections
- Clear separation of concerns
- Scalable architecture
- Maintainable code structure

## Contribution

Contributions are welcome! Please open an issue or pull request for any improvements.

## License

[MIT License](LICENSE)
