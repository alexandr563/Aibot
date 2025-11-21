import os
import subprocess
import types
from dotenv import load_dotenv
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
        

    child = os.path.abspath(full_path)
    parent = os.path.abspath(working_directory)
    if not child.startswith(parent):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        cmd = ['python3', full_path] + args
        result = subprocess.run(cmd, timeout = 30, capture_output=True, text=True, check=False)
    
        output_parts = []
        
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout.strip()}")
            
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr.strip()}")
            
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            

        return "\n".join(output_parts) if output_parts else "No output produced."
        
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="execute python file, constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute a Python file inside the allowed working directory. Returns STDOUT/STDERR and exit information.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of string arguments to pass to the script.",
                items=types.Schema(type=types.Type.STRING),
            )
        },
    ),
)
