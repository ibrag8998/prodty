# ==============
# === CREATE ===
# ==============

add_user = '\
INSERT INTO user (username, password) \
VALUES (?, ?)'

add_task = '\
INSERT INTO task (author_id, content) \
VALUES (?, ?)'

# ==============
# ==== READ ====
# ==============

get_user_by_username = '\
SELECT * \
FROM user \
WHERE username = ?'

get_user_tasks = '\
SELECT * \
FROM task \
INNER JOIN user \
ON user.id = task.author_id \
WHERE user.id = ? \
ORDER BY pub_date DESC'

# ==============
# === UPDATE ===
# ==============



# ==============
# === DELETE ===
# ==============

delete_task_by_id = '\
DELETE \
FROM task \
WHERE id = ?'

