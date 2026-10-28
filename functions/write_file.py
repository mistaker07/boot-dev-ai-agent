import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs_path =  os.path.abspath(working_directory)
        file_dir = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        # Will be True or False
        valid_file_dir = os.path.commonpath([working_directory_abs_path, file_dir]) == working_directory_abs_path

        if not valid_file_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file_dir), exist_ok=True)

        with open(file_dir, mode="w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
