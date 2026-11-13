#!/usr/bin/env python3

import os
import sys

try:
    from dotenv import dotenv_values, load_dotenv
except ImportError:
    print("ORACLE STATUS: python-dotenv is not installed")
    print("Run: pip install -r ex1/requirements.txt")
    sys.exit(1)

KEYS: list[str] = [
    "MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT",
]

# Safe defaults only: no real secret is written in this file.
DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local.db",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}

SECRET_KEYS: list[str] = ["API_KEY", "DATABASE_URL"]

HERE: str = os.path.dirname(os.path.abspath(__file__))
ENV_FILE: str = os.path.join(HERE, ".env")
GITIGNORE_FILE: str = os.path.join(HERE, ".gitignore")


def read_env_file() -> dict[str, str | None]:
    if not os.path.isfile(ENV_FILE):
        print("[WARNING] No .env file found "
              "(cp ex1/.env.example ex1/.env)")
        return {}
    try:
        values: dict[str, str | None] = dotenv_values(ENV_FILE)
        # override=False: variables already set in the shell win
        load_dotenv(ENV_FILE, override=False)
    except (OSError, ValueError) as error:
        print(f"[WARNING] Cannot read .env file: {error}")
        return {}
    return values


def load_config() -> tuple[dict[str, str], dict[str, str]]:
    shell: dict[str, str] = {}
    for key in KEYS:
        if os.environ.get(key):
            shell[key] = os.environ[key]
    env_file: dict[str, str | None] = read_env_file()
    config: dict[str, str] = {}
    sources: dict[str, str] = {}
    for key in KEYS:
        value: str = os.environ.get(key, "")
        if value == "":
            print(f"[WARNING] {key} is not set, using default value")
            config[key] = DEFAULTS[key]
            sources[key] = "default"
        else:
            config[key] = value
            if key not in shell and env_file.get(key):
                sources[key] = ".env file"
            else:
                sources[key] = "environment"
    return config, sources


def mask(value: str) -> str:
    if value == "":
        return "(empty)"
    if len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 2)


def show_config(config: dict[str, str], production: bool) -> None:
    url: str = config["DATABASE_URL"]
    level: str = config["LOG_LEVEL"].upper()
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    if url.startswith("sqlite") or "localhost" in url:
        print("Database: Connected to local instance")
        if production:
            print("[PRODUCTION WARNING] A local database is used")
    else:
        print("Database: Connected to remote instance")
    if config["API_KEY"] != "":
        print("API Access: Authenticated")
    else:
        print("API Access: No API key, access denied")
        if production:
            print("[PRODUCTION WARNING] API_KEY is required")
    if production and level == "DEBUG":
        print("Log Level: INFO (DEBUG is refused in production)")
    else:
        print(f"Log Level: {level}")
    if config["ZION_ENDPOINT"] != "":
        print("Remote Network: Online")
    else:
        print("Remote Network: Offline (no ZION_ENDPOINT)")


def show_details(config: dict[str, str], sources: dict[str, str]) -> None:
    print()
    print("Development details (never shown in production):")
    for key in KEYS:
        value: str = config[key]
        if key in SECRET_KEYS:
            value = mask(value)
        print(f"  {key} = {value} [from {sources[key]}]")


def read_text(path: str) -> str | None:
    try:
        with open(path, "r") as file:
            return file.read()
    except (OSError, ValueError):
        return None


def security_check(config: dict[str, str], sources: dict[str, str]) -> None:
    print()
    print("Configuration security check:")
    source_code: str | None = read_text(os.path.abspath(__file__))
    api_key: str = config["API_KEY"]
    if source_code is None:
        print("[WARNING] Cannot read the source code to check it")
    elif api_key != "" and api_key in source_code:
        print("[WARNING] The API key is written in the source code!")
    else:
        print("[OK] No hardcoded secrets detected")
    gitignore: str | None = read_text(GITIGNORE_FILE)
    if gitignore is not None and ".env" in gitignore.split():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARNING] .env is not listed in ex1/.gitignore")
    overrides: list[str] = [
        key for key in KEYS if sources[key] == "environment"
    ]
    if overrides:
        print(f"[OK] Production overrides active: {', '.join(overrides)}")
    else:
        print("[OK] Production overrides available")


if __name__ == "__main__":
    print("ORACLE STATUS: Consulting the configuration...")
    settings, origins = load_config()
    mode: str = settings["MATRIX_MODE"].lower()
    if mode not in ("development", "production"):
        print(f"[WARNING] Unknown MATRIX_MODE '{mode}', "
              "using development")
        mode = "development"
    settings["MATRIX_MODE"] = mode
    print()
    show_config(settings, mode == "production")
    if mode == "development":
        show_details(settings, origins)
    security_check(settings, origins)
    print()
    print("The Oracle sees all configurations.")
