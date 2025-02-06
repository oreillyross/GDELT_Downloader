
def load_event_codes():
    """
    Reads CAMEO event codes from the text file and returns a dictionary mapping
    codes to their descriptions.
    
    Returns:
        dict: Keys are event codes, values are their descriptions
    """
    event_codes = {}
    with open("utils/CAMEO.eventcodes.txt", 'r') as file:
        next(file)  # Skip header line
        for line in file:
            code, description = line.strip().split('\t')
            event_codes[code] = description
    return event_codes

if __name__ == "__main__":
    # Test the function
    codes = load_event_codes()
    print(f"Total event codes loaded: {len(codes)}")
    # Example lookup
    print("\nExample lookups:")
    print(f"Code '010': {codes['010']}")
    print(f"Code '2042': {codes['2042']}")
