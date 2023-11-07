from clause import Clause
from state import State, StateType
from traverser import TraverseContext


class MetaCommentStateClause(Clause):
    def __init__(self, id: str, state: StateType) -> None:
        super().__init__()
        self.id = id
        self.state = state

    @property
    def start_tag(self):
        return f"{self.id}-start"

    @property
    def end_tag(self):
        return f"{self.id}-end"

    def _prep_comment(self, input: str):
        return input.removeprefix("//").strip()

    def trigger(self, context: TraverseContext) -> bool:
        assert context.last_state
        if not context.current_node == "comment" or not context.enter:
            return False
        input_string = self._prep_comment(context.text)
        if (
            context.last_state.type == StateType.LINEAR
            and input_string == self.start_tag
        ):
            return True
        elif context.last_state.type == self.state and input_string == self.end_tag:
            return True
        return False

    def handle(self, context: TraverseContext):
        input_string = self._prep_comment(context.text)
        if not context.last_state:
            return
        if (
            context.last_state.type == StateType.LINEAR
            and input_string == self.start_tag
        ):
            context.state_stack.append(State(self.state, context.last_state.commands))
        elif context.last_state.type == self.state and input_string == self.end_tag:
            context.state_stack.pop()
