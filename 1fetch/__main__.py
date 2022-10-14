import platform
import re
import shutil
from dataclasses import dataclass

import psutil
import rich

COLORS = {
    "windows": "blue",
    "macos": "blue",
    "linux": "yellow",
}


@dataclass
class SystemInfo:
    """Stores information about a system.

    Attributes:
        name                 The name of the system.
        os                   The operating system.
        distro               The Linux distribution. On Windows/MacOS systems, this is :code:`None`.
        python_version       The version of Python.
        storage_capacity_gb  The storage capacity in GBs.
        ram_gb               The RAM capacity in GBs.
    """

    name: str
    os: str
    distro: str | None
    python_version: str
    storage_capacity_gb: int
    ram_gb: int

    def print(self) -> None:
        """Print the system info with style."""

        rich.print(
            f"""
[gray39]name[/gray39]     [blue]{self.name}[/blue]
[gray39]os[/gray39]       [blue]{self.os}[/blue]
[gray39]python[/gray39]   [blue]{self.python_version}[/blue]
[gray39]storage[/gray39]  [blue]{self.storage_capacity_gb}GB[/blue]
[gray39]ram[/gray39]      [blue]{self.ram_gb}GB[/blue]
[gray39]hotel[/gray39]    [yellow]Trivago[/yellow]
""".strip()
        )

    @staticmethod
    def from_current_system() -> "SystemInfo":
        """Return a :cls:`SystemInfo` object based on the current system."""

        return SystemInfo(
            name=platform.node(),
            os=platform.system(),
            python_version=platform.python_version(),
            distro=get_linux_distribution(),
            # To convert bytes into gigabytes, divide it by 1e9 (1,000,000,000)
            # Also round it to the nearest integer to have cleaner output
            storage_capacity_gb=round(shutil.disk_usage("C:")[0] / 1e9),
            ram_gb=round(psutil.virtual_memory().total / 1e9),
        )


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


def main() -> None:
    info = SystemInfo.from_current_system()
    info.print()


if __name__ == "__main__":
    main()
