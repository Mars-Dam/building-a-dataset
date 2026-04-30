import datetime
import os
import sys

class Auth:
    def __init__(self):
        # 1. Get the absolute path of the folder where THIS script is saved
        # This ensures it works on Windows, Mac, or Linux without changes.
        self.base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.file = os.path.join(self.base_path, "users.txt")
        
        # 2. Create the file immediately if it doesn't exist
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                pass

    def register(self):
        username = input("Enter new username: ")
        password = input("Enter new password: ")

        # Using 'a' (append) mode
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"REGISTER,{username},{password},{datetime.datetime.now()}\n")
            f.flush() # Force the OS to write the data to disk
            
        print(f"User '{username}' registered. Saved to: {self.file}")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        if not os.path.exists(self.file):
            print("No user database found.")
            return None

        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("REGISTER"):
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        if username == parts[1] and password == parts[2]:
                            self.log("LOGIN", username)
                            print("Login Successful!")
                            return username

        print("Invalid Credentials")
        return None

    def log(self, action, username):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"{action},{username},{datetime.datetime.now()}\n")
            f.flush()

