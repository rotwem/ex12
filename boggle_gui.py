import tkinter as tki
import boggle_board_randomizer
from boggle_Model import BoggleModel

BUTTONS_COLOR = "azure"
BUTTONS_HOVER_COLOR = "powder blue"
BUTTONS_ACTIVE_COLOR = "red"
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": BUTTONS_COLOR,
                "activebackground": BUTTONS_ACTIVE_COLOR}

class BoggleGUI:
    _buttons = {}

    def __init__(self):
        self.model = BoggleModel()
        root = tki.Tk()
        root.title("Boggle by Poli & Rotem")
        root.resizable(False, False)
        self.__main_window = root
        self._display_label = tki.Label(self.__main_window, font=("Courier", 30), width=23, relief="ridge")
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH)
        self._lower_frame = tki.Frame(self.__main_window)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._create_words_board(self.model.get_board())
        self._score_label = tki.Label(self.__main_window, font=("Courier", 30), width=23, relief="ridge")
        self._score_label.pack(side=tki.BOTTOM, fill=tki.BOTH)
        self._score_label["text"] = "0"

    def run(self):
        self.__main_window.mainloop()

    def set_display(self, display_text: str) -> None:
        self._display_label["text"] = display_text

    def _create_words_board(self, board) -> None:
        for i in range(4):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(4):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(4):
            for j in range(4):
                self._make_button(board[i][j], i, j)

    def _make_button(self, button_char: str, row: int, col: int, rowspan: int = 1, columnspan: int = 1):
        button = tki.Button(self._lower_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[button_char] = button

        def _on_enter(event):
            button['background'] = BUTTONS_HOVER_COLOR

        def _on_leave(event):
            button['background'] = BUTTONS_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        return button



if __name__ == "__main__":
    cg = BoggleGUI()
    cg.set_display("TEST MODE")
    cg.run()
