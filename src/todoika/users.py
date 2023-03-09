class User:
    def __init__(self, db_id, username, default_list_id):
        self.db_id = db_id
        self.username = username
        self.default_list_id = default_list_id

    def __repr__(self):
        return f"User({self.db_id}, {self.username}, {self.default_list_id}"
