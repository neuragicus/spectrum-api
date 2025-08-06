from dataclasses import dataclass

import toml  # type: ignore


@dataclass
class AppMetadata:
    name: str
    version: str


def get_app_metadata() -> AppMetadata:
    """Returns app metadata: name and version."""

    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

        # Fetch name and version
        return AppMetadata(
            name=config["tool"]["poetry"]["name"],
            version=config["tool"]["poetry"]["version"],
        )
