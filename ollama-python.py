import ollama

# Non-streaming chat
def chat_non_streaming(model='gemma3:4b', messages=None):
    """
    Chat with Ollama using non-streaming for real-time responses.
    
    Args:
        model: The model to use (default: 'gemma3:4b')
        messages: List of message dictionaries with 'role' and 'content'
    """
    if messages is None:
        response = ollama.chat(model='gemma3:4b', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
        ])
        print(response['message']['content'])

# Streaming chat method
def chat_stream(model='gemma3:4b', messages=None):
    """
    Chat with Ollama using streaming for real-time responses.
    
    Args:
        model: The model to use (default: 'gemma3:4b')
        messages: List of message dictionaries with 'role' and 'content'
    
    Returns:
        The complete response text
    """
    if messages is None:
        messages = [
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
        ]
    
    response_text = ""
    print("Assistant: ", end="", flush=True)
    
    for chunk in ollama.chat(
        model=model,
        messages=messages,
        stream=True
    ):
        content = chunk['message']['content']
        print(content, end="", flush=True)
        response_text += content
    
    print()  # New line after streaming
    return response_text

# Example usage of streaming chat
if __name__ == "__main__":
    chat_stream()