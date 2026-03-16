import hashlib

def hasheo(password):
    return hashlib.sha256(password.encode()).hexdigest()