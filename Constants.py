import re

class Constants:
    def is_constant(word):
        return (StringConstants.is_string_constant(word) or CharConstant.is_char_constant(word)
                or DoubleConstant.is_double_constant(word) or IntConstant.is_int_constant(word) or BooleanConstant.is_boolean_constant(word))

    def get_constant_class_name(word):
        if StringConstants.is_string_constant(word):
            return "Constant / String"
        elif CharConstant.is_char_constant(word):
            return "Constant / Character"
        elif IntConstant.is_int_constant(word):
            return "Constant / Integer"
        elif DoubleConstant.is_double_constant(word):
            return "Constant / Double"
        elif BooleanConstant.is_boolean_constant(word):
            return "Constant / Bool"
        else:
            return None


class StringConstants:
    def is_string_constant(word):
        word = word.strip()
        return len(word) >= 2 and word[0] == '"' and word[-1] == '"' and word[-2] != '\\'


class BooleanConstant:
    def is_boolean_constant(word):
        return word.lower() in {"true", "false"}


class CharConstant:
    def is_char_constant(word):
        word = word.strip()
        if len(word) == 3 and word[0] == "'" and word[2] == "'" and word[1] != "'" and word[1] != '\\':
            return True
        if len(word) == 4 and word[0] == "'" and word[3] == "'" and word[1] == '\\':
            return True
        return False


class IntConstant:
    re_pattern = re.compile(r'^[+-]?\d+$')

    def is_int_constant(word):
        return bool(IntConstant.re_pattern.match(word))


class DoubleConstant:
    re_pattern = re.compile(r'^[+-]?(\d+|(\d*\.\d+))$')

    def is_double_constant(word):
        return bool(DoubleConstant.re_pattern.match(word))