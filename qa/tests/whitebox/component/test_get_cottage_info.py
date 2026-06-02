from unittest.mock import MagicMock
from dev.db.db_client import DBClient


def test_get_cottage_info():
    db = DBClient()

    mock_cursor = MagicMock()
    db.connection = MagicMock()
    db.connection.cursor = mock_cursor

    mock_cursor.fetchone.return_value = [
        1,
        "Metanoia",
        350.00,
        "5",
        "available"
    ]

    result = db.get_cottage_info_from_db()

    assert isinstance(result, list)
    assert result[0] == 1
    assert result[1] == "Metanoia"
    assert result[4] == "available"
