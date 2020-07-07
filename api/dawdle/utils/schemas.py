from dawdle.utils import remove_extra_whitespace


def trim_string(in_data, key):
    value = in_data.get(key)
    if isinstance(value, str):
        trimmed = remove_extra_whitespace(value)
        if trimmed:
            in_data[key] = trimmed
        else:
            del in_data[key]
