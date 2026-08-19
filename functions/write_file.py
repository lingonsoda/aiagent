import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_directory_abs, target_file_path])
        if valid_target_file_path != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except (OSError, ValueError) as e:
        return f'Error: Failed to process paths - {e}'

    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        with open(target_file_path, 'w') as f:
            f.write(content)
    except OSError as e:
        return f'Error: Could not write to file - {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'   