class TestData:
    ROLES = {
        "contractor": {
            "username": "contractor1@gmail.com",
            "password": "Test@1234"
        },
        "block_engineer": {
            "username": "engineer1@adani.com",
            "password": "Test@1234"
        },
        "quality_inspector": {
            "username": "inspector9@adani.com",
            "password": "Test@1234"
        },
        "contractor_incharge": {
            "username": "contractor.incharge2@gmail.com",
            "password": "Test@1234"
        },
        "admin": {
            "username": "admin@example.com",
            "password": "Admin@1234"
        },
        "project_manager": {
            "username": "pm@example.com",
            "password": "PM@1234"
        },
        "client": {
            "username": "client@example.com",
            "password": "Client@1234"
        }
    }

    INVALID_USERNAME = "invalid@example.com"
    INVALID_PASSWORD = "wrong_password"
    
    @classmethod
    def get_credentials(cls, role):
        """Get credentials for a specific role."""
        if role not in cls.ROLES:
            raise ValueError(f"Unknown role: {role}. Available roles: {list(cls.ROLES.keys())}")
        return cls.ROLES[role]