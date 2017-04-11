import pytest
from helpers import (
    all_equal,
    state_rate_area_lookup_by_zipcode,
    combine_state_name_with_rate_area
)


class TestAllEqual:
    def test_returns_true_if_empty_list(self):
        assert all_equal([]) is True

    def test_returns_false_with_different_element_types(self):
        assert all_equal([1, '1']) is False

    def test_returns_true_with_all_same(self):
        assert all_equal([1, 1, 1]) is True

    def test_returns_false_with_different_values(self):
        assert all_equal([0, 0, 0, 0, 0, 1]) is False

    def test_returns_false_with_none(self):
        with pytest.raises(AttributeError):
            all_equal(None)


class TestCombineStateNameWithRateArea:
    def test_returns_none_if_dict_has_no_keys(self):
        assert combine_state_name_with_rate_area({'state': 'MO'}) is None

    def test_returns_a_combined_string(self):
        data_dict = {'state': 'MO', 'rate_area': '1'}
        assert combine_state_name_with_rate_area(data_dict) == 'MO 1'


class TestRateAreaLookupByZipcode:
    def test_returns_none_for_many_rate_areas_for_one_zip(self):
        zip_lookup_dict = {
            '94102': ['CA 7', 'CA 7', 'CA 9']
        }
        assert state_rate_area_lookup_by_zipcode(
            '94102',
            zip_lookup_dict
        ) is None

    def test_returns_rate_area_for_all_same(self):
        zip_lookup_dict = {
            '94102': ['CA 7', 'CA 7', 'CA 7']
        }
        assert state_rate_area_lookup_by_zipcode(
            '94102',
            zip_lookup_dict
        ) == 'CA 7'

    def test_returns_none_for_no_zip(self):
        zip_lookup_dict = {
            '94102': ['CA 7', 'CA 7', 'CA 9']
        }
        assert state_rate_area_lookup_by_zipcode(
            '94104',
            zip_lookup_dict
        ) is None

    def test_returns_none_if_none_present(self):
        zip_lookup_dict = {
            '94102': ['CA 7', 'CA 7', None]
        }
        assert state_rate_area_lookup_by_zipcode(
            '94102',
            zip_lookup_dict
        ) is None

    def test_returns_none_if_all_none(self):
        zip_lookup_dict = {
            '94102': [None, None]
        }
        assert state_rate_area_lookup_by_zipcode(
            '94102',
            zip_lookup_dict
        ) is None

    def test_returns_none_if_empty_list(self):
        zip_lookup_dict = {
            '94102': []
        }
        assert state_rate_area_lookup_by_zipcode(
            '94102',
            zip_lookup_dict
        ) is None
