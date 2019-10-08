def tree_to_string(tree, depth=0):
    DEFAULT_COLOR = '\033[39m'
    ATTR_COLOR = '\033[35m'
    NOMINAL_COLOR = '\033[34m'
    NUMERIC_COLOR = '\033[31m'
    CLASS_COLOR = '\033[36m'

    spacing = "    " * depth

    if tree.target_class:
        string = CLASS_COLOR + str(tree.target_class) + DEFAULT_COLOR
        return string

    if depth == 0:
        string = ATTR_COLOR + str(tree.attribute) + DEFAULT_COLOR + f'({tree.gain:0.3f}):\n'
    else:
        string = ATTR_COLOR + "\n" + spacing + str(tree.attribute) + DEFAULT_COLOR + f'({tree.gain:0.3f}):\n'

    if tree.kind == "nominal":
        for option in tree.options.items():
            attr_name = NOMINAL_COLOR + str(option[0]) + DEFAULT_COLOR + ": "
            string = string + spacing + attr_name + tree_to_string(option[1], depth + 1) + "\n"
    else:
        for option in tree.options.items():
            signal = " > " if option[0] else " < "
            attr_name = NUMERIC_COLOR + str(tree.cut) + DEFAULT_COLOR + signal \
                + NOMINAL_COLOR + tree.attribute + DEFAULT_COLOR + ": "
            string = string + spacing + attr_name + tree_to_string(option[1], depth + 1) + "\n"

    string = string[:-1]

    return string
