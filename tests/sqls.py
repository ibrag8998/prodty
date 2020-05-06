from werkzeug.security import generate_password_hash


add_users = "\
INSERT INTO user (username, password) \
VALUES \
('test_bot1', '{}'), \
('test_bot2', '{}')".format(
    generate_password_hash('tester1'),
    generate_password_hash('tester2')
)


add_tasks = "\
INSERT INTO task (content, author_id) \
VALUES \
('test_task_from_bot1', 1), \
('test_task_from_bot2', 2)"

get_user_by_username = '\
SELECT * \
FROM user \
WHERE username = ?'

