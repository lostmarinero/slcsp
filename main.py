from importer import (
    add_benchmark_rate_to_slcsp,
)

if __name__ == "__main__":
    try:
        add_benchmark_rate_to_slcsp('slcsp.csv', 'zips.csv', 'plans.csv')
        print(
            'Process Complete: Please view the zipcodes and benchmark rates'
            ' in the slcsp.csv file.'
        )
    except:
        print('ImporterError: Something went wrong')
