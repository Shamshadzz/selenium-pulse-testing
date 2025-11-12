# Selenium Pulse Testing

This project contains Selenium tests for web application testing with automatic login session management and multi-role support.

## Features

- **Multi-Role Support**: Support for multiple user roles (contractor, admin, project_manager, client) with separate session management
- **Session-based login**: Each role has its own session-scoped driver fixture that logs in once per session, keeping you logged in across all tests
- **No repeated logins**: Each role logs in only once per test session, even when running multiple tests
- **CLI Test Runner**: Choose specific workflows or pages to test through terminal with role selection
- **Modular Page Objects**: Organized page object model for maintainable tests

## Quick Start

### Using the CLI Runner (Recommended)

```bash
# List all available roles, workflows and pages
python run_tests.py --list

# Run RFI workflow tests as contractor (automatically logged in)
python run_tests.py --role contractor --workflow rfi

# Run Create RFI page tests as contractor
python run_tests.py --role contractor --page create_rfi

# Run all tests for a specific role
python run_tests.py --role admin --all

# Run common workflows (no role required)
python run_tests.py --workflow login

# Run with HTML report
python run_tests.py --role contractor --workflow rfi --html-report
```

### Using pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run only RFI tests (uses contractor_driver fixture - auto-logged in)
pytest tests/cntr/test_createRfi.py -v

# Run only login tests (no role needed)
pytest tests/test_login.py -v -m login

# Run specific test
pytest tests/cntr/test_createRfi.py::TestCreateRfi::test_create_rfi_successfully -v
```

## Available Roles

The following roles are configured (update credentials in `config/test_data.py`):

- **contractor**: Contractor user role
- **admin**: Administrator role
- **project_manager**: Project Manager role
- **client**: Client role

## Test Structure

- **`tests/cntr/test_createRfi.py`**: RFI creation tests (uses `contractor_driver` fixture)
- **`tests/test_login.py`**: Login functionality tests
- **`pages/`**: Page Object Model classes
- **`config/`**: Configuration and test data (including role credentials)

## Fixtures

### Standard Fixtures
- **`driver`**: Standard driver fixture (function scope)
- **`base_url`**: Base URL configuration

### Role-based Logged-in Fixtures (Session-scoped)
Each role has its own fixture that logs in once per session:

- **`contractor_driver`**: Logged-in driver for contractor role
- **`admin_driver`**: Logged-in driver for admin role
- **`project_manager_driver`**: Logged-in driver for project manager role
- **`client_driver`**: Logged-in driver for client role
- **`logged_in_driver`**: Backward compatibility - defaults to contractor role

## Configuration

### Updating Role Credentials

Edit `config/test_data.py` to update credentials for each role:

```python
ROLES = {
    "contractor": {
        "username": "contractor1@gmail.com",
        "password": "Test@1234"
    },
    "admin": {
        "username": "admin@example.com",
        "password": "Admin@1234"
    },
    # ... other roles
}
```

### Adding New Roles

1. Add role credentials to `TestData.ROLES` in `config/test_data.py`
2. Create a new fixture in `conftest.py`:
   ```python
   @pytest.fixture(scope="session")
   def new_role_driver():
       driver = _create_driver()
       _login_as_role(driver, "new_role")
       yield driver
       driver.quit()
   ```
3. Update `run_tests.py` to add workflows/pages for the new role

## Notes

- Each role's driver fixture logs in **once per test session**, so you stay logged in across all tests for that role
- You can use multiple role fixtures in the same test session - each role maintains its own separate browser session
- Dashboard page testing has been removed from RFI tests as requested
- Use `--role` with `--workflow` or `--page` flags to test role-specific functionality
- Common workflows/pages (like login) don't require a role specification
