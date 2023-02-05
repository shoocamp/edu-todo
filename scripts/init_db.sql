DROP TABLE IF EXISTS lists;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE lists
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT    NOT NULL,
    user_id     INTEGER NOT NULL,
    CONSTRAINT FK_user_id FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT uq_lists UNIQUE (user_id, description)
);

CREATE TABLE users
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT UNIQUE,
    password_md5 TEXT,
    default_list INTEGER,
    CONSTRAINT FK_default_list FOREIGN KEY (default_list) REFERENCES lists (id)
);

CREATE TABLE tasks
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT    NOT NULL,
    status      TEXT    NOT NULL,
    created     INTEGER NOT NULL,
    due_date    INTEGER,
    notes       TEXT,
    list_id     INTEGER NOT NULL,
    user_id     INTEGER NOT NULL,
    CONSTRAINT FK_list_id FOREIGN KEY (list_id) REFERENCES lists (id),
    CONSTRAINT FK_user_id FOREIGN KEY (user_id) REFERENCES users (id)
);
