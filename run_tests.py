#!/usr/bin/env python3
"""
Enhanced CLI script with parent scenario commands.

Usage:
    # Run complete scenarios (PARENT COMMANDS)
    python run_tests_enhanced.py --scenario rfi_complete
    python run_tests_enhanced.py --scenario rfi_rejection
    
    # List all scenarios
    python run_tests_enhanced.py --list-scenarios
    
    # Run individual workflows
    python run_tests_enhanced.py --role contractor --workflow rfi
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from config.test_data import TestData

# Available roles
ROLES = list(TestData.ROLES.keys())

# ============================================================================
# PARENT SCENARIOS - Complete multi-role workflows
# ============================================================================
SCENARIOS = {
    "rfi_complete": {
        "description": "Complete RFI lifecycle - Create → Review → Inspect → Approve",
        "steps": [
            {
                "role": "contractor",
                "workflow": "rfi",
                "description": "Contractor creates RFI with inspection checklist"
            },
            {
                "role": "block_engineer",
                "workflow": "review_rfi",
                "description": "Block Engineer reviews and approves RFI"
            },
            {
                "role": "quality_inspector",
                "workflow": "inspect_rfi",
                "description": "Quality Inspector inspects RFI (PASS)"
            },
            {
                "role": "quality_inspector",
                "workflow": "final_approval",
                "description": "Quality Inspector gives final approval"
            }
        ]
    },
    "rfi_rejection": {
        "description": "RFI rejection workflow - Create → Request Changes",
        "steps": [
            {
                "role": "contractor",
                "workflow": "rfi",
                "description": "Contractor creates RFI"
            },
            {
                "role": "block_engineer",
                "workflow": "request_changes",
                "description": "Block Engineer requests changes"
            }
        ]
    },
    "rfi_inspection_fail": {
        "description": "RFI inspection failure - Create → Review → Fail",
        "steps": [
            {
                "role": "contractor",
                "workflow": "rfi",
                "description": "Contractor creates RFI"
            },
            {
                "role": "block_engineer",
                "workflow": "review_rfi",
                "description": "Block Engineer reviews RFI"
            },
            {
                "role": "quality_inspector",
                "workflow": "inspect_rfi_fail",
                "description": "Quality Inspector fails inspection"
            }
        ]
    },
    "contractor_only": {
        "description": "Contractor workflows only - Create RFI",
        "steps": [
            {
                "role": "contractor",
                "workflow": "rfi",
                "description": "Contractor creates RFI with inspection checklist"
            }
        ]
    },
    "block_engineer_only": {
        "description": "Block Engineer workflows - Review → Approve",
        "steps": [
            {
                "role": "block_engineer",
                "workflow": "review_rfi",
                "description": "Block Engineer reviews RFI"
            },
            {
                "role": "block_engineer",
                "workflow": "approve_rfi",
                "description": "Block Engineer gives final approval"
            }
        ]
    },
    "quality_inspector_only": {
        "description": "Quality Inspector workflows - Inspect → Final Approval",
        "steps": [
            {
                "role": "quality_inspector",
                "workflow": "inspect_rfi",
                "description": "Quality Inspector inspects RFI"
            },
            {
                "role": "quality_inspector",
                "workflow": "final_approval",
                "description": "Quality Inspector gives final approval"
            }
        ]
    }
}

# ============================================================================
# ROLE-BASED WORKFLOWS
# ============================================================================
WORKFLOWS_BY_ROLE = {
    "contractor": {
        "rfi": {
            "description": "Test RFI creation workflow (Contractor)",
            "pytest_args": ["-m", "rfi", "-v"]
        }
    },
    "contractor_incharge": {
        "rfi": {
            "description": "Test RFI & Inspection workflow (Contractor Incharge)",
            "pytest_args": ["tests/cntr/test_createRfi.py", "-k", "test_contractor_incharge_workflow", "-v"]
        }
    },
    "block_engineer": {
        "review_rfi": {
            "description": "Test RFI review workflow (Block Engineer)",
            "pytest_args": ["tests/block_engineer/test_review_rfi.py", "-k", "test_review_rfi_workflow", "-v"]
        },
        "approve_rfi": {
            "description": "Test RFI final approval workflow (Block Engineer)",
            "pytest_args": ["tests/block_engineer/test_approve_rfi.py", "-k", "test_approve_rfi_workflow", "-v"]
        },
        "request_changes": {
            "description": "Test RFI request changes workflow (Block Engineer)",
            "pytest_args": ["tests/block_engineer/test_review_rfi.py", "-k", "test_review_rfi_request_changes", "-v"]
        }
    },
    "quality_inspector": {
        "inspect_rfi": {
            "description": "Test RFI inspection workflow (Quality Inspector)",
            "pytest_args": ["tests/quality/test_inspect_rfi.py", "-k", "test_inspect_rfi_pass_workflow", "-v"]
        },
        "inspect_rfi_fail": {
            "description": "Test RFI inspection fail workflow (Quality Inspector)",
            "pytest_args": ["tests/quality/test_inspect_rfi.py", "-k", "test_inspect_rfi_fail_workflow", "-v"]
        },
        "final_approval": {
            "description": "Test final approval workflow (Quality Inspector)",
            "pytest_args": ["tests/quality/test_final_approval.py", "-k", "test_final_approval_workflow", "-v"]
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


def print_scenarios():
    """Print available parent scenarios."""
    print("\n" + "="*80)
    print("📋 PARENT SCENARIOS (Multi-Step Workflows)")
    print("="*80)
    for name, data in SCENARIOS.items():
        print(f"\n  🎯 {name}")
        print(f"     {data['description']}")
        print(f"     Steps:")
        for idx, step in enumerate(data['steps'], 1):
            print(f"       {idx}. [{step['role']}] {step['description']}")
    print("\n" + "="*80)
    print("Usage: python run_tests_enhanced.py --scenario <scenario_name>")
    print("="*80 + "\n")


def print_workflows():
    """Print available role-based workflows."""
    print("\n" + "="*80)
    print("🔄 ROLE-BASED WORKFLOWS")
    print("="*80)
    for role, workflows in WORKFLOWS_BY_ROLE.items():
        print(f"\n  {role.upper()}:")
        for key, value in workflows.items():
            print(f"    {key:20} - {value['description']}")
    print("\n" + "="*80)
    print("Usage: python run_tests_enhanced.py --role <role> --workflow <workflow_name>")
    print("="*80 + "\n")


def get_python_executable():
    """Get the Python executable to use."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return sys.executable
    
    script_dir = Path(__file__).parent
    venv_dir = script_dir / "venv"
    
    if venv_dir.exists():
        venv_python = venv_dir / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        venv_python = venv_dir / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
    
    venv_env = os.environ.get("VIRTUAL_ENV")
    if venv_env:
        venv_path = Path(venv_env)
        venv_python = venv_path / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        venv_python = venv_path / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
    
    return sys.executable


def run_tests(pytest_args):
    """Run pytest with given arguments."""
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "pytest"] + pytest_args
    
    print(f"\n{'='*80}")
    print(f"▶️  Running: {' '.join(cmd)}")
    print(f"{'='*80}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_scenario(scenario_name, html_report=False):
    """Run a complete multi-step scenario."""
    if scenario_name not in SCENARIOS:
        print(f"❌ Error: Scenario '{scenario_name}' not found")
        print("\nAvailable scenarios:")
        for name in SCENARIOS.keys():
            print(f"  - {name}")
        return 1
    
    scenario = SCENARIOS[scenario_name]
    steps = scenario['steps']
    
    print("\n" + "="*80)
    print(f"🎯 RUNNING SCENARIO: {scenario_name}")
    print(f"📝 Description: {scenario['description']}")
    print(f"📊 Total Steps: {len(steps)}")
    print("="*80)
    
    failed_steps = []
    
    for idx, step in enumerate(steps, 1):
        role = step['role']
        workflow = step['workflow']
        description = step['description']
        
        print(f"\n{'─'*80}")
        print(f"⏩ STEP {idx}/{len(steps)}: {description}")
        print(f"   Role: {role} | Workflow: {workflow}")
        print(f"{'─'*80}")
        
        # Get pytest args for this workflow
        if role in WORKFLOWS_BY_ROLE and workflow in WORKFLOWS_BY_ROLE[role]:
            workflow_data = WORKFLOWS_BY_ROLE[role][workflow]
            pytest_args = workflow_data['pytest_args'].copy()
            
            if html_report:
                pytest_args.extend(["--html=report.html", "--self-contained-html"])
            
            # Run the test
            returncode = run_tests(pytest_args)
            
            if returncode != 0:
                print(f"\n❌ STEP {idx} FAILED: {description}")
                failed_steps.append(f"Step {idx}: {description}")
                
                # Ask user if they want to continue
                print(f"\n⚠️  Step failed. Continue with remaining steps? (y/n): ", end='')
                try:
                    response = input().strip().lower()
                    if response != 'y':
                        print("\n🛑 Scenario execution stopped by user")
                        break
                except:
                    print("\n🛑 Scenario execution stopped")
                    break
            else:
                print(f"\n✅ STEP {idx} COMPLETED: {description}")
        else:
            print(f"❌ Error: Workflow '{workflow}' not found for role '{role}'")
            failed_steps.append(f"Step {idx}: Workflow not found")
    
    # Summary
    print("\n" + "="*80)
    print(f"📊 SCENARIO SUMMARY: {scenario_name}")
    print("="*80)
    if failed_steps:
        print(f"❌ Status: FAILED")
        print(f"📉 Failed Steps: {len(failed_steps)}/{len(steps)}")
        for failed in failed_steps:
            print(f"   - {failed}")
    else:
        print(f"✅ Status: SUCCESS")
        print(f"📈 All {len(steps)} steps completed successfully!")
    print("="*80 + "\n")
    
    return 0 if not failed_steps else 1


def main():
    parser = argparse.ArgumentParser(
        description="Run Selenium test scenarios and workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete scenarios (PARENT COMMANDS)
  python run_tests_enhanced.py --scenario rfi_complete
  python run_tests_enhanced.py --scenario rfi_rejection
  python run_tests_enhanced.py --scenario contractor_only
  
  # Run individual workflows
  python run_tests_enhanced.py --role contractor --workflow rfi
  python run_tests_enhanced.py --role block_engineer --workflow review_rfi
  python run_tests_enhanced.py --role quality_inspector --workflow inspect_rfi
  
  # List available options
  python run_tests_enhanced.py --list-scenarios
  python run_tests_enhanced.py --list-workflows
  python run_tests_enhanced.py --list
        """
    )
    
    parser.add_argument(
        "--scenario", "-s",
        help="Run a complete parent scenario (multi-step workflow)"
    )
    
    parser.add_argument(
        "--role", "-r",
        choices=ROLES,
        help="Role for authentication"
    )
    
    parser.add_argument(
        "--workflow", "-w",
        help="Run specific workflow for the given role"
    )
    
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List all available parent scenarios"
    )
    
    parser.add_argument(
        "--list-workflows",
        action="store_true",
        help="List all available role-based workflows"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available scenarios and workflows"
    )
    
    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Generate HTML report"
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_scenarios:
        print_scenarios()
        return 0
    
    if args.list_workflows:
        print_workflows()
        return 0
    
    if args.list:
        print_scenarios()
        print_workflows()
        return 0
    
    # Handle scenario execution (PARENT COMMAND)
    if args.scenario:
        return run_scenario(args.scenario, args.html_report)
    
    # Handle individual workflow execution
    if args.role and args.workflow:
        if args.role in WORKFLOWS_BY_ROLE and args.workflow in WORKFLOWS_BY_ROLE[args.role]:
            workflow = WORKFLOWS_BY_ROLE[args.role][args.workflow]
            print(f"\n▶️  Running workflow: {args.workflow}")
            print(f"   Role: {args.role}")
            print(f"   Description: {workflow['description']}\n")
            
            pytest_args = workflow["pytest_args"].copy()
            if args.html_report:
                pytest_args.extend(["--html=report.html", "--self-contained-html"])
            
            return run_tests(pytest_args)
        else:
            print(f"❌ Error: Workflow '{args.workflow}' not found for role '{args.role}'")
            if args.role in WORKFLOWS_BY_ROLE:
                print(f"\nAvailable workflows for {args.role}:")
                for wf in WORKFLOWS_BY_ROLE[args.role].keys():
                    print(f"  - {wf}")
            return 1
    
    # No valid arguments provided
    print("❌ Error: Please specify --scenario, or --role with --workflow, or --list")
    print("\nQuick help:")
    print("  --list            : Show all available options")
    print("  --scenario <name> : Run a complete parent scenario")
    print("  --role <role> --workflow <name> : Run individual workflow")
    print("\nFor detailed help: python run_tests_enhanced.py --help")
    return 1


if __name__ == "__main__":
    sys.exit(main())
