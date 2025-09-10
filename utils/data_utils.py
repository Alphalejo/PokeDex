import re

def clean_text(data):
    cleaned = {}
    for version, text in data.items():
        # Remove control characters and soft hyphens
        text = text.replace('\x0c', ' ').replace('\xad', '')
        # Replace newlines with spaces
        text = text.replace('\n', ' ')
        # Normalize multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        cleaned[version] = text
    return cleaned
