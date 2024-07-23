from .controllers import find_controllers


def test_find_controllers():
    test_controller = list(find_controllers(["backend/controllers"]))
    assert test_controller == []
