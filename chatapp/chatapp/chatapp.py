"""The main Chat app."""

import reflex as rx
from chatapp.components import chat, navbar
from flask import jsonify
from flask_jwt_extended import create_access_token
from chatapp.state import State



@rx.page(route="/", on_load=State.getChats)
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

@rx.page(route="/login")
def login_page() -> rx.Component:
    """Página de inicio de sesión."""
    return rx.chakra.vstack(
        rx.form.root(
            rx.form.field(
                rx.flex(
                    rx.form.label("Username"),
                    rx.form.control(
                        rx.input(
                            placeholder="Username",
                            # type attribute is required for "typeMismatch" validation
                            type="text",
                            name="username",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Password"),
                    rx.form.control(
                        rx.input(
                            placeholder="Password",
                            # type attribute is required for "typeMismatch" validation
                            type="password",
                            name="password",
                        ),
                        as_child=True,
                    ),
                    rx.form.message(
                        "Please enter a valid email",
                        match="typeMismatch",
                    ),
                    rx.html("<u> <a href=\"/register\">Registrarse</a> </u>"),
                    rx.form.submit(
                        rx.button("Submit"),
                        as_child=True,
                    ),
                    
                    direction="column",
                    spacing="2",
                    align="stretch",
                ),
                name="login",
            ),
            on_submit=State.login,
            reset_on_submit=True,
            width="50vh",
            height="80vh",  # Ajusta la altura del contenedor para centrar verticalmente
            display="grid",
            place_items="center"
        )
        
    )
    
@rx.page(route="/register")
def register_page() -> rx.Component:
    """Página de inicio de sesión."""
    return rx.chakra.vstack(
        rx.form.root(
            rx.form.field(
                rx.flex(
                    rx.form.label("Email"),
                    rx.form.control(
                        rx.input(
                            placeholder="Email",
                            # type attribute is required for "typeMismatch" validation
                            type="email",
                            name="email",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Username"),
                    rx.form.control(
                        rx.input(
                            placeholder="Username",
                            # type attribute is required for "typeMismatch" validation
                            type="text",
                            name="username",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Password"),
                    rx.form.control(
                        rx.input(
                            placeholder="Password",
                            # type attribute is required for "typeMismatch" validation
                            type="password",
                            name="password"
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Confirm Password"),
                    rx.form.control(
                        rx.input(
                            placeholder="confirm Password",
                            # type attribute is required for "typeMismatch" validation
                            type="password",
                            name="confirm_password"
                        ),
                        as_child=True,
                    ),
                    rx.form.message(
                        "Please enter a valid email",
                        match="typeMismatch",
                    ),
                    rx.html("<u> <a href=\"/login\">LogIn</a> </u>"),
                    rx.form.submit(
                        rx.button("Submit"),
                        as_child=True,
                    ),
                    
                    direction="column",
                    spacing="2",
                    align="stretch",
                ),
                name="register",
            ),
            on_submit=State.register,
            reset_on_submit=True,
            width="50vh",
            height="80vh",  # Ajusta la altura del contenedor para centrar verticalmente
            display="grid",
            place_items="center"
        )
        
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
app.add_page(register_page)
