"""Exceptions for Todo CLI application."""


class StorageError(Exception):
    """Exception raised when storage operations fail."""
    pass


class TaskNotFoundError(Exception):
    """Exception raised when task ID does not exist."""
    pass


class InvalidTaskError(Exception):
    """Exception raised when task data is invalid."""
    pass
