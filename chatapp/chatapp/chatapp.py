"""The main Chat app."""

import reflex as rx
from chatapp.components import chat, navbar
from flask import Flask, jsonify, make_response
from flask_jwt_extended import create_access_token
import hashlib

app = Flask(__name__)

@rx.page(route="/")
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
                            name="user",
                            # type attribute is required for "typeMismatch" validation
                            type="text",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Password"),
                    rx.form.control(
                        rx.input(
                            placeholder="Password",
                            name="pass",
                            # type attribute is required for "typeMismatch" validation
                            type="password",
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
            ),
            on_submit = FormState.handle_submit_login,
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
                            name="email",
                            # type attribute is required for "typeMismatch" validation
                            type="email",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Username"),
                    rx.form.control(
                        rx.input(
                            placeholder="Username",
                            name="user",
                            # type attribute is required for "typeMismatch" validation
                            type="text",
                        ),
                        as_child=True,
                    ),
                    rx.form.label("Password"),
                    rx.form.control(
                        rx.input(
                            placeholder="Password",
                            name="pass",
                            # type attribute is required for "typeMismatch" validation
                            type="password",
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
                
            ),
            on_submit=lambda form_data: rx.window_alert(
                form_data.to_string()
            ),
            reset_on_submit=True,
            width="50vh",
            height="80vh",  # Ajusta la altura del contenedor para centrar verticalmente
            display="grid",
            place_items="center"
        )
        
    )

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit_login(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        self.login(form_data)

    def handle_submit_register(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        self.login(form_data)

    def login(self, data):
        username = data.get("user")
        password = data.get("pass")

        #Hashear 
        hashed_password = self.hash_password(password)


        #Request
    
        user_id=2
        #Cookie
    
        # access_token = create_access_token(identity=user_id)
        # response = jsonify(access_token=access_token)
        # response.set_cookie('access_token', value=access_token)  

    def register(self, data):
        email = data.get("email")
        username = data.get("user")
        password = data.get("pass")  

        #Hashear 
        hashed_password = self.hash_password(password)

        #Request
    
        user_id=2

        #Cookie
    
        # access_token = create_access_token(identity=user_id)
        # response = jsonify(access_token=access_token)
        # response.set_cookie('access_token', value=access_token) 

    def hash_password(self, password):
        """Hash a password."""
        # Codifica la contraseña como bytes UTF-8 antes de pasarla al algoritmo de hash
        encoded_password = password.encode('utf-8')
    
        # Crea un objeto hash SHA-256
        hasher = hashlib.sha256()
    
        # Actualiza el objeto hash con los bytes de la contraseña
        hasher.update(encoded_password)
    
        # Obtiene la representación hexadecimal del hash
        hashed_password = hasher.hexdigest()
    
        return hashed_password

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