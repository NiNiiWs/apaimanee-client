

class UserManager:
    def __init__(self, client):
        self.client = client

        self.loggedin_info = None

    def login(self, username, password):
        args = dict(username=username, password=password, method='login')
        response = self.client.call(args)

        self.loggedin_info = response

        return response['loggedin']

