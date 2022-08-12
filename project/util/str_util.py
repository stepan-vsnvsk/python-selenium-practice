import re 

class StrProjectUtil:
    @staticmethod
    def parse_portal_version_from_footer(version_str):   
        """ 'Version: 0' -> '0' """     
        return version_str.split()[-1]

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
        pattern_for_split_attr = (r"([A-Z]{2}-.*)\s(com\..*)\s([A-Z][a-z]*)\s(\d{4}-.*?\.\d{1})\s(\d{4}-.*?\.\d{1})\s(.*\.\d{3})")
        pattern_for_tests_in_progress = (r"([A-Z]{2}-.*)\s(com\..*)\s([A-Z][a-z]\s[a-z]*)\s(\d{4}-.*?\.\d{1})\s(.*\.\d{3})")
        
        for enum, test_string_to_parse in enumerate(list_of_tests):            
            match = re.search(pattern_for_split_attr, test_string_to_parse)
            if match:
                list_of_tests[enum] = dict(
                                                name=match.group(1),
                                                method=match.group(2),
                                                status=match.group(3).upper(),
                                                start_time=match.group(4),
                                                end_time=match.group(5),
                                                duration=match.group(6)
                                                )
            else:                
                in_progress_match = re.search(pattern_for_tests_in_progress, test_string_to_parse)
                list_of_tests[enum] = dict(
                                                name=in_progress_match.group(1),
                                                method=in_progress_match.group(2),
                                                status=in_progress_match.group(3).upper(),
                                                start_time=in_progress_match.group(4),                                                
                                                duration=in_progress_match.group(5)
                                                )
        return list_of_tests


    @staticmethod
    def parse_tests_data_from_projects_page(raw_tests_data):
        """
        Parse raw data about tests from web UI table to list of strings.

        Args:
             raw_tests_data(str): data about tests from a project's page.

        Returns:
                (list) of str's: each string contains one test's data.
        """

        #! move to file
        pattern_for_split_tests = r'[A-Z]{2}-\d{4}.*.\d{3}'
        return re.findall(pattern_for_split_tests, raw_tests_data)        


