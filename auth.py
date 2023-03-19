"""
Simulated Authentication Function
"""

PASSWORD = "0123456789"


def validate(password):
    """
    This method receives an string as a parameter,
    compares it to the global PASSWORD constant,
    and returns True if they match, and False
    otherwise.

    It is a very bad implementation of a password,
    validation function, to make it vulnerable to
    timing attacks.
    """

    # Return immediately when password length don't match
    if len(password) != len(PASSWORD):
        return False

    # Compare password element wise
    # pylint: disable=consider-using-enumerate
    for i in range(len(PASSWORD)):
        if PASSWORD[i] != password[i]:
            return False

    # If everything is good, then return True
    return True
