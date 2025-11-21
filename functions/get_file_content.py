import os
import types
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    child = os.path.abspath(full_path)
    parent = os.path.abspath(working_directory)
    if not child.startswith(parent):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    MAX_CHARS = 10000

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except:
        return 'Error:'
        
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents for file constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to read from, relative to the working directory.",
            ),
        },
    ),
)