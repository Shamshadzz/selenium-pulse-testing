class TestData:
    # Role-based login credentials
    ROLES = {
        "contractor": {
            "username": "contractor1@gmail.com",
            "password": "Test@1234"
        },
        "admin": {
            "username": "admin@example.com",  # Update with actual admin credentials
            "password": "Admin@1234"  # Update with actual admin password
        },
        "project_manager": {
            "username": "pm@example.com",  # Update with actual PM credentials
            "password": "PM@1234"  # Update with actual PM password
        },
        "client": {
            "username": "client@example.com",  # Update with actual client credentials
            "password": "Client@1234"  # Update with actual client password
        }
    }
    
    # Backward compatibility - defaults to contractor
    VALID_USERNAME = ROLES["contractor"]["username"]
    VALID_PASSWORD = ROLES["contractor"]["password"]
    
    INVALID_USERNAME = "invalid@example.com"
    INVALID_PASSWORD = "wrong_password"
    
    # Test data for different workflows
    WORKFLOW_1_DATA = {
        "field1": "value1",
        "field2": "value2"
    }
    
    WORKFLOW_2_DATA = {
        "name": "Test Name",
        "description": "Test Description"
    }
    
    @classmethod
    def get_credentials(cls, role):
        """Get credentials for a specific role."""
        if role not in cls.ROLES:
            raise ValueError(f"Unknown role: {role}. Available roles: {list(cls.ROLES.keys())}")
        return cls.ROLES[role]