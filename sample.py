import bcrypt

# Hash password for super admin
password = "adminpass".encode("utf-8")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
print("Super Admin Hashed Password:", hashed_password)

# Hash password for doctor
password = "docpass".encode("utf-8")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
print("Doctor Hashed Password:", hashed_password)