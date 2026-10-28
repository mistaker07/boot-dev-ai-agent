import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs_path =  os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs_path, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs_path, target_dir]) == working_directory_abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for item in os.listdir(target_dir):
            item_abs = os.path.join(target_dir, item)
            entries.append(f"{item}: file_size={os.path.getsize(item_abs)} bytes, is_dir={os.path.isdir(item_abs)}")

        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
