import os
import types
from dotenv import load_dotenv
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    
    child = os.path.abspath(full_path)
    parent = os.path.abspath(working_directory)
    if not child.startswith(parent):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
 
    path_list = full_path.split('/')
    path_list.pop()
    path_without_file = '/'.join(path_list)    
    
    try:
        if not os.path.exists(path_without_file):
            os. mkdir(path_without_file)
    
        with open(full_path, "w") as f:
            f.write(content)
    except:
        return 'Error:'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Rerewrite file contents for files constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to rewrite, relative to the working directory.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description='content which will be rewritten'
                )
            
        },
    ),
)
