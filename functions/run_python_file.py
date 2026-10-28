import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs_path =  os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs_path, target_file]) == working_directory_abs_path

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if not args is None:
            command.extend(args)

        output = subprocess.run(command, check=True, text=True, timeout=30, capture_output=True)

        if output.returncode != 0:
            return f"Process exited with code {output.returncode}"

        if output.stdout is None and output.stderr is None:
            return "No output produced"

        return f"STDOUT: {output.stdout} STDERR: {output.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "If asked to run Python file, it executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
