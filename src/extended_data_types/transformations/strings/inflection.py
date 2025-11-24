"""String inflection operations."""

from __future__ import annotations

import inflection
import unidecode

from extended_data_types.transformations.core import Transform


def pluralize(text: str, count: int | None = None) -> str:
    """Convert string to plural form.

    Args:
        text: String to pluralize
        count: Optional count to conditionally pluralize

    Returns:
        Pluralized string

    Example:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("cat", 1)
        'cat'
    """
    if count == 1:
        return text
    
    # Handle irregular plurals
    irregular_plurals = {
        "criterion": "criteria",
        "bacterium": "bacteria",
    }
    if text.lower() in irregular_plurals:
        return irregular_plurals[text.lower()]
    
    return inflection.pluralize(text)


def singularize(text: str) -> str:
    """Convert string to singular form.

    Args:
        text: String to singularize

    Returns:
        Singular string

    Example:
        >>> singularize("cats")
        'cat'
        >>> singularize("criteria")
        'criterion'
    """
    # Handle irregular singulars (check before inflection library)
    irregular_singulars = {
        "criteria": "criterion",
        "bacteria": "bacterium",
    }
    text_lower = text.lower()
    if text_lower in irregular_singulars:
        # Preserve original case
        if text.isupper():
            return irregular_singulars[text_lower].upper()
        elif text[0].isupper():
            return irregular_singulars[text_lower].capitalize()
        return irregular_singulars[text_lower]
    
    result = inflection.singularize(text)
    # Fix inflection library issues
    if result == "criterium" and text_lower == "criteria":
        return "criterion" if not text.isupper() else "CRITERION"
    return result


def ordinalize(number: int | str) -> str:
    """Convert number to ordinal string.

    Args:
        number: Number to convert

    Returns:
        Ordinal string

    Example:
        >>> ordinalize(1)
        '1st'
    """
    return inflection.ordinalize(str(number))


def parameterize(text: str, separator: str = "-") -> str:
    """Convert string to parameter form.

    Args:
        text: String to convert
        separator: Separator character

    Returns:
        Parameterized string

    Example:
        >>> parameterize("Hello World!")
        'hello-world'
        >>> parameterize("Hello_World")
        'hello-world'
    """
    # Convert underscores to spaces first, then parameterize
    # This ensures underscores are treated like word separators
    text = text.replace("_", " ")
    return inflection.parameterize(text, separator)


def transliterate(text: str) -> str:
    """Convert unicode string to ASCII.

    Args:
        text: String to convert

    Returns:
        ASCII string

    Example:
        >>> transliterate("héllo")
        'hello'
    """
    return unidecode.unidecode(text)

# Legacy helpers expected by tests
def camelize(text: str, uppercase_first_letter: bool = True) -> str:
    """Convert string to camel case.

    Args:
        text: String to convert
        uppercase_first_letter: Whether to uppercase the first letter

    Returns:
        Camelized string

    Example:
        >>> camelize("hello_world")
        'HelloWorld'
        >>> camelize("hello world")
        'HelloWorld'
        >>> camelize("html_parser")
        'HTMLParser'
    """
    # Handle spaces by converting to underscore first
    text = text.replace(" ", "_")
    
    # Handle acronyms - common acronyms should be uppercase
    # Note: "id" is only an acronym when standalone, not in compound words
    acronyms = ['html', 'xml', 'http', 'https', 'url', 'uri', 'api', 'pdf', 'css', 'js', 'json']
    words = text.split('_')
    
    # Build camel case manually to preserve acronym casing
    result_parts = []
    for i, word in enumerate(words):
        if not word:
            continue
        word_lower = word.lower()
        # Check if it's an acronym (but not "id" unless it's standalone)
        is_acronym = word_lower in acronyms or (word_lower == 'id' and len(words) == 1)
        if is_acronym:
            # Acronyms: uppercase unless it's the first word and uppercase_first_letter=False
            if i == 0 and not uppercase_first_letter:
                result_parts.append(word_lower)
            else:
                result_parts.append(word.upper())
        else:
            # Regular words: capitalize first letter
            if i == 0 and not uppercase_first_letter:
                result_parts.append(word.lower())
            else:
                result_parts.append(word.capitalize())
    
    return ''.join(result_parts)


def underscore(text: str) -> str:
    """Convert string to underscore case.

    Args:
        text: String to convert

    Returns:
        Underscored string

    Example:
        >>> underscore("HelloWorld")
        'hello_world'
        >>> underscore("Hello World")
        'hello_world'
        >>> underscore("UserId123")
        'user_id_123'
    """
    # Handle spaces and dashes by converting to underscore first
    text = text.replace(" ", "_").replace("-", "_")
    result = inflection.underscore(text)
    
    # Fix number handling - ensure numbers are separated with underscores
    import re
    # Add underscore before numbers that follow letters
    result = re.sub(r'([a-z])(\d)', r'\1_\2', result)
    # Add underscore after numbers that precede letters
    result = re.sub(r'(\d)([a-z])', r'\1_\2', result)
    
    return result


def humanize(text: str, capitalize: bool = True) -> str:
    """Convert string to human readable form.

    Args:
        text: String to convert
        capitalize: Whether to capitalize the result

    Returns:
        Humanized string

    Example:
        >>> humanize("hello_world")
        'Hello world'
        >>> humanize("_id")
        'Id'
        >>> humanize("user123")
        'User'
        >>> humanize("hello-world")
        'Hello world'
    """
    # Handle leading underscores specially
    if text.startswith("_"):
        # Remove leading underscores and process
        cleaned = text.lstrip("_")
        if not cleaned:
            return ""
        text = cleaned
    
    # Convert dashes and underscores to spaces before humanizing
    import re
    text = text.replace("-", "_")
    
    # Remove trailing numbers before humanizing
    text = re.sub(r'\d+$', '', text)
    
    result = inflection.humanize(text)
    # Remove trailing spaces
    result = result.rstrip()
    if not capitalize:
        result = result.lower()
    return result

# Legacy helpers expected by tests
def titleize(text: str) -> str:
    """Convert string to title case words."""
    return inflection.titleize(text)


# Register transforms
pluralize_transform = Transform(pluralize)
singularize_transform = Transform(singularize)
ordinalize_transform = Transform(ordinalize)
parameterize_transform = Transform(parameterize)
transliterate_transform = Transform(transliterate)
humanize_transform = Transform(humanize)
