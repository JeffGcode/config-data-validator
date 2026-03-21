import pytest
from src.validator.data_validator import validate_csv
from src.validator.exceptions import ValidationError

def test_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("id,name\n1,Alice")
    # Updated regex to match the new error message
    with pytest.raises(ValidationError, match="missing required columns"):
        validate_csv(str(bad_csv))

def test_missing_values(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("id,email,age\n1,alice@example.com,\n")
    with pytest.raises(ValidationError, match="missing"):
        validate_csv(str(bad_csv))

def test_invalid_email(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("id,email,age\n1,bademail,25\n")
    with pytest.raises(ValidationError, match="missing '@'"):
        validate_csv(str(bad_csv))

def test_valid_csv(tmp_path):
    good_csv = tmp_path / "good.csv"
    good_csv.write_text("id,email,age\n1,test@test.com,30\n2,user@domain.com,25")
    df = validate_csv(str(good_csv))
    assert len(df) == 2
