from tree_sitter import TreeCursor


def traverse(cursor: TreeCursor, handle_node):
    depth = 0
    while True:
        if cursor.goto_first_child():
            depth += 1
            handle_node(cursor, cursor.node, cursor.node.text.decode(), True, depth)
        elif cursor.goto_next_sibling():
            handle_node(cursor, cursor.node, cursor.node.text.decode(), True, depth)
        elif cursor.goto_parent():
            depth -= 1
            handle_node(cursor, cursor.node, cursor.node.text.decode(), False, depth)
            while not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    return
                depth -=1
                handle_node(cursor, cursor.node, cursor.node.text.decode(), False, depth)

            handle_node(cursor, cursor.node, cursor.node.text.decode(), True, depth)
        else:
            return
