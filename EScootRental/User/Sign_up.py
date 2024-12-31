import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import re
from db_pool import get_connection
import bcrypt
from PIL import ImageTk, Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def connect_to_db():
    try:
        connection = get_connection()
        mycursor = connection.cursor(dictionary=True)
        print("Connected to Database!!")
    except:
        messagebox.showerror("Connection", "Database connection not established!")
    return connection, mycursor

connection, mycursor = connect_to_db()

class SignupApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sign Up")
        self.geometry("925x600+300+200")
        self.config(bg="#f0f0f0")
        self.resizable(False, False)

        self.load_background_image()

        self.frame = ctk.CTkFrame(self, width=450, height=550, corner_radius=10)
        self.frame.place(x=250, y=25)

        self.label = ctk.CTkLabel(self.frame, text="Sign Up", font=("Century Gothic", 30, "bold"))
        self.label.place(x=150, y=30)

        self.create_input_fields()

        self.signup_button = ctk.CTkButton(self.frame, text="Sign Up", command=self.enter_pass, width=200, height=40, font=("Century Gothic", 14, "bold"))
        self.signup_button.place(x=125, y=420)

        self.back_button = ctk.CTkButton(self.frame, text="Back", command=self.back_to_login, width=100, height=40, font=("Century Gothic", 14, "bold"))
        self.back_button.place(x=175, y=470)

    def load_background_image(self):
        try:
            image = Image.open("Pictures/um.png")
            image_resized = image.resize((925, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image_resized)
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Error: 'Pictures/um.png' not found.")
        except Exception as e:
            print(f"Error loading image: {e}")

    def create_input_fields(self):
        self.usern_var = ctk.StringVar()
        self.phone_var = ctk.StringVar()
        self.passwo_var = ctk.StringVar()
        self.passwre_var = ctk.StringVar()
        self.idnumb_var = ctk.StringVar()

        self.create_input_field("Username:", 100, self.usern_var)
        self.create_input_field("Phone Number:", 160, self.phone_var)
        self.create_input_field("Password:", 220, self.passwo_var, show="*")
        self.create_input_field("Re-enter Password:", 280, self.passwre_var, show="*")
        self.create_input_field("ID number:", 340, self.idnumb_var)

    def create_input_field(self, label_text, y_position, variable, show=None):
        label = ctk.CTkLabel(self.frame, text=label_text, font=("Century Gothic", 12))
        label.place(x=40, y=y_position)
        entry = ctk.CTkEntry(self.frame, textvariable=variable, width=240, show=show)
        entry.place(x=160, y=y_position)

    def back_to_login(self):
        self.destroy()
        import Front_page
        Sign_In = ctk.CTk()
        app = Front_page.Front_page(Sign_In)
        Sign_In.mainloop()

    def enter_pass(self):
        username = self.usern_var.get().strip()
        phone = self.phone_var.get()
        password = self.passwo_var.get().strip()
        confirm_password = self.passwre_var.get().strip()
        id_number = self.idnumb_var.get()

        if username == "":
            messagebox.showerror("Invalid", "Username cannot be empty")  
        elif not re.match(r"^[0-9]{11}$", phone):
            messagebox.showerror("Invalid", "Enter a valid 11-digit phone number")  
        elif password == "":
            messagebox.showerror("Invalid", "Password cannot be empty")  
        elif confirm_password == "":
            messagebox.showerror("Invalid", "Please re-enter the password")  
        elif password != confirm_password:
            messagebox.showerror("Invalid", "Passwords do not match")  
        elif not re.match(r"^[0-9]{6}$", id_number):
            messagebox.showerror("Invalid", "Enter a valid ID number")  
        else:
            try:
                hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                insert_query = """
                    INSERT INTO useracc (username, phone, password, id_number)
                    VALUES (%s, %s, %s, %s)
                """
                values = (username, phone, hash_password, id_number)

                mycursor.execute(insert_query, values)
                connection.commit()

                messagebox.showinfo("Success", "You have successfully signed up!") 
                self.back_to_login()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    app = SignupApp()
    app.mainloop()
