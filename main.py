import os
import sys
import types
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv(dotenv_path="apikey.env")
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

sys_arg = sys.argv
if not len(sys_arg) >= 2:
    print('Usage: python3 main.py "AI prompt"')
    sys.exit(1)

prompt = sys_arg[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file content
- Rewrite file content
- Run python file with arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

sys_config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=sys_config
)

func_calls = response.function_calls

if len(sys_arg) >= 3 and '--verbose' in sys_arg:
    print(f"User prompt: {prompt}")
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    if func_calls == None:
        print(response.text)
    else:
        for function_call_part in func_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    if func_calls == None:
        print(response.text)
    else:
        for function_call_part in func_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
