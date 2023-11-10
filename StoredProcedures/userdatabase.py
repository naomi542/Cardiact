class UserDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, firstname, lastname = line.strip().split(";")
            self.users[email] = (password, firstname, lastname)

        self.file.close()

    def login(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    #not sure if this method is needed
    def get_user(self, email):
        if email in self.users:
            return True
        else:
            return False

    def add_user(self, firstname, lastname, email, password):
        if email not in self.users:
            self.users[email.strip()] = (password.strip(), firstname.strip(), lastname.strip())
            self.save()
            return True
        else:
            #account with that email already exists; show some error on UI
            return False

    def delete_user(self, email):
        #should call get_user before to ask for confirmation or something
        del self.users[email]

    def save(self):
        with open(self.filename, "w") as file:
            for user in self.users:
                file.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

