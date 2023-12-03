class Separators:
    separators = [" ", "\n", "\r", "\t"]

    def is_separator(char):
        return char in Separators.separators