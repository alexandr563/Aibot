import os
import types
from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    child = os.path.abspath(full_path)
    parent = os.path.abspath(working_directory)
    if not child.startswith(parent):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    list_in_dir = os.listdir(full_path)
    
    list_of_str = []
    for item in list_in_dir:
        item_path = os.path.join(full_path, item) 
        str = f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}'
        list_of_str.append(str)
    
    return '\n'.join(list_of_str)
   

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)