def validate_api_key(api_key):
    valid_keys = ['valid_key1', 'valid_key2', 'valid_key3']  # List of valid API keys

    if api_key in valid_keys:
        return True
    else:
        return False

# Example usage:
provided_key = input("Enter your API key: ")
if validate_api_key(provided_key):
    print("API key is valid. Access granted.")
else:
    print("Invalid API key. Access denied.")
