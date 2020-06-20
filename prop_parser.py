import sys
import string
from tree import TreeNode


def main():
    evaluate = False
    if len(sys.argv) == 2:
        if sys.argv[1] == '--eval':
            evaluate = True

    for formula in sys.stdin:
        formula = formula.replace("\n", "") \
            .replace("\r", "") \
            .replace(" ", "") \
            .replace("\t", "")  # remove ws and lf
        root = TreeNode()
        symbols = ['F']
        is_valid = is_pl(formula, root, symbols)
        if evaluate:
            end=""
        else:
            end="\n"
        print(f"'{formula}': {'is well formed' if is_valid else 'is not well formed'}", end=end)
        if evaluate:
            if not is_valid:
                print(" and thus can't be evaluated.")
                continue
            if len(symbols) != 1:
                # if not, there were other symbols in
                print(", but can't be evaluated, since more symbols than 'Falsum' are used.")
                continue
            else:
                print(f" and evaluates to: {eval_f(root.left_child)}")


def eval_f(root):
    current_root = root
    if current_root.is_leaf:
        return False # we can do this, since all leaves are falsums only

    if current_root.is_operator:
        # if the current node is an operator node, it has a left and a right child
        left_val = eval_f(current_root.left_child)
        right_val = eval_f(current_root.right_child)
        ret_val = not left_val or right_val # (a->b) is equal to not a or b
        return ret_val


def is_pl(formula, root, symbols):
    current_root = root

    if formula == "":
        return False # empty formula not allowed

    if is_valid_id(formula) or is_falsum(formula):
        current_root.left_child = TreeNode(formula)
        current_root.left_child.is_leaf = True
        if formula not in symbols:
            symbols.append(formula)
        return True # this covers all formulae that consist of a single symbol

    if formula[0] != '(' or formula[len(formula) - 1] != ')':
        return False # this takes care of missing braces around longer statements


    for i in range(0, len(formula)):
        # if '(' was read, create new child of current root node.
        if formula[i] == '(':
            if current_root.left_child is None:
                current_root.is_operator = True
                current_root.left_child = TreeNode()
                temp = current_root
                current_root = current_root.left_child
                current_root.parent = temp
            elif current_root.right_child is None:
                current_root.is_operator = True
                current_root.right_child = TreeNode()
                temp = current_root
                current_root = current_root.right_child
                current_root.parent = temp
            else:
                # we found ( too much
                return False

        elif formula[i] == ')':
            # when ')' is read go to the next higher level in tree
            if current_root == root:
                return False
            if current_root.left_child is None or current_root.right_child is None:
                # something is wrong
                return False
            if not current_root.left_child.has_ancestor_leaf or not current_root.right_child.has_ancestor_leaf:
                # if we are here, one of the child nodes has no path to a leaf. That is bad
                return False

            if current_root.has_ancestor_leaf:
                current_root.parent.has_ancestor_leaf = True
            current_root = current_root.parent

        elif is_valid_id(formula[i]) or is_falsum(formula[i]):
            if formula[i] not in symbols:
                symbols.append(formula[i])

            if current_root.is_leaf:
                return False  # This means that there are more than 1 letter/symbol
            # add a new left or right child and assign the symbol
            if current_root.left_child is None:
                current_root.left_child = TreeNode(formula[i])
                current_root.left_child.is_leaf = True
                current_root.left_child.has_ancestor_leaf = True
            elif current_root.right_child is None:
                current_root.right_child = TreeNode(formula[i])
                current_root.right_child.is_leaf = True
                current_root.right_child.has_ancestor_leaf = True
            else:
                return False
            current_root.is_operator = True
            current_root.has_ancestor_leaf = True

        elif formula[i] == '>':
            # we found an implication
            if current_root.is_leaf:
                # something is wrong.
                return False
            if current_root.left_child is None:
                # read an operator without left side
                return False
            if not current_root.left_child.has_ancestor_leaf and not current_root.left_child.is_leaf:
                # left side is not valid for reading implication
                return False
            i += 1
            continue
        else:
            return False

    if current_root == root:
        return True
    # if we were able to build the tree and the last closing brace brought us back to root,
    # the formula is valid
    # else, it is not.
    return False

def is_valid_id(char):
    if char in list(string.ascii_lowercase):
        return True
    return False


def is_falsum(char):
    if char == 'F':
        return True
    return False


if __name__ == '__main__':
    main()