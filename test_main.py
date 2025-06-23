import pytest
from api import extract_video_ids

@pytest.mark.parametrize("input_url,expected_id", [
    ("https://www.youtube.com/watch?v=DQdB7wFEygo", "DQdB7wFEygo"),
    ("https://www.youtube.com/watch?v=DQdB7wFEygo&t=48s", "DQdB7wFEygo"),
    ("DQdB7wFEygo", "DQdB7wFEygo"),
    ("https://www.youtube.com/watch?t=48s", ""),  # no v param
])
def test_extract_video_id(input_url, expected_id):
    assert extract_video_ids(input_url) == expected_id