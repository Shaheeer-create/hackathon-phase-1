"""Validation utilities for Todo CLI application."""

from typing import List, Optional

try:
    from ..models.enums import Priority
except ImportError:
    Priority = None


def validate_priority(priority_input: str) -> Optional[Priority]:
    """Validate priority input and return Priority enum or None if invalid.

    Args:
        priority_input: User input string for priority

    Returns:
        Priority enum value or None if invalid

    Examples:
        >>> validate_priority("high")
        <Priority.HIGH>
        >>> validate_priority("High")
        <Priority.HIGH>
        >>> validate_priority("H")
        <Priority.HIGH>
        >>> validate_priority("invalid")
        None
    """
    # If Priority enum not available, can't validate properly
    if Priority is None:
        return None

    if not priority_input or not priority_input.strip():
        return Priority.MEDIUM  # Default to MEDIUM

    priority_input = priority_input.lower().strip()

    if priority_input in ["high", "h"]:
        return Priority.HIGH
    elif priority_input in ["medium", "m"]:
        return Priority.MEDIUM
    elif priority_input in ["low", "l"]:
        return Priority.LOW
    else:
        return None  # Invalid priority


def validate_tags(tags_input: str) -> Optional[List[str]]:
    """Validate and parse tags from comma-separated input.

    Args:
        tags_input: User input string for tags (comma-separated)

    Returns:
        List of deduplicated tags, or None if input is empty

    Examples:
        >>> validate_tags("Work, Home, Urgent")
        ['Work', 'Home', 'Urgent']
        >>> validate_tags("")
        []
        >>> validate_tags("Work, Work, Home")
        ['Work', 'Home']  # Deduplicated
    """
    if not tags_input:
        return []

    # Split by comma and strip whitespace
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    # Deduplicate while preserving order
    seen = set()
    deduplicated = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            deduplicated.append(tag)

    return deduplicated


def is_valid_date(date_str: str) -> bool:
    """Check if date string matches YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        True if format is YYYY-MM-DD, False otherwise

    Notes:
        Month must be 01-12, day must be 01-31
    """
    import re
    pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    return bool(re.match(pattern, date_str))


def is_valid_time(time_str: str) -> bool:
    """Check if time string matches 24-hour HH:MM format.

    Args:
        time_str: Time string to validate

    Returns:
        True if format is HH:MM (24-hour format), False otherwise

    Notes:
        Hour must be 00-23, minute must be 00-59

    Examples:
        >>> is_valid_time("09:30")
        True
        >>> is_valid_time("23:59")
        True
        >>> is_valid_time("24:00")
        False
        >>> is_valid_time("9:30")
        False  # Missing leading zero
    """
    import re
    pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(pattern, time_str))
