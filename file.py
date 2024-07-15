from datetime import datetime
import json


class File:
    def __init__(self):
        current_datetime = datetime.now()
        file_name = (str(current_datetime.day) + '-' +
                     str(current_datetime.month) + '-' +
                     str(current_datetime.year) + '-' +
                     str(current_datetime.hour) + ':' +
                     str(current_datetime.minute) + '-scan.txt')
        self.scan_report = open(file_name, 'w+')

    def write(self, string):
        self.scan_report.write(string)
        self.scan_report.write('\n')

    def write_list(self, list):
        self.scan_report.write('\n'.join(list))

    def write_dict(self, dict):
        json.dump(dict, self.scan_report)

    def close(self):
        self.scan_report.close()
