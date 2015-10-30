

class UserManager:
    def __init__(self, client):
        self.client = client

        self.loggedin_info = None

    def login(self, username, password):
        args = dict(username=username, password=password, method='login')
        response = self.client.call(args)

        self.loggedin_info = response

        return response

    def register(self, username, password, email, first_name, last_name):
        args = dict(username=username, password=password, email=email, first_name=first_name, last_name=last_name, method='register')
        response = self.client.call(args)

        return response
