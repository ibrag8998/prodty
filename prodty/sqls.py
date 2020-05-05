add_user = '\
INSERT INTO user (username, password) \
VALUES (?, ?)'

get_user_by_username = '\
SELECT * \
FROM user \
WHERE username = ?'

