from tree_sitter import Node
from handlers import StateHandler
from handlers.linear import LinearStateHandler
from traverser_state import State, StateHolder


class ConditionalStateHandler(StateHandler):
    _linear_state_hander = LinearStateHandler()

    def _handle(
        self,
        current: Node,
        name: str | None,
        text: str,
        state_stack: list[StateHolder],
        enter: bool,
    ):
        if not current.parent:
            return
        current_state = state_stack[-1].type
        conseq = current.parent.child_by_field_name("consequence")
        alter = current.parent.child_by_field_name("alternative")
        if current_state == State.CONDITION:
            if enter and conseq and current.id == conseq.id:
                state_stack.append(
                    StateHolder(
                        State.CONDITIONAL_CONSEQUENCE,
                        state_stack[-1].route[-1].routes["consequence"],
                    )
                )
            elif enter and alter and current.id == alter.id:
                state_stack.append(
                    StateHolder(
                        State.CONDITIONAL_ALTERNATIVE,
                        state_stack[-1].route[-1].routes["alternative"],
                    )
                )


class BranchStateHandler(StateHandler):
    def _handle( self, current: Node, name: str | None, text: str, state_stack: list[StateHolder], enter: bool,):
        if not current.parent:
            return
        conseq = current.parent.child_by_field_name("consequence")
        alter = current.parent.child_by_field_name("alternative")
        if ( not enter and (conseq and current.id == conseq.id) or (alter and current.id == alter.id)):
            state_stack.pop()
        elif enter:
            ConditionalStateHandler._linear_state_hander._handle(
                current, name, text, state_stack, enter
            )
