import secrets
key = secrets.token_urlsafe(32)
if __name__ == '__main__':
    print(key)