from kairo import Kairo

def test_Kairo_object_exists():
    assert Kairo != None

def test_Kairo_object_takes_name():
    k = Kairo("app")
    assert True