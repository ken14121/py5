#!/usr/bin/env python3

import importlib
import sys

REAGENTS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
}


def get_version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return str(getattr(module, "__version__", "unknown"))


def check_reagents() -> list[str]:
    missing: list[str] = []
    print("Checking dependencies:")
    for name in REAGENTS:
        version: str | None = get_version(name)
        if version is None:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {REAGENTS[name]}")
    return missing


def show_install_help(missing: list[str]) -> None:
    print()
    print(f"Missing reagents: {', '.join(missing)}")
    print("Install with pip:")
    print("  pip install -r ex0/requirements.txt")
    print("Install with Poetry (pyproject.toml is in ex0/):")
    print("  pip install poetry    # only if Poetry itself is missing")
    print("  cd ex0")
    print("  poetry install")
    print("  poetry run python loading.py")


def show_pip_vs_poetry() -> None:
    print()
    print("pip vs Poetry:")
    print("requirements.txt declares what to install; "
          "pip resolves it at install time.")
    print("pyproject.toml declares the same constraints, "
          "and Poetry pins the resolved")
    print("versions in poetry.lock so every install is identical.")


def run_experiment() -> None:
    numpy = importlib.import_module("numpy")
    pandas = importlib.import_module("pandas")
    generator = numpy.random.default_rng()
    doses = generator.normal(loc=50.0, scale=10.0, size=100)
    table = pandas.DataFrame({"dose": doses})
    print()
    print("Quick experiment: 100 reagent doses simulated with numpy")
    print(f"pandas mean dose: {table['dose'].mean():.2f}")
    print(f"pandas min / max: {table['dose'].min():.2f} / "
          f"{table['dose'].max():.2f}")


if __name__ == "__main__":
    print("REAGENT STATUS: Loading reagents...")
    print(f"Python used: {sys.executable}")
    print()
    missing_reagents: list[str] = check_reagents()
    show_pip_vs_poetry()
    if missing_reagents:
        show_install_help(missing_reagents)
    else:
        run_experiment()
        print()
        print("All reagents present and accounted for.")
