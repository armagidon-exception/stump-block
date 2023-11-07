from clause import Clause
from traverser import TraverseContext


class VariableClause(Clause):

    def trigger(self, context: TraverseContext) -> bool:
        if not (child := context.first_child_by_type('variable_declaration')):
            return False

        pass

