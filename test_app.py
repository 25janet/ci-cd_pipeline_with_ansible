from app import get_status,get_healthy

def test_get_status_return_exact_string():
    """Verify get_status() returns the expected exact string"""
    assert get_status() == "Devops Task Tracker is running"

def test_get_status_return_string_type():
    """Verify the return value is a string type only"""
    assert isinstance(get_status(),str)

def test_get_health_return_healthy():
    """Verify get_health() returns the expected exact string"""
    assert get_healthy() == "I am healthy"