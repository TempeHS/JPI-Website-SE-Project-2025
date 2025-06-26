import re

# Function to sanitise user input to prevent SQL injection
def sanitize_input(user_input: str) -> str:
    # Replace single quotes with two single quotes 
    sanitized = user_input.replace("'", "''")
    # Remove common SQL injection keywords 
    sanitized = re.sub(r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|OR|AND|--|;)\b", "", sanitized)
    # Remove semicolons and double dashes
    sanitized = sanitized.replace(";", "").replace("--", "")
    return sanitized