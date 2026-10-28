"""github-actions.

Github Actions - LinkML Schema
"""

try:
    from github_actions._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
