


def test_add(client, auth):
    # should be redirected because not logged in
    assert client.get('/add').status_code == 302

    auth.login()

    # if not logged in, should be redirected, else 200
    assert client.get('/add').status_code == 200

    # test if tasks adds correctly
    resp = client.post('/add', data={'task': 'test_task'})
    assert b'test_task' in resp.data

    # test tasks deleteing
    # since each time We launch test, temporary database
    # created and then deleted, We can be sure that our
    # newly added task's id == 1
    resp = client.post('/done/1')
    assert b'test_task' not in resp.data


def test_index(client, auth):
    auth.login()

    # first add the task
    client.post('/add', data={'task': 'test_task'})
    # now check if it is on index page
    resp = client.get('/')
    assert b'test_task' in resp.data

    # as a bonus, test if username is shown (in navbar)
    assert b'test_bot1' in resp.data

