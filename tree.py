class TreeNode:
    def __init__(self, sub=None):
        self.formula = sub
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.has_ancestor_leaf = False
        self.is_operator = False
        self.is_leaf = False
