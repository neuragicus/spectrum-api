#!/usr/bin/env bash
# bump-version.sh

# Save old version
OLD_VER=$(poetry version --short)

# Run poetry version with passed argument (patch, minor, major)
poetry version "$1"

# Get new version
NEW_VER=$(poetry version --short)

# Commit the change
git add pyproject.toml
git commit -m "Bump version $OLD_VER to $NEW_VER"
