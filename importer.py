import csv
import os

from helpers import (
    state_rate_area_lookup_by_zipcode,
    combine_state_name_with_rate_area,
)

from rate_helpers import (
    pull_benchmark_rate,
)

from path_helpers import (
    build_absolute_path,
    build_archive_file_name,
    build_new_file_name,
)


def import_csv_to_zipcode_key_dict(csv_file):
    '''
    This function imports a csv file and creates a dict with the keys being
    the zip codes mapped to all (can be multiple) state rate areas.
    Do note state rate areas are the STATE combined with the RATE AREA.
    '''
    zip_dict = {}
    relative_csv_path = build_absolute_path(csv_file)
    with open(relative_csv_path) as import_csv:
        reader = csv.DictReader(import_csv)
        for row in reader:
            zipcode = row['zipcode']
            state_rate_area = combine_state_name_with_rate_area(row)
            if zipcode in zip_dict:
                zip_dict[zipcode].append(state_rate_area)
            else:
                zip_dict[zipcode] = [state_rate_area]
    return zip_dict


def import_csv_to_state_rate_area_key_dict(csv_file):
    '''
    This function imports a csv file and creates a dict with the keys
    being the state rate area (state plus rate area number) mapped to a list
    containing all plans (plan_id, state, metal_level, rate, rate_area).
    '''
    rate_area_lookup = {}
    relative_csv_path = build_absolute_path(csv_file)
    with open(relative_csv_path) as import_csv:
        reader = csv.DictReader(import_csv)
        for row in reader:
            state_rate_area = combine_state_name_with_rate_area(row)
            if state_rate_area in rate_area_lookup:
                if row not in rate_area_lookup[state_rate_area]:
                    rate_area_lookup[state_rate_area].append(row)
            else:
                rate_area_lookup[state_rate_area] = [row]
    return rate_area_lookup


def add_benchmark_rate_to_slcsp(slcsp_file, zipcode_file, plan_file):
    '''
    This function imports the necessary csv files and extracts the data into
    dictionaries. It then loops through the target csv file, pulls the
    zipcode from it and finds the benchmark plan for each. It then saves
    the zip code and the benchmark rate to a new csv file. When it is finished
    it renames the old csv and replaces it with the new csv with the complete
    data.
    '''
    zipcode_dict = import_csv_to_zipcode_key_dict(zipcode_file)
    rate_area_dict = import_csv_to_state_rate_area_key_dict(plan_file)
    slcsp_relative_path = build_absolute_path(slcsp_file)
    new_slcsp_file_name = build_new_file_name(slcsp_relative_path)
    with open(slcsp_relative_path) as import_csv, \
            open(new_slcsp_file_name, 'w') as export_csv:
        reader = csv.DictReader(import_csv)
        writer = csv.DictWriter(export_csv, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            zipcode = row['zipcode']
            rate_area = state_rate_area_lookup_by_zipcode(
                zipcode,
                zipcode_dict
            )
            all_plans = rate_area_dict.get(rate_area, [])
            row['rate'] = pull_benchmark_rate(all_plans)
            writer.writerow(row)
    archive_name = build_archive_file_name(slcsp_relative_path)
    os.rename(slcsp_relative_path, archive_name)
    os.rename(new_slcsp_file_name, slcsp_relative_path)
