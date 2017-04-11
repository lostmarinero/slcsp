from helpers import isfloat


def pull_unique_rate_silver_plans(plan_list):
    '''
    This function pulls all plans with a meta level of 'Silver' from a list of
    plans and removes any silver plans with the same 'rate'
    '''
    seen = set()
    return [x for x in plan_list
            if (
                x['metal_level'] == 'Silver' and
                x['rate'] not in seen and
                not seen.add(x['rate'])
            )]


def pull_second_lowest_plan(list_of_values):
    '''
    This function takes a list of dicts. It sorts the list by the rate
    attribute and then returns the object with the second lowest
    value, or None if there is less than 2 values
    '''
    if list_of_values == []:
        return None
    list_of_values = [x for x in list_of_values
                      if ('rate' in x and
                          isinstance(x['rate'], str) and
                          isfloat(x['rate']))
                      ]
    sorted_list = sorted(list_of_values,
                         key=lambda x: float(x['rate']),
                         reverse=True)
    return sorted_list[-2] if len(sorted_list) >= 2 else None


def pull_second_lowest_rate(all_plans):
    '''
    This function pulls the second lowest rate based on the 'rate' attribute.

    test if given empty, multiple rates that it is second lowest (and not second highest), etc
    '''
    second_lowest_plan = pull_second_lowest_plan(all_plans)
    return None if second_lowest_plan is None else second_lowest_plan['rate']


def pull_benchmark_plan(plan_list):
    '''
    This function pulls the silver plans from a list, and then from that list
    returns the second lowest rate (or None if there is less than 1
    silver plan). It will return None if no rate is found.
    '''
    all_silver_plans = pull_unique_rate_silver_plans(plan_list)
    return pull_second_lowest_plan(all_silver_plans)


def pull_benchmark_rate(plan_list):
    '''
    This function finds the plan with the second lowest rate and then
    returns the rate.
    '''
    if plan_list == []:
        return None
    benchmark_plan = pull_benchmark_plan(plan_list)
    return None if benchmark_plan is None else benchmark_plan['rate']
