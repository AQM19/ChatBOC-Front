"""The main Chat app."""

import reflex as rx
from chatapp.components import chat, navbar

def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )

def login_page() -> rx.Component:
    """Página de inicio de sesión."""
    return rx.chakra.flex(
        "Página de inicio de sesión",
        justify="center",
        align="center",
        height="100vh",
    )

# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)
app.add_page(index)
app.add_page(login_page)