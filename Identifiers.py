import re

class Identifier:
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    def is_identifier(word):
        return bool(Identifier.identifier_pattern.match(word))