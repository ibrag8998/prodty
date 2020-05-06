from prodty import create_app


# test if create_app() :test_config: parameter works properly
def test_config():
    # when no test_config is passed, check if TESTING is False
    assert not create_app().testing
    # inverse
    assert create_app({'TESTING': True}).testing


# test the example hello view
def test_hello(client):
    resp = client.get('/hello')
    assert resp.data == b'Hello!'

