import string
import random


class StrUtil:
    """Utility methods to work with strings."""

    @staticmethod
    def generate_text(length=31):
        """Generate some random string.
                
        Args:
            length: length of a password.
        Returns:
            (str).
        """

        more_vowels = 'aeiouy'
        random_source = string.ascii_lowercase + more_vowels
        return ''.join([random.choice(random_source) for _ in range(length)])


    @staticmethod
    def split_string(string, delimeter='\n'):
        return string.split(delimeter)


    @staticmethod
    def parse_comment_string(comment):
        """Drop non essential comment's data.
        
        Note:
            comment_list: [name, message, date, respond, share,
                           post_id, comment_id].         
            drop: [date, respond, share]. 
        
        Returns: 
            (list): [name, message, post_id, comment_id]
        """
        
        comment_list = StrUtil.split_string(comment)
        return comment_list[:2] + comment_list[5:]


    @staticmethod
    def parse_likes_string(likes):
        if not likes:
            return 0
        else:
            return int(likes)
