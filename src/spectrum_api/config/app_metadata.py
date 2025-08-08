from dataclasses import dataclass

import toml  # type: ignore


@dataclass
class AppMetadata:
    """Application metadata container.

    Args:
        name: The name of the application
        version: The version string of the application
    """

    name: str
    version: str


def get_app_metadata() -> AppMetadata:
    """Retrieve application metadata from pyproject.toml.

    Returns:
        AppMetadata object containing the application name and version

    Raises:
        FileNotFoundError: If pyproject.toml is not found.
        KeyError: If required metadata fields are missing.
    """

    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

        # Fetch name and version
        return AppMetadata(
            name=config["tool"]["poetry"]["name"],
            version=config["tool"]["poetry"]["version"],
        )
