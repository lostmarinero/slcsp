import os
from datetime import datetime


def build_absolute_path(path_name):
    root_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root_path, path_name)


def file_rename_with_path(func):
    def function_wrapper(old_file_path):
        just_file_name = os.path.basename(old_file_path)
        old_file_name, old_file_extension = os.path.splitext(just_file_name)
        old_file_directory = os.path.dirname(old_file_path)
        new_file_name = func(old_file_name)
        new_file_path = os.path.join(old_file_directory,
                                     new_file_name + old_file_extension)
        return new_file_path
    return function_wrapper


@file_rename_with_path
def build_archive_file_name(old_file_name):
    int_timestamp = int(datetime.now().timestamp())
    return 'original_{0}_{1}'.format(old_file_name, int_timestamp)


@file_rename_with_path
def build_new_file_name(old_file_name):
    return 'new_{0}'.format(old_file_name)
