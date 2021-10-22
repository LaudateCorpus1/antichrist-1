class Menu:
    def __init__(self, z):
        self.z = z


class TextBox (Menu):
    def __init__(self, z, text):
        super().__init__(z)
        self.text = text
