import ollama
import sys
from typing import Optional


class Chatbot:
    """A chatbot interface using local Ollama."""
    
    def __init__(self, model: str = "gemma3:4b"):
        """
        Initialize the chatbot with a specific model.
        
        Args:
            model: The Ollama model to use (default: "llama2")
        """
        self.model = model
        self.conversation_history = []
        
    def chat(self, message: str, stream: bool = True) -> str:
        """
        Send a message to the chatbot and get a response.
        
        Args:
            message: The user's message
            stream: Whether to stream the response (default: True)
            
        Returns:
            The chatbot's response
        """
        if not message.strip():
            return ""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            if stream:
                response_text = ""
                print("\nAssistant: ", end="", flush=True)
                for chunk in ollama.chat(
                    model=self.model,
                    messages=self.conversation_history,
                    stream=True
                ):
                    content = chunk['message']['content']
                    print(content, end="", flush=True)
                    response_text += content
                print("\n")  # New line after streaming
                
                # Add assistant response to history
                self.conversation_history.append({"role": "assistant", "content": response_text})
                return response_text
            else:
                response = ollama.chat(
                    model=self.model,
                    messages=self.conversation_history
                )
                response_text = response['message']['content']
                
                # Add assistant response to history
                self.conversation_history.append({"role": "assistant", "content": response_text})
                return response_text
                
        except Exception as e:
            error_msg = f"Error: {e}"
            print(f"\n{error_msg}")
            return error_msg
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.\n")
    
    def list_models(self):
        """List available Ollama models."""
        try:
            models = ollama.list()
            print("\nAvailable models:")
            for model in models['models']:
                print(f"  - {model['name']}")
            print()
        except Exception as e:
            print(f"\nError listing models: {e}\n")


def main():
    """Main function to run the chatbot."""
    print("=" * 60)
    print("AI Chatbot with Local Ollama")
    print("=" * 60)
    print("\nCommands:")
    print("  /help     - Show this help message")
    print("  /clear    - Clear conversation history")
    print("  /models   - List available Ollama models")
    print("  /model <name> - Switch to a different model")
    print("  /quit     - Exit the chatbot")
    print("\n" + "=" * 60 + "\n")
    
    # Initialize chatbot
    chatbot = Chatbot()
    
    # Check if model is available
    try:
        # Try to pull the model if it doesn't exist
        ollama.list()
    except Exception as e:
        print(f"Warning: Could not connect to Ollama. Make sure Ollama is running.")
        print(f"Error: {e}\n")
        print("To start Ollama, run: ollama serve")
        print("To pull a model, run: ollama pull llama2\n")
        return
    
    print(f"Using model: {chatbot.model}")
    print("Type your message or use /help for commands.\n")
    
    # Main chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower().split()[0]
                
                if command == "/quit" or command == "/exit":
                    print("\nGoodbye!")
                    break
                elif command == "/help":
                    print("\nCommands:")
                    print("  /help     - Show this help message")
                    print("  /clear    - Clear conversation history")
                    print("  /models   - List available Ollama models")
                    print("  /model <name> - Switch to a different model")
                    print("  /quit     - Exit the chatbot\n")
                elif command == "/clear":
                    chatbot.clear_history()
                elif command == "/models":
                    chatbot.list_models()
                elif command == "/model":
                    parts = user_input.split()
                    if len(parts) > 1:
                        new_model = parts[1]
                        chatbot.model = new_model
                        chatbot.clear_history()
                        print(f"Switched to model: {new_model}\n")
                    else:
                        print("Usage: /model <model_name>\n")
                else:
                    print(f"Unknown command: {command}. Type /help for available commands.\n")
            else:
                # Regular chat message
                chatbot.chat(user_input)
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
