import re


def convert_datetime_str(dt_str):
    """
    Attempts to convert a date string with potential leading text to desired format.

    Args:
      dt_str: The input string containing the date in a specific format.

    Returns:
      The converted date string in the desired format ("YYYYMMDD HHMMSS") or None if unsuccessful.
    """

    # Try to extract date and time groups using a regular expression.
    match = re.search(r"(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}.\d{2}.\d{2})", dt_str)
    if match is None:
        return None  # Handle no match scenario

    # Unpack groups only if a match is found
    print(match)
    print(type(match))
    year, month, day, hour, minute = match.groups()

    # Combine extracted values into desired format
    converted_str = f"{year:02d}{month:02d}{day:02d} {hour:02d}{minute:02d}"

    return converted_str


# Test cases
test_strings = [
    "Screenshot 2023-12-16 at 20.03.01",
    # "Image 2024-02-29 at 11.45.23",  # Include a potentially non-existent date (February 29th)
]

for dt_str in test_strings:
    converted_str = convert_datetime_str(dt_str)
    if converted_str is not None:
        print(f"Converted string for '{dt_str}': {converted_str}")
    else:
        print(f"Input string '{dt_str}' does not match the expected format.")
