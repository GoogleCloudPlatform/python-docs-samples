import pytest
import tempfile
import add_dags_to_composer
# fixture of valid directory

# fixture of empty directory
@pytest.fixture(scope="function")
def empty_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir

# fixture of composer storage bucket
#TODO: implement
@pytest.fixture(scope="function")
def bucket():
    yield "leah-playground"

# create dags list
## test invalid directory
def test_create_dags_list_invalid_directory():
    with pytest.raises(FileNotFoundError):
        (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")

## test valid directory
#TODO: implement
def test_create_dags_list():
    (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")
    assert len(dags) > 0

# upload
#TODO: implement
## test no files in directory
def test_upload_dags_to_composer_no_files(capsys, empty_directory, bucket):
    add_dags_to_composer.upload_dags_to_composer(empty_directory, bucket)
    out, _ = capsys.readouterr()
    assert "No DAGs to upload." in out
## test invalid permissions
#TODO: implement
def test_upload_dags_to_composer_insufficient_permissions(capsys):
    add_dags_to_composer.upload_dags_to_composer("this-directory-does-not-exist/", "not-a-bucket")
    out, _ = capsys.readouterr()
    assert "this is a dag" in out
## test successful upload
#TODO: implement
def test_upload_dags_to_composer(capsys):
    add_dags_to_composer.upload_dags_to_composer("this-directory-does-not-exist/", "not-a-bucket")
    out, _ = capsys.readouterr()
    assert "this is a dag" in out