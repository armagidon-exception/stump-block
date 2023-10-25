from tree_sitter import TreeCursor


def traverse(cursor: TreeCursor, handle_node):
    while True:
        if cursor.goto_first_child():
            handle_node(cursor, cursor.node, cursor.node.text.decode(), True)
        elif cursor.goto_next_sibling():
            handle_node(cursor, cursor.node, cursor.node.text.decode(), True)
        elif cursor.goto_parent():
            handle_node(cursor, cursor.node, cursor.node.text.decode(), False)
            while not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    return
                handle_node(cursor, cursor.node, cursor.node.text.decode(), False)

            handle_node(cursor, cursor.node, cursor.node.text.decode(), True)
        else:
            return
