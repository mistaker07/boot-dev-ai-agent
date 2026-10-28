import os


MAX_CHARACTERS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs_path =  os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_directory_abs_path, target_file]) == working_directory_abs_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as file:
            content = file.read(MAX_CHARACTERS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'

            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARACTERS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
