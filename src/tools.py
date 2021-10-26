def format_file_size(size):
    unit_arr = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    final_unit_idx = 0
    while size > 1024:
        size = int(size / 1024)
        final_unit_idx = final_unit_idx + 1
    return str(size) + ' ' + unit_arr[final_unit_idx]


def sort_tags_by_type(arr):
    todo_arr = []
    http_arr = []
    rest_arr = []
    for item in arr:
        if is_type(item, "TODO"):
            todo_arr.append(item)
        elif is_type(item, "http"):
            http_arr.append(item)
        else:
            rest_arr.append(item)
    return todo_arr + rest_arr + http_arr


def is_type(strs, type_name):
    return strs.startswith(type_name)