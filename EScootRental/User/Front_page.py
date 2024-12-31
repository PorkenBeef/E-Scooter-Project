from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import customtkinter
from db_pool import get_connection
import bcrypt

class Front_page:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("925x500+300+200")
        self.root.resizable(False, False)

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.myresult = None 

        self.setup_ui() 

    def setup_ui(self):
        img = ImageTk.PhotoImage(file="Pictures/Pogi_Logo.png")
        Label(self.root, image=img, bg="white").place(x=-100, y=-195)
        self.root.image = img 

        frame = Frame(self.root, width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        heading = Label(frame, text="Sign in", fg="#57a1f8", bg="white",
                        font=("Microsoft YaHei UI light", 23, "bold"))
        heading.place(x=110, y=5)

        self.user = Entry(frame, width=30, fg="black", border=0, bg="white",
                          font=("Microsoft YaHei UI light", 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, "Username")
        self.user.bind("<FocusIn>", self.on_enter_user)
        self.user.bind("<FocusOut>", self.on_leave_user)
        Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

        self.UserP = Entry(frame, width=30, fg="black", border=0, bg="white",
                           show="*", font=("Microsoft YaHei UI light", 11))
        self.UserP.place(x=30, y=150)
        self.UserP.insert(0, "Password")
        self.UserP.bind("<FocusIn>", self.on_enter_pass)
        self.UserP.bind ("<FocusOut>", self.on_leave_pass)
        Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

        Button(frame, width=39, pady=7, text="Sign in", bg="#57a1f8", fg="white",
               border=0, command=self.signing).place(x=35, y=204)

        label = Label(frame, text="Don't have an account?", fg="black", bg="white",
                      font=("Microsoft YaHei UI Light", 9))
        label.place(x=75, y=270)

        Button(frame, width=6, text="Sign up", border=0, bg="white", cursor="hand2",
                fg="#57a1f8", command=self.sign_up).place(x=215, y=270)


    def on_enter_user(self, e):
        if self.user.get() == "Username":
            self.user.delete(0, "end")

    def on_leave_user(self, e):
        if self.user.get() == "":
            self.user.insert(0, "Username")

    def on_enter_pass(self, e):
        if self.UserP.get() == "Password":
            self.UserP.delete(0, "end")

    def on_leave_pass(self, e):
        if self.UserP.get() == "":
            self.UserP.insert(0, "Password")
                
    def signing(self):
        username = self.user.get().strip()
        password = self.UserP.get().strip()

        if username == "" or username == "Username" or password == "" or password == "Password":
            messagebox.showerror("Entry Error", "Type username or password")
            return

        try:
            connection = get_connection()
            mycursor = connection.cursor(dictionary=True)
            print("Connected to Database!!")
        except:
            messagebox.showerror("Connection Error", "Database connection not established!")
            return

        try:
            query = "SELECT * FROM useracc WHERE username=%s"
            mycursor.execute(query, (username,))
            self.myresult = mycursor.fetchone()
            print(self.myresult)

            if self.myresult is None:
                messagebox.showinfo("Invalid", "Invalid username or password!")
                return

            # Verify the password
            stored_hash = self.myresult["password"]
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                messagebox.showinfo("Invalid", "Invalid username or password!")
                return

            query = """
                SELECT user_status 
                FROM rental_history 
                WHERE username=%s 
                ORDER BY id DESC LIMIT 1
            """
            mycursor.execute(query, (username,))
            rental_status = mycursor.fetchone()

            if rental_status and rental_status["user_status"] == "Active":
                messagebox.showinfo("Account Status", "You have an active rental. Please complete it before proceeding.")
                return

            self.open_main_page()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                mycursor.close()
                connection.close()

        
    def open_main_page(self):
        self.root.destroy()  

        rental_root = customtkinter.CTk()  
        import Main_Page
        app = Main_Page.Main_Page(rental_root, self.myresult)
        rental_root.mainloop()
 
    def sign_up(self):
        self.root.destroy()
        import Sign_up
        app = Sign_up.SignupApp()
        app.mainloop()

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = Front_page(root)
    root.mainloop()

