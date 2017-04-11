import pytest
from rate_helpers import (
    pull_unique_rate_silver_plans,
    pull_second_lowest_plan,
    pull_second_lowest_rate,
    pull_benchmark_plan,
    pull_benchmark_rate
)


@pytest.fixture
def all_plans():
    plan_datas = [
        ('Gold', '370.8'), ('Gold', '347.04'), ('Silver', '317.83'),
        ('Silver', '310.52'), ('Silver', '282.53'), ('Silver', '261.61'),
        ('Silver', '213.54'), ('Silver', '213.54'), ('Bronze', '238.14'),
        ('Bronze', '203.69'), ('Catastrophic', '202.63')
    ]
    all_plans = []
    for index, plan_data in enumerate(plan_datas):
        all_plans.append({
            'metal_level': plan_data[0],
            'rate': plan_data[1],
            'state': 'CA',
            'rate_area': '1',
            'plan_id': (plan_data[0] + str(index))
        })
    return all_plans


class TestPullSilverPlans:
    def test_pull_unique_rate_silver_plans_pulls_only_silver(self, all_plans):
        silver_plans = pull_unique_rate_silver_plans(all_plans)
        assert all(x['metal_level'] for x in silver_plans)

    def test_removes_silver_plans_with_duplicate_rates(self, all_plans):
        silver_plans = pull_unique_rate_silver_plans(all_plans)
        assert silver_plans[-1]['rate'] == '213.54'
        assert silver_plans[-2]['rate'] != '213.54'
        assert silver_plans[-1]['rate'] != silver_plans[-2]['rate']

    def test_pull_unique_rate_silver_plans_returns_empty_list_if_none(self, all_plans):
        all_plans_minus_silver = [x for x
                                  in all_plans
                                  if x['metal_level'] != 'Silver']
        silver_plans = pull_unique_rate_silver_plans(all_plans_minus_silver)
        assert silver_plans == []


class TestPullSecondLowestPlan:
    def test_pulls_second_lowest_rate_plan(self, all_plans):
        second_lowest = pull_second_lowest_plan(all_plans)
        assert second_lowest['rate'] == '203.69'
        assert second_lowest['metal_level'] == 'Bronze'

    def test_pulls_second_lowest_rate_plan_separate_order(self, all_plans):
        new_plans = list(reversed(all_plans))
        second_lowest = pull_second_lowest_plan(new_plans)
        assert second_lowest['rate'] == '203.69'
        assert second_lowest['metal_level'] == 'Bronze'

    def test_pulls_second_lowest_rate_plan_with_two_plans(self, all_plans):
        two_plans = all_plans[:2]
        second_lowest = pull_second_lowest_plan(two_plans)
        assert second_lowest['rate'] == '370.8'

    def test_returns_none_if_only_one(self, all_plans):
        only_plan = all_plans[:1]
        second_lowest = pull_second_lowest_plan(only_plan)
        assert second_lowest is None

    def test_returns_none_if_empty_list(self, all_plans):
        second_lowest = pull_second_lowest_plan([])
        assert second_lowest is None

    def test_no_error_if_dict_missing_key(self, all_plans):
        del all_plans[0]['rate']
        second_lowest = pull_second_lowest_plan(all_plans)
        assert second_lowest['rate'] == '203.69'

    def test_no_error_if_rate_empty(self, all_plans):
        all_plans[0]['rate'] = ''
        second_lowest = pull_second_lowest_plan(all_plans)
        assert second_lowest['rate'] == '203.69'

    def test_no_error_if_rate_bad_format(self, all_plans):
        all_plans[0]['rate'] = 'error'
        second_lowest = pull_second_lowest_plan(all_plans)
        assert second_lowest['rate'] == '203.69'

    def test_no_error_if_rate_none(self, all_plans):
        all_plans[0]['rate'] = None
        second_lowest = pull_second_lowest_plan(all_plans)
        assert second_lowest['rate'] == '203.69'

    def test_if_two_lowest_are_same_price(self):
        # Could test if there are two of the same price (lowest), how does that
        # qualify?
        pass

    def test_if_second_and_thire_lowest_are_same_price(self):
        # Could test if there are two of the same price (second lowest), how
        # does that qualify?
        pass


class TestPullSecondLowestRate:
    def test_pulls_second_lowest_rate(self, all_plans):
        second_lowest = pull_second_lowest_rate(all_plans)
        assert second_lowest == '203.69'

    def test_pulls_second_lowest_rate_with_only_two_plans(self, all_plans):
        two_plans = all_plans[:2]
        second_lowest = pull_second_lowest_rate(two_plans)
        assert second_lowest == '370.8'

    def test_returns_none_if_only_one(self, all_plans):
        only_plan = all_plans[:1]
        second_lowest = pull_second_lowest_rate(only_plan)
        assert second_lowest is None

    def test_returns_none_if_empty_list(self, all_plans):
        second_lowest = pull_second_lowest_rate([])
        assert second_lowest is None


class TestPullBenchmarkPlan:
    def test_pulls_second_lowest_silver_plan(self, all_plans):
        second_lowest_silver = pull_benchmark_plan(all_plans)
        assert second_lowest_silver['rate'] == '261.61'
        assert second_lowest_silver['metal_level'] == 'Silver'

    def test_returns_none_if_no_silver(self, all_plans):
        new_plans = [x for x in all_plans if x['metal_level'] != 'Silver']
        second_lowest_silver = pull_benchmark_plan(new_plans)
        assert second_lowest_silver is None

    def test_returns_none_if_only_one_silver(self, all_plans):
        new_plans = [x for x in all_plans if x['metal_level'] != 'Silver']
        new_plans.append({'rate': '100', 'metal_level': 'Silver',
                          'plan_id': 'Silver1', 'state': 'CA',
                          'rate_area': '1'})
        second_lowest_silver = pull_benchmark_plan(new_plans)
        assert second_lowest_silver is None

    def test_returns_none_if_empty_list(self, all_plans):
        second_lowest_silver = pull_benchmark_plan([])
        assert second_lowest_silver is None


class TestPullBenchmarkRate:
    def test_pulls_second_lowest_silver_plan_rate(self, all_plans):
        second_lowest_silver = pull_benchmark_rate(all_plans)
        assert second_lowest_silver == '261.61'

    def test_returns_none_if_no_silver(self, all_plans):
        new_plans = [x for x in all_plans if x['metal_level'] != 'Silver']
        second_lowest_silver = pull_benchmark_rate(new_plans)
        assert second_lowest_silver is None

    def test_returns_none_if_only_one_silver(self, all_plans):
        new_plans = [x for x in all_plans if x['metal_level'] != 'Silver']
        new_plans.append({'rate': '100', 'metal_level': 'Silver',
                          'plan_id': 'Silver1', 'state': 'CA',
                          'rate_area': '1'})
        second_lowest_silver = pull_benchmark_rate(new_plans)
        assert second_lowest_silver is None

    def test_returns_none_if_empty_list(self, all_plans):
        second_lowest_silver = pull_benchmark_rate([])
        assert second_lowest_silver is None
