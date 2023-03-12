import graphviz

import red_black_tree as rbt

def visualize_rbt(tree: rbt.RedBlackTree):
    dot = graphviz.Digraph(comment='Red-Black Tree Visualization')
    visualize_subtree(dot, tree.root)
    dot.view()
        
def visualize_subtree(dot: graphviz.Digraph, node: rbt.Node):
    if node is None:
        return
    
    dot.node(str(id(node)), 
             f"key={node.key},value={node.value}",  
             color=node.color.lower())
    
    if node.left is not None:
        dot.edge(str(id(node)), str(id(node.left)))
        visualize_subtree(dot, node.left)
        
    if node.right is not None:
        dot.edge(str(id(node)), str(id(node.right)))
        visualize_subtree(dot, node.right)

tree = rbt.RedBlackTree()
tree.add("1", "bar")
tree.add("3", "bar")
tree.add("2", "bar")
tree.add("5", "bar")

visualize_rbt(tree)