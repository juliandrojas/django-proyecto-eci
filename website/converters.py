# converters.py
import re

class FileNameConverter:
    regex = r'[^/]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
