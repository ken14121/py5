#!/usr/bin/env python3

import os
import site
import sys


def get_venv_name() -> str | None:
    if sys.prefix != sys.base_prefix:
        return os.path.basename(sys.prefix)
    return None


def show_package_locations() -> None:
    print("Package locations:")
    print(f"Global Python: {sys.base_prefix}")
    print(f"Current Python: {sys.prefix}")
    for path in site.getsitepackages():
        print(f"Packages are installed in: {path}")


def show_open_laboratory() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print()
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")
    print()
    show_package_locations()


def show_sealed_laboratory(venv_name: str) -> None:
    print("LABORATORY STATUS: The laboratory is sealed")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    for path in site.getsitepackages():
        print(path)
    print()
    show_package_locations()


if __name__ == "__main__":
    name: str | None = get_venv_name()
    if name is None:
        show_open_laboratory()
    else:
        show_sealed_laboratory(name)
