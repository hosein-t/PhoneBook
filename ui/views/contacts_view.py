from customtkinter import CTkLabel
from PhoneBook import shared
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.models.contact import Contact, show_empty_contacts_message



def initialize_contacts_view(contacts_data):
    # Labels
    shared.contacts_count_text = my_label(shared.root, text=":تعداد مخاطبین", x=278, y=87, size=11, fg="#AAB7CC", font="Samim WOL")
    shared.contacts_count_label = CTkLabel(shared.root, textvariable=shared.contacts_count, width=38, height=24, fg_color="#292342", text_color="#D0C4FF", font=("TkFixedFont", 14, "bold"), corner_radius=12, border_width=1, border_color="#62558F")
    shared.contacts_count_label.place(x=234, y=90)

    if not contacts_data:
        shared.contacts_count_text.place_forget()
        shared.contacts_count_label.place_forget()

    # Add Contacts
    if not contacts_data:
        show_empty_contacts_message()
    else:
        for contact in contacts_data:
            Contact(contact["name"], contact["number"], contact["group"], contact.get("favorite", False))