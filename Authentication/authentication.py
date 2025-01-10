import hashlib

def hash_passcode(passcode: str) -> str:
    return hashlib.sha256(passcode.encode('utf-8')).hexdigest()

VALID_CLIENT_PASSCODE_HASH = hash_passcode("mypasscode")
VALID_MESSAGE_PASSCODE_HASH = hash_passcode("mymessagepasscode")

def authenticate_client(passcode: str) -> bool:
    return hash_passcode(passcode) == VALID_CLIENT_PASSCODE_HASH

def authenticate_message(passcode: str) -> bool:
    return hash_passcode(passcode) == VALID_MESSAGE_PASSCODE_HASH