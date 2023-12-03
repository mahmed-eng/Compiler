class KeywordType:
    def __init__(self, class_name, children):
        self.class_name = class_name
        self.children = children

    def get_class_name(self):
        return self.class_name

    def is_available(self, keyword):
        return keyword in self.children

    def __str__(self):
        children_str = ", ".join(self.children)
        return f"{{\n  Class Name: {self.class_name}\n  Children: {children_str}\n}}\n"


class Keywords:
    keywords_groups = []
    source_data = """
        str: str
        char: char
        int: int
        dbl: float
        bool: bool
        void: None
        datetime: datetime
        if: if
        else: else
        do: do
        while: while
        elif: elif
        return: return
        class: class
        new: new
        extends: @
        implements: implements
        interface: interface
        final: final
        abstract: abstract
        try: try
        catch: except
        finally: finally
        throw: raise
    """

    def initialize_keywords():
        for class_line in Keywords.source_data.split('\n'):
            tokens = class_line.strip().split(':')
            if len(tokens) > 1 and tokens[0] and tokens[1]:
                class_name = tokens[0].strip()
                children = [key.strip() for key in tokens[1].split(',')]
                Keywords.keywords_groups.append(KeywordType(class_name, children))

    def get_keywords_groups():
        return Keywords.keywords_groups

    def is_keyword(keyword):
        if not keyword:
            return False
        for instance in Keywords.keywords_groups:
            if instance.is_available(keyword):
                return True
        return False

    def get_keyword_class_name(keyword):
        if Keywords.is_keyword(keyword):
            for instance in Keywords.keywords_groups:
                if instance.is_available(keyword):
                    return f"Keyword / {instance.get_class_name()}"
        return None


# Initialize keywords
Keywords.initialize_keywords()

# Example usage:
# To get all keyword groups:
# all_keyword_groups = Keywords.get_keywords_groups()
#
# To check if a word is a keyword:
# is_keyword = Keywords.is_keyword("if")
#
# To get the class name of a keyword:
# keyword_class_name = Keywords.get_keyword_class_name("if")