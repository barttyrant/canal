import pprint
import csv

from covid_data_purifier import CovidDataPurifier


class CovidCasesDataPurifier(CovidDataPurifier):
   
    def purify_data(self):
        if (self._source_data is None):
            return False

        output_data = []

        for i, record in enumerate(self._source_data):
            if (i == 0):
                # header row
                record_output = [
                    'date',
                    'regA',
                    'regB',
                    'sex',
                    'age',
                    'age_cat',
                    'producer',
                    'doses',
                    'low_immune',
                    # 'reporting_cnt'
                ]
            else:
                # ordinary row

                record_output = [
                    self._purify_date(record[0]),
                    self._purify_regA(record[1]),
                    self._purify_regB(record[2]),
                    self._purify_sex(record[3]),
                    self._purify_age(record[4]),
                    self._purify_ageCat(record[5]),
                    self._purify_producer(record[6]),
                    self._purify_doses(record[7]),
                    self._purify_low_immune(record[8]),
                    # self._purify_reporting(record[9]),
                ]

            output_data.append(record_output)

        self._purified_data = output_data
        return self._purified_data

    
def main():

    purifier = CovidCasesDataPurifier()
    purifier.load_source_data('samples/test-data-cases.csv')
    purifier.purify_data()
    purifier.print_output_csv()


if __name__ == '__main__':
    main()
