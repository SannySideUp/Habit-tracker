import secrets

secrets.token_hex(16)

def generateRandomUserID():
    UUID = secrets.token_hex(16)
    return UUID