from tkinter import Label, Toplevel



class tooltip:
    def __init__(self, widget, text):
        self.tip = None
        self.timer = None
        self.widget = widget
        self.text = text

        self.widget.bind("<Enter>", self.show, add="+")
        self.widget.bind("<Leave>", self.hide, add="+")

    def show(self, event):
        self.timer = self.widget.after(300, lambda: self.create_tip(event))

    def create_tip(self, event):
        self.tip = Toplevel(self.widget, bg="#303030", highlightbackground="#555555", highlightthickness=1)

        self.tip.overrideredirect(True)
        self.tip.attributes("-topmost", True)

        Label(self.tip, text=self.text, bg="#303030", fg="white", font=("Vazir", 9)).pack(padx=6, pady=3)

        self.tip.geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

    def hide(self, _):
        if self.timer:
            self.widget.after_cancel(self.timer)
            self.timer = None

        if self.tip:
            self.tip.destroy()
            self.tip = None
