import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_functions import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("Environment variable OPENROUTER_API_KEY not found")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = []
for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
        tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("Error during connection to the client")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")


    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls is None:
        print(response.choices[0].message.content)
        break
    else:
        print(message.tool_calls)
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call, function_args)

            if result_message["content"] == '':
                raise Exception("Content is empty")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)

            if _ == 20:
                sys.exit("Could not find a solution in 20 iterations")
