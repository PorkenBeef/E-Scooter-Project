import tkinter
from tkinter import messagebox
import customtkinter
from PIL import ImageTk, Image
from db_pool import get_connection
import Amainpage

class AdminLoginApp:
    def __init__(self):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("green")

        self.app = customtkinter.CTk()
        self.app.geometry("600x440")
        self.app.title('Admin Login')
        self.app.resizable(False, False)

        self.admin_data = None

        self.setup_ui()
        self.app.mainloop()

    def setup_ui(self):
        img1 = ImageTk.PhotoImage(Image.open("Pictures/Campus.jpg"))
        Pic = customtkinter.CTkLabel(master=self.app, image=img1)
        Pic.pack()

        frame = customtkinter.CTkFrame(master=Pic, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        Header = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
        Header.place(x=50, y=45)

        self.User = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
        self.User.place(x=50, y=110)

        self.UserP = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
        self.UserP.place(x=50, y=165)

        button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=self.signin, corner_radius=6)
        button1.place(x=50, y=240)

    def signin(self):
        username = self.User.get()
        password = self.UserP.get()

        if not username or not password:
            messagebox.showerror("Entry Error", "Type username or password")
            return

        try:
            connection = get_connection()
            mycursor = connection.cursor(dictionary=True)
            command = "SELECT * FROM adminacc WHERE Username=%s AND Password=%s"
            mycursor.execute(command, (username, password))
            myresult = mycursor.fetchone()
            print(myresult)

        except Exception as e:
            messagebox.showerror("Connection", f"Database connection not established: {e}")
            return
        finally:
            if connection.is_connected():
                mycursor.close()
                connection.close()

        if myresult is None:
            messagebox.showinfo("Invalid", "Invalid username or password")
        else:
            self.admin_data = myresult
            self.app.destroy()

            # Pass myresult to AdminApp
            root = Amainpage.AdminApp(self.admin_data)  # Pass admin data here
            root.mainloop()


if __name__ == "__main__":
    AdminLoginApp()
