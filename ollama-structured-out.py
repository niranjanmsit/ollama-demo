from ollama import chat
from pydantic import BaseModel

import main

class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]

def get_country_info(query: str):
    print(f"Getting country info for {query}")
    response = chat(
    model='gemma3:4b',
    messages=[{'role': 'user', 'content': query}],
    format=Country.model_json_schema(),
    )
    return response.message.content;

def get_country_info_stream(query: str):
    """
    Get country info with streaming response.
    
    Args:
        query: The query about a country (e.g., "Tell me about Canada")
    
    Returns:
        The complete response text that can be parsed as JSON
    """
    print(f"Getting country info for {query}")
    print("Assistant: ", end="", flush=True)
    
    response_text = ""
    for chunk in chat(
        model='gemma3:4b',
        messages=[{'role': 'user', 'content': query}],
        format=Country.model_json_schema(),
        stream=True
    ):
        content = chunk.message.content
        print(content, end="", flush=True)
        response_text += content
    
    print()  # New line after streaming
    return response_text


if __name__ == "__main__":
    query = input("Enter a country name: ")
    response = get_country_info_stream(query)
    country = Country.model_validate_json(response)
    print(country)