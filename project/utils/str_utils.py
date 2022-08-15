class UnionReportingStrUtils:
    """Functions to work with str data."""   

    @staticmethod
    def parse_portal_version_from_footer(version_str):   
        """ 'Version: 0' -> '0' """     
        return version_str.split()[-1]      
