# smart_chunker.py

def chunk_text(text, max_tokens=7000):
    """
    Splits raw feat text into safe chunks based on max_tokens (~4 chars per token)
    """
    max_chars = max_tokens * 4
    lines = text.splitlines()
    chunks = []
    buffer = ""

    for line in lines:
        if len(buffer) + len(line) < max_chars:
            buffer += line + "\n"
        else:
            chunks.append(buffer.strip())
            buffer = line + "\n"

    if buffer:
        chunks.append(buffer.strip())

    return chunks
  
