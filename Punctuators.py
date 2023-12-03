class Punctuators:
    punctuators = [",", ";", ":", ".", "{", "}", "[", "]", "(", ")"]

    def is_punctuator(char):
        return char in Punctuators.punctuators

    def get_punctuator_class_name(punctuator):
        if not Punctuators.is_punctuator(punctuator):
            return None

        punctuator_mappings = {
            ",": "Punctuator / Comma",
            ";": "Punctuator / Semicolon",
            ":": "Punctuator / Colon",
            ".": "Punctuator / Dot",
            "{": "Punctuator / OCB",
            "}": "Punctuator / CCB",
            "(": "Punctuator / OB",
            ")": "Punctuator / CB",
            "[": "Punctuator / OSB",
            "]": "Punctuator / CSB"
        }

        return punctuator_mappings.get(punctuator, None)