#!/usr/bin/env python3
"""
CLI script to run specific test workflows/pages with role-based authentication.
Usage:
    python run_tests.py --role contractor --workflow rfi
    python run_tests.py --role admin --page create_rfi
    python run_tests.py --role contractor --all
    python run_tests.py --list
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from config.test_data import TestData

# Available roles
ROLES = list(TestData.ROLES.keys())

# Role-based workflows and pages
# Format: {role: {workflow_name: {description, pytest_args}}}
WORKFLOWS_BY_ROLE = {
    "contractor": {
        "rfi": {
            "description": "Test RFI creation workflow (Contractor)",
            "pytest_args": ["-m", "rfi", "-v"]
        }
    },
    "admin": {
        "admin_dashboard": {
            "description": "Test Admin Dashboard workflow",
            "pytest_args": ["-m", "admin", "-v"]
        }
    },
    "project_manager": {
        "pm_dashboard": {
            "description": "Test Project Manager Dashboard workflow",
            "pytest_args": ["-m", "pm", "-v"]
        }
    },
    "client": {
        "client_portal": {
            "description": "Test Client Portal workflow",
            "pytest_args": ["-m", "client", "-v"]
        }
    }
}

# Role-based pages
# Format: {role: {page_name: {description, pytest_args}}}
PAGES_BY_ROLE = {
    "contractor": {
        "create_rfi": {
            "description": "Test Create RFI page (Contractor)",
            "pytest_args": ["tests/cntr/test_createRfi.py", "-v"]
        }
    },
    "admin": {
        "admin_panel": {
            "description": "Test Admin Panel page",
            "pytest_args": ["tests/admin/test_admin_panel.py", "-v"]
        }
    },
    "project_manager": {
        "pm_dashboard": {
            "description": "Test PM Dashboard page",
            "pytest_args": ["tests/pm/test_pm_dashboard.py", "-v"]
        }
    },
    "client": {
        "client_portal": {
            "description": "Test Client Portal page",
            "pytest_args": ["tests/client/test_client_portal.py", "-v"]
        }
    }
}

# Common workflows (not role-specific)
COMMON_WORKFLOWS = {
    "login": {
        "description": "Test login functionality",
        "pytest_args": ["-m", "login", "-v"]
    }
}

# Common pages (not role-specific)
COMMON_PAGES = {
    "login": {
        "description": "Test Login page",
        "pytest_args": ["tests/test_login.py", "-v"]
    }
}


def print_menu():
    """Print available roles, workflows and pages."""
    print("\n" + "="*70)
    print("Available Roles:")
    print("="*70)
    for role in ROLES:
        print(f"  {role}")
    
    print("\n" + "="*70)
    print("Role-based Workflows:")
    print("="*70)
    for role, workflows in WORKFLOWS_BY_ROLE.items():
        print(f"\n  {role.upper()}:")
        for key, value in workflows.items():
            print(f"    {key:20} - {value['description']}")
    
    print("\n" + "="*70)
    print("Role-based Pages:")
    print("="*70)
    for role, pages in PAGES_BY_ROLE.items():
        print(f"\n  {role.upper()}:")
        for key, value in pages.items():
            print(f"    {key:20} - {value['description']}")
    
    print("\n" + "="*70)
    print("Common Workflows (no role required):")
    print("="*70)
    for key, value in COMMON_WORKFLOWS.items():
        print(f"  {key:15} - {value['description']}")
    
    print("\n" + "="*70)
    print("Common Pages (no role required):")
    print("="*70)
    for key, value in COMMON_PAGES.items():
        print(f"  {key:15} - {value['description']}")
    print("="*70 + "\n")


def get_python_executable():
    """Get the Python executable to use, preferring virtual environment if available."""
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Already in a virtual environment
        return sys.executable
    
    # Check for venv in the project directory
    script_dir = Path(__file__).parent
    venv_dir = script_dir / "venv"
    
    if venv_dir.exists():
        # Windows
        venv_python = venv_dir / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        
        # Unix/Linux/Mac
        venv_python = venv_dir / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
    
    # Check for VIRTUAL_ENV environment variable
    venv_env = os.environ.get("VIRTUAL_ENV")
    if venv_env:
        venv_path = Path(venv_env)
        # Windows
        venv_python = venv_path / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        # Unix/Linux/Mac
        venv_python = venv_path / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
    
    # Fall back to current Python
    return sys.executable

def run_tests(pytest_args):
    """Run pytest with given arguments."""
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "pytest"] + pytest_args
    
    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run Selenium tests for specific workflows or pages with role-based authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --role contractor --workflow rfi
  python run_tests.py --role contractor --page create_rfi
  python run_tests.py --role admin --all
  python run_tests.py --workflow login  (no role needed)
  python run_tests.py --list
        """
    )
    
    parser.add_argument(
        "--role", "-r",
        choices=ROLES,
        help="Role to use for authentication (contractor, admin, project_manager, client)"
    )
    
    parser.add_argument(
        "--workflow", "-w",
        help="Run tests for a specific workflow (use --list to see available workflows)"
    )
    
    parser.add_argument(
        "--page", "-p",
        help="Run tests for a specific page (use --list to see available pages)"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all tests (optionally filtered by role)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available roles, workflows and pages"
    )
    
    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Generate HTML report"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print_menu()
        return 0
    
    pytest_args = []
    
    if args.html_report:
        pytest_args.extend(["--html=report.html", "--self-contained-html"])
    
    if args.all:
        if args.role:
            print(f"\nRunning all tests for role: {args.role}")
            # Filter tests by role marker if available
            pytest_args.extend(["-m", args.role, "-v"])
        else:
            print("\nRunning all tests")
            pytest_args.extend(["-v"])
    elif args.workflow:
        # Check if it's a common workflow
        if args.workflow in COMMON_WORKFLOWS:
            workflow = COMMON_WORKFLOWS[args.workflow]
            print(f"\nRunning workflow: {args.workflow}")
            print(f"Description: {workflow['description']}\n")
            pytest_args.extend(workflow["pytest_args"])
        elif args.role and args.role in WORKFLOWS_BY_ROLE:
            if args.workflow in WORKFLOWS_BY_ROLE[args.role]:
                workflow = WORKFLOWS_BY_ROLE[args.role][args.workflow]
                print(f"\nRunning workflow: {args.workflow} (Role: {args.role})")
                print(f"Description: {workflow['description']}\n")
                pytest_args.extend(workflow["pytest_args"])
            else:
                print(f"Error: Workflow '{args.workflow}' not found for role '{args.role}'")
                print(f"Available workflows for {args.role}: {list(WORKFLOWS_BY_ROLE[args.role].keys())}")
                return 1
        else:
            print("Error: Role is required for role-based workflows")
            print("Use --role to specify a role, or use --list to see available options")
            return 1
    elif args.page:
        # Check if it's a common page
        if args.page in COMMON_PAGES:
            page = COMMON_PAGES[args.page]
            print(f"\nRunning page tests: {args.page}")
            print(f"Description: {page['description']}\n")
            pytest_args.extend(page["pytest_args"])
        elif args.role and args.role in PAGES_BY_ROLE:
            if args.page in PAGES_BY_ROLE[args.role]:
                page = PAGES_BY_ROLE[args.role][args.page]
                print(f"\nRunning page tests: {args.page} (Role: {args.role})")
                print(f"Description: {page['description']}\n")
                pytest_args.extend(page["pytest_args"])
            else:
                print(f"Error: Page '{args.page}' not found for role '{args.role}'")
                print(f"Available pages for {args.role}: {list(PAGES_BY_ROLE[args.role].keys())}")
                return 1
        else:
            print("Error: Role is required for role-based pages")
            print("Use --role to specify a role, or use --list to see available options")
            return 1
    else:
        print("Error: Please specify --workflow, --page, --all, or --list")
        print_menu()
        parser.print_help()
        return 1
    
    return run_tests(pytest_args)


if __name__ == "__main__":
    sys.exit(main())

