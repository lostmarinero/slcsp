import pytest
import csv
import os

from importer import (
    import_csv_to_zipcode_key_dict,
    import_csv_to_state_rate_area_key_dict,
    add_benchmark_rate_to_slcsp,
)


def create_test_file_name(file_name):
    __location__ = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(__location__, 'test_files', file_name)


@pytest.fixture
def zipcode_dict():
    return import_csv_to_zipcode_key_dict(
        create_test_file_name('test_zips.csv')
    )


@pytest.fixture
def state_rate_dict():
    return import_csv_to_state_rate_area_key_dict(
        create_test_file_name('test_plans.csv')
    )


class TestImportCSVToZipcodeKeyDict:
    def test_multiple_same_state_rate_areas(self, zipcode_dict):
        assert zipcode_dict['35115'] == ['AL 3', 'AL 3', 'AL 3']

    def test_multiple_diff_state_rate_areas(self, zipcode_dict):
        assert zipcode_dict['36006'] == ['AL 11', 'AL 3']

    def test_multiple_state_rate_areas_diff_states(self, zipcode_dict):
        assert zipcode_dict['30165'] == ['AL 13', 'GA 13', 'GA 13']

    def test_two_state_rate_areas(self, zipcode_dict):
        assert zipcode_dict['36758'] == ['AL 11', 'AL 11']

    def test_one_state_rate_areas2(self, zipcode_dict):
        assert zipcode_dict['36574'] == ['AL 13']

    def test_one_state_rate_areas3(self, zipcode_dict):
        assert zipcode_dict['03103'] == ['NH 1']


class TestImportCSVToStateRateAreaKeyDict:
    def test_multiple_plans_same_state_rate_area(self, state_rate_dict):
        assert len(state_rate_dict['GA 13']) == 3

    def test_many_plans_same_state_rate_area(self, state_rate_dict):
        assert len(state_rate_dict['AL 3']) == 10

    def test_one_plan_same_state_rate_area(self, state_rate_dict):
        assert len(state_rate_dict['AL 9']) == 1

    def test_remove_duplicates(self, state_rate_dict):
        assert len(state_rate_dict['AL 11']) == 5


@pytest.yield_fixture
def test_slcsp():
    with open(create_test_file_name('test_slcsp.csv')) as f:
        yield csv.DictReader(f)


class TestImportCSVFilesToDicts:
    @classmethod
    def setup_class(cls):
        """
        Run the method to build the new slcsp file
        """
        add_benchmark_rate_to_slcsp('test/test_files/test_slcsp.csv',
                                    'test/test_files/test_zips.csv',
                                    'test/test_files/test_plans.csv')

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        for file_name in os.listdir(create_test_file_name('')):
            if 'original_test_slcsp' in file_name:
                os.rename(create_test_file_name(file_name),
                          create_test_file_name('test_slcsp.csv'))

    def pull_all_rows_by_zip(self, zipcode, dictreader):
        return [row for row in dictreader if row['zipcode'] == zipcode]

    def pull_first_row_by_zip(self, zipcode, dictreader):
        return self.pull_all_rows_by_zip(zipcode, dictreader)[0]

    def test_expected_csv_vs_actual_csv(self):
        actual_file_name = create_test_file_name('test_slcsp.csv')
        expected_file_name = create_test_file_name('expected_test_slcsp.csv')
        with open(actual_file_name) as actual, \
                open(expected_file_name) as expected:
                    actual1 = list(csv.DictReader(actual))
                    expected1 = list(csv.DictReader(expected))
                    assert actual1 == expected1

    def test_zipcode_multiple_diff_rate_areas_returns_empty(self, test_slcsp):
        '''
        Zip code 36006 has two rate areas, AL 11 and AL 3
        and therefore has no benchmark rate
        '''
        row = self.pull_first_row_by_zip('36006', test_slcsp)
        assert row['zipcode'] == '36006'
        assert row['rate'] == ''

    def test_zipcode_multiple_diff_state_rate_areas_return_none(self, test_slcsp):
        '''
        Zip code 30165 has two rate areas, AL 13 and GA 13
        and therefore has no benchmark rate
        '''
        row = self.pull_first_row_by_zip('30165', test_slcsp)
        assert row['zipcode'] == '30165'
        assert row['rate'] == ''

    def test_zipcode_3_valid_silver_plans(self, test_slcsp):
        '''
        Zip code 35115 has multiple state rate areas but all equal AL 3
        AL 3 has 3 plans with 'metal_level' == 'Silver'
        The benchmark rate is 271.98
        '''
        row = self.pull_first_row_by_zip('35115', test_slcsp)
        assert row['zipcode'] == '35115'
        assert row['rate'] == '271.98'

    def test_zipcode_2_valid_silver_plans(self, test_slcsp):
        '''
        Zip code 36758 has one state rate area, AL 11
        AL 11 has 2 plans with 'metal_level' == 'Silver'
        The benchmark rate is 268.26
        '''
        row = self.pull_first_row_by_zip('36758', test_slcsp)
        assert row['zipcode'] == '36758'
        assert row['rate'] == '268.26'

    def test_zipcode_1_valid_silver_plans(self, test_slcsp):
        '''
        Zip code 36574 has one state rate area, AL 13
        AL 13 has 1 plan with 'metal_level' == 'Silver'
        The benchmark rate is therefore ''
        '''
        row = self.pull_first_row_by_zip('36574', test_slcsp)
        assert row['zipcode'] == '36574'
        assert row['rate'] == ''

    def test_zipcode_0_valid_silver_plans(self, test_slcsp):
        '''
        Zip code 03103 has one state rate area, NH 1
        NH 1 has 0 plans with 'metal_level' == 'Silver'
        The benchmark rate is therefore ''
        '''
        row = self.pull_first_row_by_zip('03103', test_slcsp)
        assert row['zipcode'] == '03103'
        assert row['rate'] == ''

    def test_zipcode_multiple_silver_plans_with_same_rate(self, test_slcsp):
        '''
        Zip code 04003 has one state rate area, ME 1
        ME 1 has 3 plans with 'metal_level' == 'Silver' but the lowest has
        the same rate as the second lowest.
        This tests that each Silver Rate plan has an unique rate.
        The benchmark rate is therefore ''
        '''
        row = self.pull_first_row_by_zip('04003', test_slcsp)
        assert row['zipcode'] == '04003'
        assert row['rate'] == '305.27'


class TestSystemFileRenames:
    def test_original_file_kept(self):
        '''
        This is to test that the original import slcsp.csv file is saved with a
        separate name so that in the case of a failure we can move back and
        restart (the import method is destructive to the original file
        in nature). We use a separate test file to not create problems with the
        other tests.
        '''
        add_benchmark_rate_to_slcsp('test/test_files/starting_test_slcsp.csv',
                                    'test/test_files/test_zips.csv',
                                    'test/test_files/test_plans.csv')

        file_name = [x for x in os.listdir(create_test_file_name(''))
                     if 'original_starting_test_slcsp' in x][0]
        duplicate_file_name = create_test_file_name(
            'duplicate_of_starting_test_slcsp.csv'
        )
        original_file_name = create_test_file_name(file_name)

        with open(duplicate_file_name) as duplicate, \
                open(original_file_name) as original:
                    duplicate1 = list(csv.DictReader(duplicate))
                    original1 = list(csv.DictReader(original))
                    assert duplicate1 == original1

        for file_name in os.listdir(create_test_file_name('')):
            if 'original_starting_test_slcsp' in file_name:
                dup_file_name = create_test_file_name(file_name)
                orig_file_name = create_test_file_name(
                    'starting_test_slcsp.csv'
                )
                os.rename(dup_file_name,
                          orig_file_name)
