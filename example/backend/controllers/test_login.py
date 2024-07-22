from fastapi.testclient import TestClient


from frontend.app import app_controller

client = TestClient(app_controller.app)

def test_read_main():
    pass