class Operators:
    arithmetic_ops_class_name = "Operator / Arithmetic"
    relational_ops_class_name = "Operator / Relational"
    assignment_ops_class_name = "Operator / Assignment"
    inc_dec_ops_class_name = "Operator / IncDec"
    logical_class_name = "Operator / Logical"

    arithmetic_ops = ["+", "-", "/", "*", "%"]
    relational_ops = ["==", "!=", ">", "<", "<=", ">="]
    assignment_ops = ["="]
    inc_dec_ops = ["++", "--"]
    logical_ops = ["||", "&&"]

    def is_operator(_operator):
        return (Operators.is_arithmetic_operator(_operator) or
                Operators.is_assignment_operator(_operator) or
                Operators.is_inc_dec_operator(_operator) or
                Operators.is_relational_operator(_operator) or
                Operators.is_logical_ops(_operator))

    def is_arithmetic_operator(_operator):
        return _operator in Operators.arithmetic_ops

    def is_relational_operator(_operator):
        return _operator in Operators.relational_ops

    def is_logical_ops(_operator):
        return _operator in Operators.logical_ops

    def is_pm(_operator):
        return _operator == "+" or _operator == "-"

    def is_mdm(_operator):
        return _operator in ["*", "/", "%"]

    def is_assignment_operator(_operator):
        return _operator in Operators.assignment_ops

    def is_inc_dec_operator(_operator):
        return _operator in Operators.inc_dec_ops

    def is_multi_character_op(_operator):
        return Operators.is_inc_dec_operator(_operator) or Operators.is_relational_operator(_operator)

    def get_operator_class_name(_operator):
        if Operators.is_operator(_operator):
            if Operators.is_arithmetic_operator(_operator):
                return Operators.arithmetic_ops_class_name
            elif Operators.is_assignment_operator(_operator):
                return Operators.assignment_ops_class_name
            elif Operators.is_inc_dec_operator(_operator):
                return Operators.inc_dec_ops_class_name
            elif Operators.is_relational_operator(_operator):
                return Operators.relational_ops_class_name
            elif Operators.is_logical_ops(_operator):
                return Operators.logical_class_name
        return None