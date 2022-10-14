import platform
import re


def get_linux_distribution() -> str | None:
    """Attempt to get the Linux distribution.
    If the system is not Linux, this will return :code:`None`.
    """

    if platform.system() != "Linux":
        return None

    try:
        with open("/etc/os-release") as file:
            name_regex_result = re.findall('NAME="(.+)"', file.read())

            try:
                return name_regex_result[0]
            except IndexError as e:
                raise ValueError("NAME property not found") from e
    except IOError as e:
        raise FileNotFoundError("/etc/os-release") from e
