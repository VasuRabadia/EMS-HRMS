import os
import uuid
import secrets

digits = 16
os_secret_key = os.urandom(digits)
print(os_secret_key)

uuid_secret_key = uuid.uuid4().hex
print(uuid_secret_key)

secrets_secret_key = secrets.token_urlsafe(digits)
print(secrets_secret_key)
