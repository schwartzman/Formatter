from .prettytable import PrettyTable

try:
    from colorama import init

    init()
except ImportError:
    pass


RESET_CODE = "\x1b[0m"


class Theme:
    def __init__(
        self,
        default_color = "",
        vertical_char = "|",
        vertical_color = "",
        horizontal_char = "-",
        horizontal_color = "",
        junction_char = "+",
        junction_color = "",
    ):
        self.default_color = Theme.format_code(default_color)
        self.vertical_char = vertical_char
        self.vertical_color = Theme.format_code(vertical_color)
        self.horizontal_char = horizontal_char
        self.horizontal_color = Theme.format_code(horizontal_color)
        self.junction_char = junction_char
        self.junction_color = Theme.format_code(junction_color)

    @staticmethod
    def format_code(s):
        """Takes string and intelligently puts it into an ANSI escape sequence"""
        if s.strip() == "":
            return ""
        elif s.startswith("\x1b["):
            return s
        else:
            return "\x1b[%sm" % s


class Themes:
    DEFAULT = Theme()
    OCEAN = Theme(
        default_color = "96",
        vertical_color = "34",
        horizontal_color = "34",
        junction_color = "36",
    )


class ColorTable(PrettyTable):
    def __init__(self, field_names = None, **kwargs):
        super().__init__(field_names = field_names, **kwargs)
        # TODO: Validate option

        self.theme = kwargs.get("theme") or Themes.DEFAULT

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value
        self.update_theme()

    def update_theme(self):
        theme = self._theme

        self._vertical_char = (
            theme.vertical_color
            + theme.vertical_char
            + RESET_CODE
            + theme.default_color
        )

        self._horizontal_char = (
            theme.horizontal_color
            + theme.horizontal_char
            + RESET_CODE
            + theme.default_color
        )

        self._junction_char = (
            theme.junction_color
            + theme.junction_char
            + RESET_CODE
            + theme.default_color
        )

    def get_string(self, **kwargs):
        return super().get_string(**kwargs) + RESET_CODE
