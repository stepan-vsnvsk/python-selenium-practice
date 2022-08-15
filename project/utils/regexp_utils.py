import re 
from framework.utils.json_utils import JsonUtils


class UnionReportingRegexpUtils:
    _regexp = None

    @staticmethod
    def setup(regexp_dict):
        UnionReportingRegexpUtils._regexp = regexp_dict

    @staticmethod
    def parse_tests_data_from_projects_page(raw_tests_data):
        """
        Parse raw data about tests from web UI table to list of strings.

        Args:
             raw_tests_data(str): data about tests from a project's page.

        Note:
            Regex pattern looks for a string that starts with a test name
             (KS-1231 [...]) and ends with mlsecond timestamp .000 .

        Returns:
                (list) of str's: each string contains one test's data.
        """

        #! move to file
        #test_name_starts = r"[A-Z]{2}-\d{4}.*"
        #timestamp_ends = r".\d{3}"
        #pattern_for_split_tests = r'[A-Z]{2}-\d{4}.*.\d{3}'

        test_name_starts = UnionReportingRegexpUtils._regexp['test_name_starts']
        timestamp_ends = UnionReportingRegexpUtils._regexp['timestamp_ends']
        pattern_for_splitting_tests = fr"{test_name_starts}{timestamp_ends}"
        return re.findall(pattern_for_splitting_tests, raw_tests_data) 

    @staticmethod
    def parse_tests_data_by_attributes(list_of_tests):
        """
        Transform unstructured test's data (str) to list of dict's.

        Note:
             initial list will be changed.
        
        Args:
             list_of_tests(str): data about tests.

        Returns:
                (list) of dict's: each dictionary contains test's data
                                  with attribute-value pairs.
        """
        
        #! move to file 
        # test_name_group = r"([A-Z]{2}-.*)"
        # method_group = r"(com\..*)"
        # status_group = r"([A-Z][a-z]*)"
        # time_group = r"(\d{4}-.*?\.\d{1})"        
        # duration_group = r"(.*\.\d{3})"
        # space = r"\s"
        test_name_group = UnionReportingRegexpUtils._regexp['test_name_group']
        method_group = UnionReportingRegexpUtils._regexp['method_group']
        status_group = UnionReportingRegexpUtils._regexp['status_group']
        status_in_progress_group = UnionReportingRegexpUtils._regexp['status_in_progress_group']
        time_group = UnionReportingRegexpUtils._regexp['time_group']
        duration_group = UnionReportingRegexpUtils._regexp['duration_group']
        space = UnionReportingRegexpUtils._regexp['space']


        #pattern_for_split_attr  = (test_name_group + space + method_group + space + status_group + space \
        #                          + time_group + space + time_group + space + duration_group)
        pattern_for_splitting_by_attr = (fr"{test_name_group}{space}{method_group}{space}{status_group}{space}{time_group}{space}{time_group}{space}{duration_group}")

        #pattern_if_test_in_progress = (test_name_group + space + method_group + space + status_group + space \
        #+ time_group + space + duration_group)

        pattern_for_tests_in_progress = (fr"{test_name_group}{space}{method_group}{space}{status_in_progress_group}{space}{time_group}{space}{duration_group}")

        # pattern_for_split_attr = (r"([A-Z]{2}-.*)\s(com\..*)\s([A-Z][a-z]*)\s(\d{4}-.*?\.\d{1})\s(\d{4}-.*?\.\d{1})\s(.*\.\d{3})")
        # pattern_for_tests_in_progress = (r"([A-Z]{2}-.*)\s(com\..*)\s([A-Z][a-z]\s[a-z]*)\s(\d{4}-.*?\.\d{1})\s(.*\.\d{3})")
        
        for enum, test_string_to_parse in enumerate(list_of_tests):            
            match = re.search(pattern_for_splitting_by_attr, test_string_to_parse)
            if match:
                list_of_tests[enum] = dict(
                                                name=match.group(1),
                                                method=match.group(2),
                                                status=match.group(3).upper(),
                                                start_time=match.group(4),
                                                end_time=match.group(5),
                                                duration=match.group(6)
                                            )
            else: # 'In progress' tests             
                in_progress_match = re.search(pattern_for_tests_in_progress, test_string_to_parse)
                list_of_tests[enum] = dict(
                                                name=in_progress_match.group(1),
                                                method=in_progress_match.group(2),
                                                status=in_progress_match.group(3),
                                                start_time=in_progress_match.group(4),                                                
                                                duration=in_progress_match.group(5)
                                            )
        return list_of_tests
        