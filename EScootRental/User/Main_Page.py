import customtkinter
import tkinter as tk
from tkinter import messagebox
import time
import threading
import mysql.connector
from db_pool import get_connection
from PIL import ImageTk, Image
import pywinstyles
from enum import Enum

try:
    connection = get_connection()
    mycursor = connection.cursor(dictionary=True)
    print("Connected to Database!!")
except:
    print("No connection")

class Main_Page:
    def __init__(self, master, user_data=None):
        self.master = master
        self.user_data = user_data  
        master.title("E-Scooter Rental System")
        master.geometry("950x500+300+200")
        master.resizable(False, False)
        master.config(bg="#ADD8E6")
        
        self.balance = 0 
        self.timer_running = False
        self.start_time = 0
        self.total_time = 0  
        self.deduction_rate_per_second = 0.031
        self.deducted_amount = 0
        self.buttons_visible = False
        self.buttons_frame = None
        self.rented_scooters = []
        self.active_rentals = []
        

        class Scooter (Enum):
            SCOOTER_1 = "Scooter 1"
            SCOOTER_2 = "Scooter 2"
            SCOOTER_3 = "Scooter 3"
            SCOOTER_4 = "Scooter 4"
            SCOOTER_5 = "Scooter 5"
            SCOOTER_6 = "Scooter 6"
            SCOOTER_7 = "Scooter 7"
            SCOOTER_8 = "Scooter 8"
            SCOOTER_9 = "Scooter 9"
            SCOOTER_10 = "Scooter 10"
            SCOOTER_11 = "Scooter 11"
            SCOOTER_12 = "Scooter 12"
            SCOOTER_13 = "Scooter 13"
            SCOOTER_14 = "Scooter 14"
            SCOOTER_15 = "Scooter 15"
            SCOOTER_16 = "Scooter 16"
            SCOOTER_17 = "Scooter 17"
            SCOOTER_18 = "Scooter 18"
            SCOOTER_19 = "Scooter 19"
            SCOOTER_20 = "Scooter 20"
        
        self.sections = {
            "Matina Gate": [Scooter.SCOOTER_1, Scooter.SCOOTER_2, Scooter.SCOOTER_3,Scooter.SCOOTER_4],
            "BE Building": [Scooter.SCOOTER_5, Scooter.SCOOTER_6, Scooter.SCOOTER_7,Scooter.SCOOTER_8],
            "GET Building": [Scooter.SCOOTER_9, Scooter.SCOOTER_10, Scooter.SCOOTER_11,Scooter.SCOOTER_12],
            "DPT Building": [Scooter.SCOOTER_13, Scooter.SCOOTER_14, Scooter.SCOOTER_15,Scooter.SCOOTER_16],
            "Maa Gate": [Scooter.SCOOTER_17, Scooter.SCOOTER_18, Scooter.SCOOTER_19,Scooter.SCOOTER_20],
        }

        self.setup_ui()

        self.fetch_balance_from_db() 
        
        self.return_scooter_loop()

        self.load_active_rentals()

        print(user_data)

    def setup_ui(self):
        try:
            image = Image.open("Pictures/Main_Bg.png")
        
            self.image_resized = image.resize((self.master.winfo_width(), self.master.winfo_height()), Image.Resampling.LANCZOS)
            self.main_bg_image = ImageTk.PhotoImage(self.image_resized)

            self.bg_label = tk.Label(self.master, image=self.main_bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except FileNotFoundError:
            print("Error: 'Pictures/Main_Bg.png' not found.")

        selection_frame = customtkinter.CTkFrame(
            master=self.master, 
            width=400, 
            height=200, 
            corner_radius=10, 
            fg_color="#f0f0f0",
            bg_color="blue"
            )
        selection_frame.pack(padx=20, pady=20)
        selection_frame.place(x=580,y=200)

        selection_title = customtkinter.CTkLabel(

            selection_frame, 
            text="Station & Scooter Selection", 
            font=("Microsoft YaHei UI light", 18, "bold"), 
            text_color="#333333"
        )
        selection_title.pack(pady=10,padx=20)

        station_label = customtkinter.CTkLabel(
            selection_frame, 
            text="Choose a Station:", 
            font=("Microsoft YaHei UI light", 14), 
            text_color="#555555"
        )   
        station_label.pack(anchor="w", padx=20)

        self.section_var = tk.StringVar(value="Matina Gate")
        self.section_menu = customtkinter.CTkOptionMenu(
            selection_frame, 
            variable=self.section_var, 
            values=list(self.sections.keys()), 
            command=self.update_scooter_menu,
            dropdown_fg_color="#ffffff", 
            dropdown_text_color="#333333"
        )
        self.section_menu.pack(padx=20, pady=5, fill="x")
        self.section_var.set("Matina Gate") 

        scooter_label = customtkinter.CTkLabel(
            selection_frame, 
            text="Choose a Scooter:", 
            font=("Microsoft YaHei UI light", 14), 
            text_color="#555555"
        )
        scooter_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.scooter_var = tk.StringVar(value=self.sections["Matina Gate"][0].value)  
        self.scooter_menu = customtkinter.CTkOptionMenu(
            selection_frame, 
            variable=self.scooter_var, 
            values=[scooter.value for scooter in self.sections["Matina Gate"]],  
            dropdown_fg_color="#ffffff", 
            dropdown_text_color="#333333"
        )
        self.scooter_menu.pack(padx=20, pady=5, fill="x")
        
        info_frame = customtkinter.CTkFrame(
            master=self.master, 
            width=400, 
            height=150, 
            corner_radius=10, 
            fg_color="#f0f0f0",
            bg_color="blue"
        )
        info_frame.pack(padx=20, pady=20)
        info_frame.place(x=560, y=50)

        self.balance_label = customtkinter.CTkLabel(
            info_frame, 
            text="Balance: 0 pesos", 
            font=("Microsoft YaHei UI light", 18, "bold"), 
            text_color="#0078D7"
        )
        self.balance_label.pack(pady=20)

        self.timer_label = customtkinter.CTkLabel(
            info_frame, 
            text="Timer: 0 minutes 0 seconds", 
            font=("Microsoft YaHei UI light", 22, "bold"), 
            text_color="#333333"
        )
        self.timer_label.pack(padx=20)

        scooter_ids = ', '.join(map(str, self.active_rentals)) if self.active_rentals else 'N/A'

        self.user = customtkinter.CTkLabel(
            info_frame,
            text=f"User: {self.user_data.get('username', 'N/A')} | ID: {self.user_data.get('id_number', 'N/A')} | Scooter: {scooter_ids}",
            font=("Microsoft YaHei UI light", 14),
            text_color="#333333"
        )
        self.user.pack(pady=5)

        self.buttons_exte()

        self.update_scooter_menu(self.section_var.get())
    
    def buttons(self):
        buttonFrame = customtkinter.CTkFrame(self.master, width=500, height=400, corner_radius=9, fg_color="transparent",border_color='none')
        buttonFrame.place(x=10, y=75)

        self.button_rent = customtkinter.CTkButton(buttonFrame, text="Rent Scooter", command=self.rent_scooter, width=150)
        self.button_rent.pack(padx=10, pady=10)

        self.button_return = customtkinter.CTkButton(buttonFrame, text="Return Scooter", command=self.return_scooter, width=150)
        self.button_return.pack(padx=10, pady=10)

        self.button_pause = customtkinter.CTkButton(buttonFrame, text="Pause Rental", command=self.pause_rental, width=150)
        self.button_pause.pack(padx=10, pady=10)

        self.button_resume = customtkinter.CTkButton(buttonFrame, text="Resume Rental", command=self.resume_rental, width=150)
        self.button_resume.pack(padx=10, pady=10)

        self.add_balance = customtkinter.CTkButton(buttonFrame, text='Add balance',command= self.manual_balance_adding, width=150)
        self.add_balance.pack(padx=10,pady=10)

        def Location():
            if self.timer_running ==True:
                res = messagebox.showinfo("ERROR CANNOT BE OPENED", "You have a rental ongoing")
            else:
                self.master.destroy()
                import Location_page
                LocPage = customtkinter.CTk()  
                Lo = Location_page.LocationPage(LocPage, self.user_data)
                LocPage.mainloop()

        self.button_show_location = customtkinter.CTkButton(buttonFrame, text="Show Location", command=Location, width=150)
        self.button_show_location.pack(padx=10, pady=10)

        def Log_Out():
            res = messagebox.askokcancel("Exit application", "Are you sure you want to close the application?")
            self.master.destroy()
            rental_root = customtkinter.CTk()  
            import Front_page
            app = Front_page.Front_page(rental_root)
            rental_root.mainloop()

        self.log_out = customtkinter.CTkButton(buttonFrame, text="Log Out", command=Log_Out, width=150)
        self.log_out.pack(padx=10, pady=10)

    def fetch_balance_from_db(self):
        """Fetch the user's balance from the database using the existing connection."""
        try:
            mycursor = connection.cursor(dictionary=True)
            print("Fetching balance for:", self.user_data['username'])  
    
            query = "SELECT Balance FROM useracc WHERE username = %s"
            mycursor.execute(query, (self.user_data['username'],))
    
            result = mycursor.fetchone()
    
            if result:  
                print("Balance fetched:", result)  
                if 'Balance' in result and result['Balance'] is not None:
                    self.balance = result['Balance']
                else:
                    self.balance = 0  
                self.update_balance()  
            else:
                self.balance = 0
                self.update_balance() 
        except mysql.connector.Error as err:
            print(f"Error: {err}")  
            messagebox.showerror("Database Error", f"Error: {err}")

        if self.master:
            self.master.after(1000, self.fetch_balance_from_db)
            
    def manual_balance_adding(self):
        if hasattr(self, 'manualadding') and self.manualadding.winfo_exists():
            self.manualadding.lift()
            return

        self.manualadding = customtkinter.CTk()
        self.manualadding.geometry("400x200")
        self.manualadding.resizable(False, False)
        self.manualadding.title("Add Balance")

        Cardbar = customtkinter.CTkEntry(self.manualadding, width=300)
        Cardbar.pack(padx=10, pady=10)

        def code_checking():
            CardbarF = Cardbar.get().strip()
            if not CardbarF:
                messagebox.showerror("Input Error", "Please enter a valid card code.")
                return

            try:
                mycursor = connection.cursor(dictionary=True)
                query_balancecard = "SELECT amount FROM balancecards WHERE codes = %s"
                mycursor.execute(query_balancecard, (CardbarF,))
                result2 = mycursor.fetchone()

                if not result2:
                    messagebox.showerror("Invalid Code", "The gift card code is invalid or already used.")
                    return

                card_amount = result2['amount']

                self.balance += card_amount
                self.update_balance()

                messagebox.showinfo("Balance Updated", f"Successfully added {card_amount} pesos to your balance!")

                mark_as_used = "DELETE FROM balancecards WHERE codes = %s"
                mycursor.execute(mark_as_used, (CardbarF,))
                connection.commit()

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                self.manualadding.destroy()

        yes = customtkinter.CTkButton(self.manualadding, text='Confirm', command=code_checking)
        yes.pack(padx=10, pady=10)

        def close_adding():
            self.manualadding.destroy()

        close = customtkinter.CTkButton(self.manualadding, text='Close', command=close_adding)
        close.pack(padx=10, pady=10)

        self.manualadding.mainloop()

    def update_balance(self):
        """Update the balance on the UI and in the database."""
        self.balance_label.configure(text=f"Balance: {self.balance:.2f} pesos")
        try:
            mycursor = connection.cursor(dictionary=True)
            query = "UPDATE useracc SET Balance = %s WHERE username = %s"
            mycursor.execute(query, (self.balance, self.user_data['username']))
            connection.commit()
            print("Balance updated in the database.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def rent_scooter(self):
        if not self.user_data or 'username' not in self.user_data or 'id_number' not in self.user_data:
            messagebox.showerror("Error", "User data is incomplete. Please log in again.")
            return

        self.refresh_scooter_menu()

        username = self.user_data['username']
        id_number = self.user_data['id_number']
        selected_scooter = self.scooter_var.get()

        if not selected_scooter:
            messagebox.showerror("Error", "Please select a scooter to rent.")
            return

        if selected_scooter in self.rented_scooters:
            messagebox.showerror("Error", "Scooter is already rented!")
            return

        if self.timer_running:
            messagebox.showinfo("Rental Active", "You're already renting a scooter!")
            return

        if self.balance <= 15:
            messagebox.showinfo("No Balance", "You need to have at least 15 PHP balance to rent a scooter.")
            return

        try:
            query = "SELECT * FROM useracc WHERE username = %s AND id_number = %s"
            mycursor.execute(query, (username, id_number))
            result = mycursor.fetchone()

            if not result:
                messagebox.showerror("User Not Found", "No such user found in the system.")
                return

            insert_query = """
            INSERT INTO rental_history (username, id_number, user_status, escoot_id)
            VALUES (%s, %s, %s, %s)
            """
            mycursor.execute(insert_query, (username, id_number, "Active", selected_scooter))
            connection.commit()

            self.rented_scooters.append(selected_scooter)
            self.start_time = time.time()
            self.timer_running = True
            self.deducted_amount = 0

            self.update_timer()

            rental_fee = self.deduction_rate_per_second * 60
            self.balance -= rental_fee
            self.update_balance()

            messagebox.showinfo("Rental Started", "You have successfully rented a scooter. Enjoy your ride!")

            self.update_user_label(selected_scooter)

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"Error while processing rental: {err}")


    def return_scooter(self):
        if not self.timer_running:
            messagebox.showinfo("No Active Rental", "You don't have any active rental!")
            return

        username = self.user_data['username']
        id_number = self.user_data['id_number']

        try:
            connection = get_connection()
            mycursor = connection.cursor(dictionary=True)
            selected_scooter = self.scooter_var.get()
            self.refresh_scooter_menu()

            if not selected_scooter or selected_scooter not in self.rented_scooters:
                messagebox.showerror("Error", "No valid scooter selected for return.")
                return

            self.rented_scooters.remove(selected_scooter)

            rental_time = time.time() - self.start_time
            total_seconds = int(rental_time)

            self.deducted_amount = total_seconds * self.deduction_rate_per_second

            total_minutes = total_seconds // 60
            total_seconds_remaining = total_seconds % 60
            self.total_time = f"{total_minutes} minutes {total_seconds_remaining} seconds"

            update_query = """
            UPDATE rental_history 
            SET user_status = %s, user_time = %s, deducted_amount = %s, escoot_id = %s
            WHERE username = %s AND id_number = %s AND user_status = %s
            ORDER BY id DESC LIMIT 1
            """
            mycursor.execute(update_query, (
                "Inactive",
                self.total_time,
                self.deducted_amount,
                selected_scooter,
                username,
                id_number,
                "Active",
            ))

            if mycursor.rowcount == 0:
                messagebox.showerror("Error", "No active rental found for this user.")
                return

            connection.commit()

            self.timer_running = False
            self.start_time = None

            self.balance -= self.deducted_amount
            self.update_balance()

            messagebox.showinfo(
                "Rental Completed",
                f"Your total rental amount is {self.deducted_amount:.2f} pesos.\nScooter successfully returned."
            )
            

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"An error occurred: {err}")

        finally:
            if connection.is_connected():
                mycursor.close()
                connection.close()

    def return_scooter_loop(self):
        try:
            connection = get_connection()
            mycursor = connection.cursor(dictionary=True)

            query = "SELECT username, user_status FROM rental_history WHERE user_status = 'Active'"
            mycursor.execute(query)
            result = mycursor.fetchall()

            for record in result:
                username = record["username"]
                user_status = record["user_status"]

                if user_status == "Inactive":
                    print(f"Detected inactive rental for user: {username}. Processing return...")
                    self.return_scooter()  

            mycursor.close()
            connection.close()

        except Exception as e:
            print(f"Error during rental check: {e}")

        self.master.after(1000, self.return_scooter_loop)


    def pause_rental(self):
        if self.timer_running:
            self.timer_running = False
            self.deducted_amount += (time.time() - self.start_time) * self.deduction_rate_per_second
            self.balance -= self.deducted_amount
            self.update_balance()
            messagebox.showinfo("Rental Paused", f"Your total rental amount is {self.deducted_amount:.2f} pesos.")
        else:
            messagebox.showinfo("No Active Rental", "You're not renting a scooter!")

    def resume_rental(self):
        if not self.timer_running:
            self.start_time = time.time() - self.total_time
            self.timer_running = True
            self.update_timer()
        else:
            messagebox.showinfo("Rental Active", "You're already renting a scooter!")

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.total_time = elapsed_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            self.timer_label.configure(text=f"Timer: {minutes} minutes {seconds} seconds")

            deduction = self.total_time * self.deduction_rate_per_second - self.deducted_amount

            if self.balance - deduction >= 0:
                self.balance -= deduction
                self.deducted_amount += deduction
            else:
                self.balance -= deduction
                self.deducted_amount += deduction
            
            self.update_balance()

            self.update_rental_history(self.deducted_amount, elapsed_time)

        if self.timer_running:
            self.master.after(1000, self.update_timer)


    def buttons_exte(self):
        image_path = "Pictures/buttons2.png"

        try:
            image = Image.open(image_path)
            resized_image = image.resize((60, 60))
            settings = ImageTk.PhotoImage(resized_image)

            img_label = customtkinter.CTkButton(
                self.master,
                image=settings,
                command=self.buttons,
                text="",
                width=50,
                height=50,
                fg_color="dark blue",  
            )
            img_label.place(x=1, y=1)

        except FileNotFoundError:
            print(f"Error: File not found at {image_path}")


    def update_rental_time(self):
        while self.timer_running:
            try:
                rental_time = time.time() - self.start_time
                total_seconds = int(rental_time)
                total_minutes = total_seconds // 60
                total_seconds_remaining = total_seconds % 60
                formatted_time = f"{total_minutes} minutes {total_seconds_remaining} seconds"

                self.deducted_amount = total_seconds * 0.031

                update_query = """
                UPDATE rental_history
                SET user_time = %s, deducted_amount = %s
                WHERE username = %s AND id_number = %s AND user_status = %s
                ORDER BY id DESC LIMIT 1
                """
                mycursor.execute(update_query, (formatted_time, self.deducted_amount, self.user_data['username'], self.user_data['id_number'], "Active"))
                connection.commit()

                time.sleep(1)

            except mysql.connector.Error as err:
                print(f"Error while updating rental time and deducted amount: {err}")

    def update_scooter_menu(self, selected_station):
        active_rentals = self.get_active_rentals()
        
        scooters = self.sections.get(selected_station, [])
        
        available_scooters = [scooter.value for scooter in scooters if scooter.value not in active_rentals]

        print(active_rentals)

        if available_scooters:
            self.scooter_var.set(available_scooters[0])
        else:
            self.scooter_var.set("")

        self.scooter_menu.configure(values=available_scooters)

    def get_active_rentals(self):
        active_rentals = []
        try:
            mycursor = connection.cursor(dictionary=True)
            query = """
            SELECT escoot_id FROM rental_history WHERE user_status = 'Active'
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            active_rentals = [row['escoot_id'] for row in result]
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Database Error", f"Error: {err}")
        return active_rentals

    def display_active_rentals(self):
        print("Active Rentals:", self.active_rentals)

    def refresh_scooter_menu(self):
        if hasattr(self, "selected_station") and self.selected_station.get():
            selected_station = self.selected_station.get()
            if selected_station in self.sections:
                self.update_scooter_menu(selected_station)

    def on_station_change(self, *args):
        selected_station = self.selected_station.get()
        if selected_station in self.sections:
            self.refresh_scooter_menu()

    def monitor_active_rentals(self):
        selected_station = self.selected_station.get() if hasattr(self, "selected_station") else None
        if selected_station and selected_station in self.sections:
            self.update_scooter_menu(selected_station)
        self.master.after(1, self.monitor_active_rentals)

    def load_active_rentals(self):
        self.active_rentals = self.get_active_rentals()

    def update_rental_history(self, deducted_amount, user_time):
        try:
            update_query = """
            UPDATE rental_history
            SET deducted_amount = %s, user_time = %s
            WHERE username = %s AND escoot_id = %s AND user_status = 'Active'
            """
            mycursor.execute(update_query, (deducted_amount, user_time, self.user_data['username'], self.scooter_var.get()))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating rental history: {err}")
            messagebox.showerror("Database Error", f"Error updating rental history: {err}")

    def update_user_label(self, selected_scooter):
        scooter_ids = selected_scooter if selected_scooter else 'N/A'
        if hasattr(self, 'user') and self.user:
            self.user.configure(text=f"User: {self.user_data.get('username', 'N/A')} | ID: {self.user_data.get('id_number', 'N/A')} | Scooter: {scooter_ids}")
        else:
            self.user = customtkinter.CTkLabel(
                self.info_frame,
                text=f"User: {self.user_data.get('username', 'N/A')} | ID: {self.user_data.get('id_number', 'N/A')} | Scooter: {scooter_ids}",
                font=("Microsoft YaHei UI light", 14),
                text_color="#333333"
            )
            self.user.pack(pady=5)

    
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = Main_Page(root,user_data={"username": "test_user"})
    root.mainloop()