import os
import subprocess

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_directory_abs, target_file_path])
        if valid_target_file_path != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except (OSError, ValueError) as e:
        return f'Error: Failed to process paths - {e}'

    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory_abs, timeout=30)
        if result.returncode != 0:
            return f'Error: Process exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            return 'Error: No output produced'
        output = f'STDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}'
    except subprocess.TimeoutExpired:
        return 'Error: Process timed out'
    except Exception as e:
        return f'Error: Failed to execute the file - {e}'
    return output