import pkgutil
import warnings
import subprocess
from contextlib import redirect_stdout
from io import StringIO
from typing import List, Any

import inquirer


def get_installed_modules() -> List[str]:
    """
    Get a list of installed Python modules.
    """
    installed_modules = [name for _, name, _ in pkgutil.iter_modules()]
    return installed_modules


def suppress_stdout(func: Any) -> Any:
    """
    Decorator to suppress standard output for a given function.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with redirect_stdout(StringIO()):
            return func(*args, **kwargs)

    return wrapper


def create_menu(modules: List[str]) -> List[str]:
    """
    Create a menu to select modules for uninstallation.
    """
    questions = [
        inquirer.Checkbox(
            "selected_modules", message="Select modules to uninstall", choices=modules
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["selected_modules"]


def confirm_uninstall(modules: List[str]) -> bool:
    """
    Confirm uninstallation of selected modules.
    """
    module_list = ", ".join(modules)
    question = inquirer.Confirm(
        "confirm_uninstall",
        message=f"Are you sure you want to uninstall the following modules: {module_list}?",
    )
    answer = inquirer.prompt([question])
    return answer["confirm_uninstall"]


def uninstall_modules(modules: List[str]) -> None:
    """
    Uninstall selected modules.
    """
    if confirm_uninstall(modules):
        for module in modules:
            subprocess.run(["pip", "uninstall", "-y", module])
            print(f"Uninstalled: {module}")
        print("Uninstallation completed.")
    else:
        print("Uninstallation canceled.")


def main():
    # Ignore warnings during execution
    warnings.filterwarnings("ignore")

    # Suppress standard output
    suppress_stdout_decorator = suppress_stdout

    print("Fetching installed Python modules...")
    modules = get_installed_modules()

    if modules:
        selected_modules = create_menu(modules)

        if selected_modules:
            print("\nUninstalling selected modules:")
            uninstall_modules(selected_modules)
        else:
            print("No modules selected.")
    else:
        print("No Python modules found.")
