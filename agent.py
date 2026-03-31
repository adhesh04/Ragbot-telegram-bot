from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:7b")

conversation_history = []

def ask_agent(question: str) -> str:
    global conversation_history
    
    conversation_history.append(f"User: {question}")
    
    full_prompt = "\n".join(conversation_history) + "\nAssistant:"
    
    try:
        response = llm.invoke(full_prompt)
        conversation_history.append(f"Assistant: {response}")
        
        # Keep history from growing too large
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        
        return response
    except Exception as e:
        return f"Error talking to Ollama: {str(e)}"