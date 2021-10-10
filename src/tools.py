def format_file_size(size):
    unit_arr = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    final_unit_idx = 0
    while size > 1024:
        size = int(size / 1024)
        final_unit_idx = final_unit_idx + 1
    return str(size) + ' ' + unit_arr[final_unit_idx]
