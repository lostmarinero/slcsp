import os
from path_helpers import (
    build_absolute_path,
    build_archive_file_name,
    build_new_file_name,
)


def get_base_path():
    return os.path.normpath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    )


def test_base_path_is_slcsp_directory():
    '''
    This is a test of a test helper to ensure it is doing exactly what we
    want it to.
    '''
    base_path = get_base_path()
    assert 'slcsp' in base_path
    assert os.path.basename(base_path) == 'slcsp'


class TestBuildRelativePath:
    def test_build_absolute_path(self):
        relative_path = build_absolute_path('')
        base_path = get_base_path()
        assert relative_path == base_path + '/'

    def test_build_absolute_path_with_file_name(self):
        relative_path = build_absolute_path('test.py')
        expected_path = get_base_path()
        expected_path += '/test.py'
        assert relative_path == expected_path


class TestBuildArchiveFileName:
    def test_build_archive_file_name(self):
        original = get_base_path() + '/test.py'
        archive_file_name = build_archive_file_name(original)
        base_path = get_base_path()
        assert 'original_' in archive_file_name
        assert base_path in archive_file_name

    def test_build_archive_file_name_no_path(self):
        archive_file_name = build_archive_file_name('test.py')
        base_path = get_base_path()
        assert 'original_' in archive_file_name
        assert base_path not in archive_file_name


class TestBuildNewFileName:
    def test_build_new_file_name(self):
        original = get_base_path() + '/test.py'
        new_file_name = build_new_file_name(original)
        base_path = get_base_path()
        assert 'new_' in new_file_name
        assert base_path in new_file_name

    def test_build_new_file_name_no_path(self):
        new_file_name = build_new_file_name('test.py')
        base_path = get_base_path()
        assert 'new_' in new_file_name
        assert base_path not in new_file_name
