from backend.db import *


def get_user_by_id(user_id):
    return query_single("SELECT * FROM users WHERE id = ?", user_id)
