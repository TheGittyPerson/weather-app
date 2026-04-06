"""Utility for installing third-party dependencies using pip.

Use a requirements file:

```
from weather_app.utils import package_installer

package_installer.install_requirements()
```

Or install specific packages in code:

```
from weather_app.utils import package_installer

package_installer.install("requests>=2.31.0", ("rich", "13.7.0"))
```

Make sure to call these helpers before importing the third-party packages.

This module intentionally avoids third-party dependencies, so it does not
perform version comparison. When updates are enabled, it will run pip with
``--upgrade`` for the given requirement.
"""

import sys
import subprocess
from importlib import import_module
from pathlib import Path

_REQ_OPERATORS = ("==", ">=", "<=", "!=", "~=", ">", "<")


def install(*packages: object,
            check_updates: bool = True,
            update_pip: bool = True) -> None:
    """Ensure specified third-party packages are installed.

    Accepts one or more package specifiers. Each argument may be a string
    package name (optionally including a version specifier, such as
    ``requests>=2.24.0``) or an iterable of length two where the first item
    is the package name and the second item is the version requirement (for
    example, ``">=1.2.0"`` or ``"2.24.0"``). For each package, attempts to
    import it, and if missing, installs it via pip. If installed and updates
    are allowed, runs pip with ``--upgrade`` for the requirement. Optionally
    upgrades pip before the first installation/upgrade.

    Note: Make sure to import the dependencies after calling this function.

    Parameters:
        *packages:
            Package specifiers as strings or iterables of length two.
        check_updates (bool, optional):
            Whether to run pip with ``--upgrade`` when a package is already
            installed (default is True). When False, packages that can be
            imported are skipped.
        update_pip (bool, optional):
            Whether to upgrade pip before installing (default is True).

    Raises:
        RuntimeError: Failed to install packages.
        TypeError: Invalid package specifier.
    """
    requirements: dict[str, str] = {}
    for pkg in packages:
        if isinstance(pkg, str):
            pkg_name, spec = _parse_requirement_line(pkg)
        else:
            try:
                pkg_name, spec = pkg
            except Exception as exc:
                raise TypeError(
                    "Each package must be a string or an iterable of length "
                    "two."
                ) from exc

            if not isinstance(pkg_name, str):
                raise TypeError("Package name must be a string.")
            pkg_name = pkg_name.strip()
            if not pkg_name:
                continue

            if spec is None:
                spec = ""
            if not isinstance(spec, str):
                raise TypeError("Version specifier must be a string.")
            spec = _normalize_specifier(spec)

        if not pkg_name:
            continue
        requirements[pkg_name] = spec

    if not requirements:
        return

    pip_upgraded = False
    new_installed = False
    first = True
    for pkg_name, spec in requirements.items():
        requirement = f"{pkg_name}{spec}" if spec else pkg_name
        installed = True
        try:
            import_module(pkg_name)
        except ModuleNotFoundError:
            installed = False
            new_installed = True

        if installed and not check_updates:
            continue
        if first:
            first = False
            print("\nInstalling third-party dependencies...")

        try:
            if update_pip and not pip_upgraded:
                print("\nUpgrading pip first...\n")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade",
                     "pip"]
                )
                pip_upgraded = True
                print("\nSuccessfully upgraded pip.")
                print("\nInstalling packages...\n")

            install_cmd = [sys.executable, "-m", "pip", "install"]
            if check_updates:
                install_cmd.append("--upgrade")
            install_cmd.append(requirement)
            subprocess.check_call(install_cmd)

            print(f"\nSuccessfully installed '{pkg_name}'.")

        except subprocess.CalledProcessError:
            raise RuntimeError(
                f"\nFailed to install '{pkg_name}'. Please install it manually."
            )

    if new_installed:
        print("\nSuccessfully installed packages.")
        print("Resuming program...")
        print("\n==============================\n")


def install_requirements(requirements_file: str | Path = "requirements.txt",
                         check_updates: bool = True,
                         update_pip: bool = True, ) -> None:
    """Ensure third-party packages listed in a requirements file are installed.

    Reads a text file where each non-empty, non-comment line is a package name
    optionally followed by a version specifier (for example, ``>=1.2.0`` or
    ``==2.24.0``). For each package, attempts to import it, and if missing,
    installs it via pip. If installed and updates are allowed, runs pip with
    ``--upgrade`` for the requirement. Optionally upgrades pip before the first
    installation/upgrade.

    Exits function if requirements file not found.
    
    Note: Make sure to import the dependencies after calling this function.

    Parameters:
        requirements_file (str | Path, optional):
            Path to a text file with one package name per line, optionally
            followed by a version specifier (default is "requirements.txt").
        check_updates (bool, optional):
            Whether to run pip with ``--upgrade`` when a package is already
            installed (default is True). When False, packages that can be
            imported are skipped.
        update_pip (bool, optional):
            Whether to upgrade pip before installing (default is True).
            
    Raises:
        OSError: Failed to read requirements file.
        RuntimeError: Failed to install packages.
    """
    
    requirements = _read_requirements_file(requirements_file)
    if not requirements:
        return

    pip_upgraded = False
    new_installed = False
    first = True
    for pkg_name, spec in requirements.items():
        requirement = f"{pkg_name}{spec}" if spec else pkg_name
        installed = True
        try:
            import_module(pkg_name)
        except ModuleNotFoundError:
            installed = False
            new_installed = True

        if installed and not check_updates:
            continue
        if first:
            first = False
            print("\nInstalling third-party dependencies...")

        try:
            if update_pip and not pip_upgraded:
                print("\nUpgrading pip first...\n")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade",
                     "pip"]
                )
                pip_upgraded = True
                print("\nSuccessfully upgraded pip.")
                print("\nInstalling packages...\n")

            install_cmd = [sys.executable, "-m", "pip", "install"]
            if check_updates:
                install_cmd.append("--upgrade")
            install_cmd.append(requirement)
            subprocess.check_call(install_cmd)

            print(f"\nSuccessfully installed '{pkg_name}'.")

        except subprocess.CalledProcessError:
            raise RuntimeError(
                f"\nFailed to install '{pkg_name}'. Please install it manually."
            )
        
    if new_installed:
        print("\nSuccessfully installed requirements.")
        print("Resuming program...")
        print("\n==============================\n")


def _parse_requirement_line(line: str) -> tuple[str, str]:
    """Parse a requirements line into (name, spec)."""
    stripped = line.split("#", 1)[0].strip()
    if not stripped:
        return "", ""

    normalized = "".join(stripped.split())
    for op in _REQ_OPERATORS:
        if op in normalized:
            name, version = normalized.split(op, 1)
            name = name.strip()
            version = version.strip()
            if not name:
                return "", ""
            return name, f"{op}{version}" if version else op
    return normalized, ""


def _normalize_specifier(spec: str) -> str:
    """Normalize a version specifier string."""
    stripped = spec.strip()
    if not stripped:
        return ""
    normalized = "".join(stripped.split())
    for op in _REQ_OPERATORS:
        if normalized.startswith(op):
            version = normalized[len(op):].strip()
            return f"{op}{version}" if version else op
    for op in _REQ_OPERATORS:
        if op in normalized:
            _, version = normalized.split(op, 1)
            version = version.strip()
            return f"{op}{version}" if version else op
    return f"=={normalized}"


def _read_requirements_file(requirements_file: str | Path) -> dict[str, str]:
    """Read requirements and return a mapping of package name to spec."""
    requirements_path = Path(requirements_file)
    try:
        lines = requirements_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return {}
    except OSError as exc:
        raise OSError(
            f"\nFailed to read requirements file '{requirements_path}': {exc}"
        )

    requirements: dict[str, str] = {}
    for line in lines:
        pkg_name, spec = _parse_requirement_line(line)
        if not pkg_name:
            continue
        requirements[pkg_name] = spec
    return requirements
