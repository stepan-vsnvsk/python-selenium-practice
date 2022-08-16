from framework.ui.base.elements.base_element import BaseElement
from framework.utils.logger import Logger


class TextField(BaseElement):
    """
    Methods to work with Textfield element
    """

    def send_keys(self):
        """Find element and 'send keys' to it.

        Note: Based an assumption that a 'message' was saved
              as a 'send_word' property (attribute)
        """

        Logger.info(f"Send {self.send_word} to {self.name}")
        self.find_element().send_keys(self.send_word)

    def clear(self):
        """Find element and resets it's content."""
        Logger.info(f"Clear {self.name}")
        self.find_element().clear()
