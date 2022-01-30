import csv
import pprint


class CovidDataPurifier():

    _source_data = None
    _purified_data = None

    _regionBMap = None
    _regionAMap = {
        "02": "Dolnośląskie",
        "04": "Kujawsko-pomorskie",
        "06": "Lubelskie",
        "08": "Lubuskie",
        "10": "Łódzkie",
        "12": "Małopolskie",
        "14": "Mazowieckie",
        "16": "Opolskie",
        "18": "Podkarpackie",
        "20": "Podlaskie",
        "22": "Pomorskie",
        "24": "Śląskie",
        "26": "Świętokrzyskie",
        "28": "Warmińsko-mazurskie",
        "30": "Wielkopolskie",
        "32": "Zachodniopomorskie"
    }

    def load_source_data(self, filepath):
        with_headers = 1

        if (filepath is None):
            return False

        data = []

        with open(filepath) as csv_file:
            csv_reader = csv.reader(
                csv_file, delimiter=";", dialect="excel")
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    # header row
                    if (with_headers):
                        data.append(row)
                    line_count += 1
                else:
                    # data rows
                    data.append(row)
                    line_count += 1
        self._source_data = data
        return self._source_data

    def print_output_csv(self, separator=","):
        final_arr = []
        final_str = ""

        for row in self._purified_data:
            row_string = separator.join(str(x) for x in row)
            final_arr.append(row_string)

        final_str += "\n".join(final_arr)

        print(final_str)
        return final_str

    def _purify_date(self, param):
        return param

    def _purify_regA(self, param):

        output = ""

        if param in self._regionAMap.keys():
            output = self._regionAMap[param]

        return output

    def _purify_regB(self, param):
        if(self._regionBMap is None):
            # if regions map not loaded, load it now!

            filepath = 'samples/wszystkie-powiaty.csv'
            d = {}

            with open(filepath) as csv_file:
                csv_reader = csv.reader(
                    csv_file, delimiter=";", dialect="excel")
                line_count = 0

                for row in csv_reader:
                    if line_count == 0:
                        line_count = line_count+1
                        continue
                    else:
                        d[row[0] + row[1]] = row[4] + " (" + self._regionAMap[row[0]] + ") - " + row[0] + row[1]
                        line_count += 1
            self._regionBMap = d

        if param in self._regionBMap.keys():
            return self._regionBMap[param]

        return "n/a"

    def _purify_sex(self, param):
        sex_map = {
            "K": "F",
            "M": "M",
            "nieznana": "n/a",
        }

        output = ""

        if param in sex_map.keys():
            output = sex_map[param]

        return output

    def _purify_age(self, param):
        if(len(param) > 0):
            return param
        else:
            return "n/a"

    def _purify_ageCat(self, param):
        if(len(param) > 0 and param != "BD"):
            return param
        else:
            return "n/a"

    def _purify_producer(self, param):

        producer_map = {
            "Astra Zeneca": "AstraZeneca",
            "Johnson&Johnson": "Johnson&Johnson",
            "Moderna": "Moderna",
            "Pfizer": "Pfizer",
            "brak danych": "n/a"
        }

        output = ""

        if param in producer_map.keys():
            output = producer_map[param]

        return output

    def _purify_doses(self, param):
        doses_map = {
            "jedna_dawka": "HALF",
            "pelna_dawka": "FULL",
            "przypominajaca": "BOOST",
            "uzupe�niaj�ca": "BOOST"
        }

        output = ""

        if param in doses_map.keys():
            output = doses_map[param]

        return output

    def _purify_low_immune(self, param):
        return param

    def _purify_reporting(self, param):
        return param
