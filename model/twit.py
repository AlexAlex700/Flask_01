from model.user import User

class Twit:
    def __init__(self, body: str, author: User):
        self.body = body
        self.author = author