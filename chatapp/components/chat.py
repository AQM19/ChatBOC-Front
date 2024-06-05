import reflex as rx

from chatapp.components import loading_icon
from chatapp.state import QA, State


message_style = dict(display="inline-block", padding="1em", border_radius="8px", max_width=["30em", "30em", "50em", "50em", "50em", "50em"])


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.box(
            rx.markdown(
                qa.answer,
                background_color=rx.color("accent", 4),
                color=rx.color("accent", 12),
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.scroll_area(
            rx.text(rx.foreach(State.chats[State.current_chat], message), width="100%", id="chat-box"),
            rx.text("", id="chat-end"),
            py="8",
            flex="1",
            width="100%",
            max_width="50em",
            padding_x="4px",
            align_self="center",
            align_items="center",
            overflow="hidden",
            padding_bottom="5em",
            on_mount=State.scroll_to_bottom,
            
        )
    

def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        rx.radix.text_field.root(
                            rx.radix.text_field.input(
                                placeholder="Escribe algo...",
                                id="question",
                                width=["15em", "20em", "45em", "50em", "50em", "50em"],
                                name="question",
                                on_change=State.set_question,
                            ),
                            rx.radix.text_field.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Haz una pregunta",
                                )
                            ),
                        ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text("Send"),
                            ),
                            on_click=State.submit_question,
                            type="submit",
                        ),
                        rx.button(
                            "⇓", 
                            on_click=State.scroll_to_bottom,
                            id="scroll-down",
                            type="button"
                            ),
                        align_items="center",
                    ),
                    is_disabled=State.processing,
                ),
                #on_submit=State.submit_question,
                on_submit=State.process_question,
                reset_on_submit=True,
            ),
            rx.text(
                "ChatBOC puede responder incorrectamente o imprecisa. Uselo con precaución.",
                text_align="center",
                font_size=".75em",
                color=rx.color("mauve", 10),
            ),
            #rx.logo(margin_top="-1em", margin_bottom="-1em"),
            align_items="center",
        ),
        position="sticky",
        bottom="0",
        left="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        align_items="stretch",
        width="100%",
    )
