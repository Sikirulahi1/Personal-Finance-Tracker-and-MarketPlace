import secrets

def generate_secret_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Example usage
if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:", secret_key)
