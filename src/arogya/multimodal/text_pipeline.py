# Normalize raw text input
def process_text(text : str) -> dict:
    return {
        "type": "text",
        "content": text.strip(),
        "metadata": {
            "source": "user_input"
        }
    }