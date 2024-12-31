import tkinter as tk
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import customtkinter

class LocationPage:
    def __init__(self, master, user_data=None):
        self.master = master
        self.user_data = user_data

        master.title("Station Location")
        master.geometry("950x550")
        master.resizable(False, False)

        self.map_widget = TkinterMapView(master, width=950, height=550, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(7.066488, 125.595682)
        self.map_widget.set_zoom(17)

        self.add_markers()

        self.back_button = customtkinter.CTkButton(
            master, text="Back", font=("Century Gothic", 14), fg_color="#57a1f8", 
            text_color="white", command=self.back_to_main, cursor="hand2"
        )
        self.back_button.place(x=800, y=500)        

        self.overlay_label = None

    def add_markers(self):
        self.marker_data = [
            {"lat": 7.065089, "lng": 125.598142, "name": "Matina Gate", "image": "Matina_Gate.jpg"},
            {"lat": 7.065483, "lng": 125.596321, "name": "BE Building", "image": "BE building.jpg"},
            {"lat": 7.067424, "lng": 125.596408, "name": "GET Building", "image": "GET building.jpg"},
            {"lat": 7.068349, "lng": 125.595643, "name": "DPT Building", "image": "DPT building.jpg"},
            {"lat": 7.067512, "lng": 125.592169, "name": "MAA Gate", "image": "MAA gate.jpg"}
        ]

        self.marker_map = {}

        for marker_info in self.marker_data:
            marker = self.map_widget.set_marker(
                marker_info["lat"], marker_info["lng"], text=marker_info["name"],
                command=self.on_marker_click
            )
            self.marker_map[marker] = marker_info

    def on_marker_click(self, marker):
        marker_info = self.marker_map.get(marker)

        if marker_info:
            self.show_image(marker_info)
        else:
            print("No data for marker.")

    def show_image(self, marker_info):
        if self.overlay_label:
            self.overlay_label.destroy()

        image_path = f"Pictures/{marker_info['image']}"
        try:
            img = Image.open(image_path).resize((300, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.overlay_label = tk.Label(self.master, image=photo, bg="white")
            self.overlay_label.image = photo
            self.overlay_label.place(x=620, y=10)

            close_button = customtkinter.CTkButton(
                self.overlay_label, text="Close", font=("Century Gothic", 12),
                fg_color="#FF5555", text_color="white", command=self.close_img, cursor="hand2"
            )
            close_button.place(relx=0.5, rely=0.9, anchor="center")

        except FileNotFoundError:
            print(f"Image not found for {marker_info['name']}")

    def back_to_main(self):
        self.master.destroy()
        print("Returning to the main page...")
        rental_root = customtkinter.CTk()  
        import Main_Page
        app = Main_Page.Main_Page(rental_root, self.user_data)
        rental_root.mainloop()

    def close_img(self):
        if self.overlay_label:
            self.overlay_label.destroy()
            self.overlay_label = None

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = LocationPage(root, user_data={"username": "test_user"})
    root.mainloop()
