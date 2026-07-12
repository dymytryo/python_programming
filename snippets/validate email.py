def is_valid_email(email: str) -> bool:
    """
    Validates if the given string meets common email address requirements.

    Args:
        email (str): The email string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern: Pattern[str] = re.compile(r'^[a-zA-Z0-9._%&+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    return bool(pattern.match(email))


def test_is_valid_email():
    assert is_valid_email("test@example.com")
    assert is_valid_email("test.email+regex@example.com")
    assert is_valid_email("test@subdomain.example.co.uk")
    assert not is_valid_email("test")
    assert not is_valid_email("test@.com")
    assert not is_valid_email("test@com")
    assert not is_valid_email("@example.com")
    print("All tests passed!")

test_is_valid_email()
