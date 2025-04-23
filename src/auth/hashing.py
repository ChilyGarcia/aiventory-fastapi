import bcrypt

def hash_password(password: str) -> str:
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Generar el salt y hacer el hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Devolver el hash como string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convertir las contraseñas a bytes
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Verificar
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
