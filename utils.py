# utils.py

def is_float(value):
    """
    Checks if the provided value can be converted to a float.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if convertible to float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
