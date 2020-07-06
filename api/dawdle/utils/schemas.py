from dawdle.utils import remove_extra_whitespace


def trim_string(in_data, key):
    if key in in_data:
        trimmed = remove_extra_whitespace(in_data[key])
        if trimmed:
            in_data[key] = trimmed
        else:
            del in_data[key]
