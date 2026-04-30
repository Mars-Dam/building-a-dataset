import datetime


class Auth:
    def __init__(self):
        self.file = "login.txt"

    def register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        with open(self.file, "a") as f:
            f.write(f"REGISTER,{username},{password},{datetime.datetime.now()}\n")

        print("User Registered Successfully")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        with open(self.file, "r") as f:
            users = f.readlines()

        for user in users:
            if "REGISTER" in user:
                data = user.strip().split(",")
                if username == data[1] and password == data[2]:
                    self.log("LOGIN", username)
                    print("Login Successful")
                    return username

        print("Invalid Credentials")
        return None

    def logout(self, username):
        self.log("LOGOUT", username)
        print("Logged Out")