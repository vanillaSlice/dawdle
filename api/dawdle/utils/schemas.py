def trim_string(in_data, key):
    if key in in_data:
        trimmed = " ".join(in_data[key].split())
        if trimmed:
            in_data[key] = trimmed
        else:
            del in_data[key]
