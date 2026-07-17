from worker.tasks import add, ping


def test_add() -> None:
    assert add.delay(2, 3).get() == 5


def test_ping() -> None:
    assert ping.delay().get() == "pong"
