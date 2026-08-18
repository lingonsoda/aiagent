import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path:str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_directory_abs, target_file_path])
        if valid_target_file_path != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except (OSError, ValueError) as e:
        return f'Error: Failed to process paths - {e}'

    try:
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regualar file: "{file_path}"'
    except OSError as e:
        return f'Error: Could not check file - {e}'

    content = ""
    with open(target_file_path, 'r') as f:
        try:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        except Exception as e:
            return f'Error: Could not read file content - {e}'
    return content