

def combine_state_name_with_rate_area(row_dict):
    if not all(x in row_dict.keys() for x in ['state', 'rate_area']):
        return None
    return row_dict['state'] + ' ' + row_dict['rate_area']


def all_equal(list_of_values):
    if list_of_values == []:
        return True
    return list_of_values.count(list_of_values[0]) == len(list_of_values)


def state_rate_area_lookup_by_zipcode(zipcode, zip_lookup_dict):
    rate_areas = zip_lookup_dict.get(zipcode, [])
    if all_equal(rate_areas) and rate_areas != []:
        return rate_areas[0]
    else:
        return None


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
