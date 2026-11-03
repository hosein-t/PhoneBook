from tkinter import Label, PhotoImage



def my_label(window, x, y, text=None, image=None, textvariable=None, bg="#0D1729", fg="white", font="Vazir", size=12, style="normal", cursor="arrow", anchor=False) -> Label:
    label = Label(window, text=text, image=image, textvariable=textvariable, bg=bg, fg=fg, font=(font, size, style), cursor=cursor)
    label.place(x=x, y=y, anchor="e" if anchor else None)

    return label


def label_image(window, address, x, y, bg="#0D1729") -> Label:
    image = PhotoImage(file=address)

    label = my_label(window=window, image=image, x=x, y=y, bg=bg)
    label.image = image

    return label