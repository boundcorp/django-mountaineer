from fastapi.testclient import TestClient


from example.app import app_controller

client = TestClient(app_controller.app)

def test_read_main():
    pass