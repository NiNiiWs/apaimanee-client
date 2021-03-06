from .base import Manager

class UserManager(Manager):
    def __init__(self, client):
        super().__init__(client)

        self.loggedin_info = None

    def get_token(self):
        if self.is_loggedin():
            return self.loggedin_info['token']
        return None

    def login(self, username, password):
        args = dict(username=username, password=password)
        response = self.call('login',args)

        if 'responses' in response:
            self.loggedin_info = response.get('responses')

        return response

    def register(self, username, password, email, first_name, last_name):
        args = dict(username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        response = self.call('register', args)

        return response

    def is_loggedin(self):
        if self.loggedin_info is not None:
            if 'token' in self.loggedin_info:
                return True

        return False
