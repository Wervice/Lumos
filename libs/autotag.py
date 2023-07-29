def find_repeating_strings(strings_list):
    repeating_strings = []
    seen_strings = set()

    for string in strings_list:
        string.split("-").split("_")
        if string.startswith('-') or string.startswith('_'):
            # Check if the string is already in the set of seen_strings
            if string in seen_strings:
                repeating_strings.append(string)
            else:
                seen_strings.add(string)

    return repeating_strings

# Example usage:
strings_list = ["-apple", "_banana", "orange", "_banana", "pear", "-apple", "_kiwi"]
repeating_strings = find_repeating_strings(strings_list)
print("Repeating strings:", repeating_strings)