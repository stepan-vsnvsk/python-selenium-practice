class ListUtil:
    """Methods to work with list data."""

    @staticmethod
    def check_order(list, reverse=False):
        """
        Check whether data in list is sorted.
        
        Args:
            list -- list to check
            reverse -- False -> check for ascending order
                       True  -> descending
        Returns:
            (bool): True if sorted, False otherwise.
        """
        
        return list == sorted(list, reverse=reverse)
