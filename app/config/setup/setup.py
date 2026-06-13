from decouple import config


def get_variable(name: str) -> str:
    var = config(name)

    if var.startswith("<") or not var:
        raise Exception(f"Invalid or missing {var} in the .env file")

    return var


# Django
DJANGO_KEY  : str = get_variable("DJANGO_KEY")

# MySQL
MYSQL_USERNAME : str  = get_variable("MYSQL_USERNAME")
MYSQL_PASSWORD : str  = get_variable("MYSQL_PASSWORD")
MYSQL_ADDRESS  : str  = get_variable("MYSQL_ADDRESS")
MYSQL_NAME     : str  = get_variable("MYSQL_NAME")
MYSQL_PORT     : str  = get_variable("MYSQL_PORT")
