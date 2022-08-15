import string
import random


class StrUtils:
    """Utility methods to work with strings."""

    @staticmethod
    def generate_text():
        """Generate some random string.
                
        Args:
            length: length of a password.
        Returns:
            (str).
        """
        length = random.randint(13, 31)
        more_vowels = 'aeiouy'
        random_source = string.ascii_lowercase + more_vowels + ' '
        return ''.join([random.choice(random_source) for _ in range(length)])

    @staticmethod
    def read_text(filepath, encoding='utf-8', errors=None):
        """Open the file in text mode, read it, and close the file."""
        with open(filepath, mode='r', encoding=encoding, errors=errors) as f:
            return f.read()
