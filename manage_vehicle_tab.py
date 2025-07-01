import customtkinter as ctk
from pathlib import Path
from PIL import Image, ImageTk

class ManageVehicleTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF", corner_radius=0)
        self.scale_factor = 0.8
        self.create_widgets()

    def load_and_resize_image(self, image_path, size=None):
        img = Image.open(relative_to_assets(image_path))
        if size:
            scaled_size = (int(size[0] * self.scale_factor), int(size[1] * self.scale_factor))
            img = img.resize(scaled_size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        vehicle_cards = [
            {"type": "Motorcycle", "image": "image_3.png"},
            {"type": "6 Seater Car", "image": "image_5.png"},
            {"type": "4 Seater Car", "image": "image_4.png"},
            {"type": "Mini Van", "image": "image_7.png"},
            {"type": "Van", "image": "image_6.png"},
            {"type": "Add New", "image": "button_2.png", "is_add_button": True}
        ]

        for i, card in enumerate(vehicle_cards):
            row = i // 3
            col = i % 3

            card_width = int(300 * self.scale_factor)
            card_height = int(280 * self.scale_factor)

            card_frame = ctk.CTkFrame(self, fg_color="#FFBEBE" if card.get("is_add_button") else "#510000",
                                      corner_radius=10, width=card_width, height=card_height)

            x_pos = 50 + col * (card_width + 20)
            y_pos = 80 + row * (card_height + 20)

            card_frame.place(x=x_pos, y=y_pos)

            if card.get("is_add_button"):
                add_icon = self.load_and_resize_image(card["image"], (48, 48))
                ctk.CTkButton(card_frame, image=add_icon, text="", fg_color="transparent", hover_color="#FFD0D0").place(relx=0.5, rely=0.4, anchor="center")
                ctk.CTkLabel(card_frame, text="Add New Vehicle", text_color="#000000", font=("Inter Medium", 16)).place(relx=0.5, rely=0.7, anchor="center")
            else:
                vehicle_img = self.load_and_resize_image(card["image"], (150, 100))
                ctk.CTkLabel(card_frame, image=vehicle_img, text="", fg_color="transparent").place(relx=0.5, rely=0.3, anchor="center")
                ctk.CTkLabel(card_frame, text=card["type"], text_color="#FFFFFF", font=("Inter", 18)).place(relx=0.5, rely=0.55, anchor="center")

                ctk.CTkLabel(card_frame, text="Cost Per Mile", text_color="#FFFFFF", font=("Inter", 16)).place(relx=0.5, rely=0.65, anchor="center")

                entry_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
                entry_frame.place(relx=0.5, rely=0.8, anchor="center")

                ctk.CTkLabel(entry_frame, text="₱", text_color="#FFFFFF", font=("Inter", 20)).pack(side="left", padx=5)

                entry = ctk.CTkEntry(entry_frame, width=120, height=28, fg_color="#747474", text_color="#000716", border_width=0, corner_radius=5)
                entry.pack(side="left")

        save_button = ctk.CTkButton(self, text="Save", command=self.save_clicked)
        save_button.place(relx=0.85, rely=0.95)

    def save_clicked(self):
        print("Save button clicked")
