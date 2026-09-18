from core import greeting


def test_greeting_falls_back_to_world() -> None:
    assert greeting("   ") == "Hello, world!"


def test_greeting_uses_name() -> None:
    assert greeting("Ada") == "Hello, Ada!"
