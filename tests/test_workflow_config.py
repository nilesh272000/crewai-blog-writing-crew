import os

os.environ["MOCK_MODE"] = "true"

from crewai_blog.config import default_target_words, is_mock_mode


def test_mock_mode():
    assert is_mock_mode() is True


def test_default_target_words():
    assert default_target_words() == 1200
