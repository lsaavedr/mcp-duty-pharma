# SPDX-FileCopyrightText: 2025-present Luis Saavedra <luis94855510@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Command-line interface."""

from .duty_pharma import mcp


def entry_point() -> None:
    """Entry point for the package."""
    mcp.run()


if __name__ == "__main__":
    entry_point()
