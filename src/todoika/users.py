class User:
    def __init__(self, db_id, username, password, default_list_id):
        self.db_id = db_id
        self.username = username
        self.password = password
        self.default_list_id = default_list_id

    def __repr__(self):
        return f"[{self.db_id}] {self.username}, default list: {self.default_list_id}"
