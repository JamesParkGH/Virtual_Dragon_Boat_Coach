import os

def check_credentials(username, password):
    file_path = os.path.join(os.path.dirname(__file__), "credentials.txt")

    with open(file_path, "r") as file:
        for line in file:
            saved_username, saved_password = line.strip().split(",")

            if username == saved_username and password == saved_password:
                return True

    return False
