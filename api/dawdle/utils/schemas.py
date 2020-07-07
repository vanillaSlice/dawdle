from dawdle.utils import remove_extra_whitespace


def trim_string(in_data, key):
    value = in_data.get(key)

    if not isinstance(value, str):
        return

    trimmed = remove_extra_whitespace(value)

    if not trimmed:
        del in_data[key]
        return

    in_data[key] = trimmed
