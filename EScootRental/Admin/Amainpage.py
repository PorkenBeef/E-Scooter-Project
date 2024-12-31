import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_pool import get_connection
from enum import Enum   


class AdminApp:
    class Pic(Enum):
        Admin = "Admin_pic/Admin.png"
        JERFEL = "Admin_pic/Jerfel.png"
        GIL = "Admin_pic/Gil.jpg"
        NANITO = "Admin_pic/Nanito.jpg"

    def __init__(self, myresult):
        self.admin_data = myresult
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("green")

        self.app = customtkinter.CTk()
        self.app.title("Admin")
        self.app.geometry("1500x800")
        self.app.resizable(False, False)    

        self.setup_frames()
        self.setup_buttons()
        self.admin_frame()
        self.app.mainloop()
        print(self.admin_data)

    def setup_frames(self):
        self.Admin_photo = customtkinter.CTkFrame(master=self.app, height= 300, width=300, corner_radius=8, bg_color="white")
        self.Admin_photo.place(x=17, y=15)
        self.admin_pic()

        self.Main_Frame = customtkinter.CTkFrame(master=self.app, height=770, width=1130, corner_radius=8)
        self.Main_Frame.place(x=350, y=15)

        self.Buttons_Frame = customtkinter.CTkFrame(master=self.app, height=415, width=340, corner_radius=8)
        self.Buttons_Frame.place(x=15, y=365)
    
    def admin_pic(self):
        username_to_pic = {
            "Admin": self.Pic.Admin.value,
            "Jerfel": self.Pic.JERFEL.value,
            "Gil": self.Pic.GIL.value,
            "Nanito": self.Pic.NANITO.value
        }

        username = self.admin_data.get("Username")
        image_path = username_to_pic.get(username, None)

        if image_path:
            try:
                image = Image.open(image_path)
                resized_image = image.resize((300, 320))
                user_photo = ImageTk.PhotoImage(resized_image)

                img_label = customtkinter.CTkLabel(master=self.Admin_photo, image=user_photo, text="", bg_color="white")
                img_label.image = user_photo
                img_label.grid(padx=10, pady=10)
            except FileNotFoundError:
                print(f"Error: File not found at {image_path}")
        else:
            print(f"No image mapped for username: {username}")

    def admin_frame(self):
        Ad_frame = customtkinter.CTkFrame(master=self.app, height=130, width=340)
        Ad_frame.place(x=5, y=650)

        Ad_label = customtkinter.CTkLabel(master=Ad_frame, text=f"Welcome to the Admin Dashboard, {self.admin_data['Username']}!"
                                        "\n\n We're glad to have you here to manage and oversee"
                                        "\n the application efficiently.", font=("Arial", 13))
        Ad_label.grid(padx=20, pady=35)

    def setup_buttons(self):
        self.UserInfo = customtkinter.CTkButton(master=self.Buttons_Frame, text='User Info', fg_color='black', bg_color='white', command=self.UserI)
        self.UserInfo.pack(padx=90, pady=20)

        self.Analytic = customtkinter.CTkButton(master=self.Buttons_Frame, text='Dasboard', fg_color='black', bg_color='white', command=self.Stats)
        self.Analytic.pack(padx=90, pady=20)

        self.Income = customtkinter.CTkButton(master=self.Buttons_Frame, text='Active Rental', fg_color='black', bg_color='white', command=self.Scoot_Activity)
        self.Income.pack(padx=90, pady=20)

        self.Log_out_Button = customtkinter.CTkButton(master=self.Buttons_Frame, text='Logout', fg_color='black', bg_color='white', command=self.LogOut)
        self.Log_out_Button.pack(padx=90, pady=20)

    def clear_data_frame(self):
        for widget in self.Main_Frame.winfo_children():
            widget.destroy()

    def UserI(self):
        self.clear_data_frame()

        def fetch_users_from_db():
            try:
                connection = get_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM useracc")
                users = cursor.fetchall()
                return users
            except Exception as e:
                tkinter.messagebox.showerror("Database Error", f"Error: {e}")
                return []
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        def add_balance_to_user(user_id):
            def add_balance():
                try:
                    balance_to_add = tkinter.simpledialog.askfloat("Add Balance", "Enter amount to add:")
                    if balance_to_add is None:
                        return

                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute("UPDATE useracc SET balance = balance + %s WHERE id_number = %s", (balance_to_add, user_id))
                    connection.commit()
                    tkinter.messagebox.showinfo("Success", f"Added PHP {balance_to_add} to the user's account.")
                    refresh_user_list()
                except Exception as e:
                    tkinter.messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

            return add_balance

        def delete_user_account(user_id):
            def delete_account():
                confirm = tkinter.messagebox.askyesno("Delete Account", "Are you sure you want to delete this account?")
                if not confirm:
                    return
        
                try:
                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM useracc WHERE id_number = %s", (user_id,))
                    connection.commit()
                    tkinter.messagebox.showinfo("Success", "User account deleted successfully.")
                    refresh_user_list()
                except Exception as e:
                    tkinter.messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

            return delete_account

        def populate_scrollable_frame(scrollable_frame, filter_text=""):
            users = fetch_users_from_db()
            if not users:
                tkinter.messagebox.showinfo("No Data", "No users found in the database.")
                return

            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            filtered_users = [user for user in users if filter_text.lower() in user['username'].lower()]
            if not filtered_users:
                no_results_label = customtkinter.CTkLabel(scrollable_frame, text="No users match the search criteria.")
                no_results_label.pack(pady=10)
                return

            for i, user in enumerate(filtered_users):
                user_info = f"{i + 1}. Username: {user['username']} | Phone: {user['phone']} | ID: {user['id_number']} | Balance: PHP {user['Balance']:.2f}"
                user_label = customtkinter.CTkLabel(scrollable_frame, text=user_info, font=("Arial", 20), anchor="w")
                user_label.pack(fill="x", pady=5, padx=10)

                button_frame = customtkinter.CTkFrame(scrollable_frame)
                button_frame.pack(pady=5, padx=10, fill="x")

                add_balance_button = customtkinter.CTkButton(
                    button_frame, text="Add Balance", font=("Arial", 15), command=add_balance_to_user(user["id_number"])
                )
                add_balance_button.pack(side="left", padx=5)

                delete_account_button = customtkinter.CTkButton(
                    button_frame, text="Delete Account", font=("Arial", 15), command=delete_user_account(user["id_number"])
                )
                delete_account_button.pack(side="left", padx=5)

        def refresh_user_list():
            populate_scrollable_frame(scrollable_frame, search_entry.get())

        search_frame = customtkinter.CTkFrame(master=self.Main_Frame, corner_radius=8)
        search_frame.pack(padx=20, pady=(20, 10), fill="x")

        search_label = customtkinter.CTkLabel(search_frame, text="Search Username:", font=("Arial", 14))
        search_label.pack(side="left", padx=5)

        search_entry = customtkinter.CTkEntry(search_frame, font=("Arial", 14), placeholder_text="Enter username")
        search_entry.pack(side="left", padx=5, fill="x", expand=True)

        search_button = customtkinter.CTkButton(search_frame, text="Search", font=("Arial", 14), command=refresh_user_list)
        search_button.pack(side="right", padx=5)

        scrollable_frame = customtkinter.CTkScrollableFrame(master=self.Main_Frame, height=700, width=1050, corner_radius=10)
        scrollable_frame.pack(padx=20, pady=(10, 20), fill="both", expand=True)
        refresh_user_list()


    def Stats(self):
        self.clear_data_frame()

        canvas = tkinter.Canvas(self.Main_Frame, height=770, width=1130, bg="black")
        scrollable_frame = customtkinter.CTkFrame(canvas, height=770, width=1130, corner_radius=8)

        scrollbar = tkinter.Scrollbar(self.Main_Frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        data = self.fetch_rental_history_data()
        if not data:
            tkinter.messagebox.showerror("Error", "Unable to fetch rental history data.")
            return

        users_by_month = data["users_by_month"]
        most_frequent_scooters = data["most_frequent_scooters"]
        monthly_income = data["monthly_income"]

        months = list(users_by_month.keys())
        unique_users = [len(users) for users in users_by_month.values()]
        scooter_ids = [scooter[0] for scooter in most_frequent_scooters[:5]]
        scooter_rentals = [scooter[1] for scooter in most_frequent_scooters[:5]]

        operational_costs = 42500
        monthly_profit = [income - operational_costs for income in monthly_income.values()]

        total_income = sum(monthly_income.values())
        total_profit = sum(monthly_profit)
        desired_monthly_income = 42500  # Example desired income
        income_percentage = abs((total_income / (desired_monthly_income * 12)) * 100)

        monthly_desired_percentages = [
            abs((income / desired_monthly_income) * 100) for income in monthly_income.values()
        ]

        graph_frame = tkinter.Frame(scrollable_frame, bg="black")
        graph_frame.pack(fill=tkinter.BOTH, expand=True, pady=30, padx=10)

        self.create_graph(graph_frame, "bar", months, unique_users, "Unique Users by Month", "Months", "Unique Users", 0, 0)
        self.create_graph(graph_frame, "bar", scooter_ids, scooter_rentals, "Top 5 Frequent Scooters", "Scooter IDs", "Rentals", 0, 1)
        self.create_graph(graph_frame, "line", months, list(monthly_income.values()), "Monthly Income", "Months", "Income (PHP)", 1, 0)
        self.create_graph(graph_frame, "line", months, monthly_profit, "Monthly Profit", "Months", "Profit (PHP)", 1, 1)
        self.create_graph(graph_frame, "pie", scooter_ids, scooter_rentals, "Scooter Usage Distribution", "", "", 2, 0, colspan=2)

        tkinter.Label(scrollable_frame, text="Financial Summary", font=("Arial", 14, "bold"), bg="gray").pack(pady=10)
        tkinter.Label(scrollable_frame, text=f"Income Percentage to Desired Income: {income_percentage:.2f}%", font=("Arial", 12), bg="gray").pack(pady=10)
        tkinter.Label(scrollable_frame, text=f"Total Income: PHP {total_income:,.2f}", font=("Arial", 12), bg="gray").pack(pady=10)

        for month, percentage in zip(months, monthly_desired_percentages):
            tkinter.Label(scrollable_frame, text=f"{month}: {percentage:.2f}% of Desired Income", font=("Arial", 12), bg="gray").pack(pady=10)

        tkinter.Label(scrollable_frame, text=f"Desired Monthly Income: PHP {desired_monthly_income:,.2f}", font=("Arial", 12), bg="gray").pack(pady=10)

    def create_graph(self, frame, graph_type, x_data, y_data, title, x_label, y_label, row, col, colspan=1):
        fig, ax = plt.subplots(figsize=(5, 3))

        if graph_type == "bar":
            ax.bar(x_data, y_data, color='skyblue', edgecolor='black')
        elif graph_type == "line":
            ax.plot(x_data, y_data, marker='o', color='green', linestyle='-', linewidth=2, markersize=6)
        elif graph_type == "pie":
            ax.pie(y_data, labels=x_data, autopct='%1.1f%%', colors=plt.cm.Paired.colors)

        ax.set_title(title, fontsize=12)
        if graph_type != "pie":
            ax.set_xlabel(x_label, fontsize=10)
            ax.set_ylabel(y_label, fontsize=10)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=row, column=col, padx=30, pady=10, columnspan=colspan)
        canvas.draw()

    def fetch_rental_history_data(self):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT username, rental_date, escoot_id, 
                    user_time, deducted_amount
                FROM rental_history
            """
            cursor.execute(query)
            rental_history = cursor.fetchall()

            users_by_month = {}
            scooter_usage = {}
            monthly_income = {}

            for record in rental_history:
                username = record['username']
                rental_date = record['rental_date']
                scooter_id = record['escoot_id']
                rental_time = record['user_time']
                deducted_amount = record['deducted_amount']

                time_parts = rental_time.split(' ')
                total_seconds = 0
                if 'minute' in time_parts[0]:
                    total_seconds += int(time_parts[0]) * 60
                if 'second' in time_parts:
                    total_seconds += int(time_parts[2])

                month = rental_date.strftime('%B')
                if month not in users_by_month:
                    users_by_month[month] = set()
                users_by_month[month].add(username)

                if month not in monthly_income:
                    monthly_income[month] = 0
                monthly_income[month] += deducted_amount

                if scooter_id not in scooter_usage:
                    scooter_usage[scooter_id] = 0
                scooter_usage[scooter_id] += 1

            most_frequent_scooters = sorted(scooter_usage.items(), key=lambda x: x[1], reverse=True)
            return {
                "users_by_month": users_by_month,
                "most_frequent_scooters": most_frequent_scooters,
                "monthly_income": monthly_income
            }

        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to fetch rental history: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def Scoot_Activity(self):
        self.clear_data_frame()

        def fetch_active_scooters():
            try:
                connection = get_connection()
                cursor = connection.cursor(dictionary=True)
                # Fetch active scooters along with their usernames
                query = """
                    SELECT username, escoot_id 
                    FROM rental_history 
                    WHERE user_status = 'Active'
                """
                cursor.execute(query)
                scooters = cursor.fetchall()
                return scooters
            except Exception as e:
                tkinter.messagebox.showerror("Database Error", f"Error: {e}")
                return []
            finally:
                if connection and connection.is_connected():
                    cursor.close()
                    connection.close()

        def deactivate_scooter(escoot_id):
            def deactivate():
                try:
                    confirmation = tkinter.messagebox.askyesno("Confirm", "Are you sure you want to deactivate this scooter?")
                    if not confirmation:
                        return

                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute("UPDATE rental_history SET user_status = 'Inactive' WHERE escoot_id = %s", (escoot_id,))
                    connection.commit()
                    tkinter.messagebox.showinfo("Success", f"Scooter ID {escoot_id} has been deactivated.")
                    refresh_scooter_list()
                except Exception as e:
                    tkinter.messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    if connection and connection.is_connected():
                        cursor.close()
                        connection.close()

            return deactivate

        def populate_scrollable_frame(scrollable_frame, filter_text=""):
            scooters = fetch_active_scooters()
            if not scooters:
                return

            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            filtered_scooters = [scooter for scooter in scooters if filter_text.lower() in scooter['username'].lower()]
            if not filtered_scooters:
                no_results_label = customtkinter.CTkLabel(scrollable_frame, text="No scooters match the search criteria.")
                no_results_label.pack(pady=10)
                return

            for i, scooter in enumerate(filtered_scooters):
                scooter_info = f"{i + 1}. Username: {scooter['username']} | Scooter ID: {scooter['escoot_id']}"
                scooter_label = customtkinter.CTkLabel(scrollable_frame, text=scooter_info, font=("Arial", 14), anchor="w")
                scooter_label.pack(fill="x", pady=5, padx=10)

                deactivate_button = customtkinter.CTkButton(
                    scrollable_frame,
                    text="Deactivate",
                    font=("Arial", 12),
                    command=deactivate_scooter(scooter["escoot_id"])
                )
                deactivate_button.pack(pady=5)

        def refresh_scooter_list():
            populate_scrollable_frame(scrollable_frame, search_entry.get())

        search_entry = customtkinter.CTkEntry(self.Main_Frame, placeholder_text="Search by username...")
        search_entry.pack(fill="x", padx=10, pady=5)
        search_entry.bind("<KeyRelease>", lambda event: refresh_scooter_list())

        scrollable_frame = customtkinter.CTkScrollableFrame(self.Main_Frame, height=700, width=1050,)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        refresh_scooter_list()

    def LogOut(self):
        if tkinter.messagebox.askokcancel("Logout", "Are you sure you want to logout?"):
            self.app.quit()
            self.app.destroy()

if __name__ == "__main__":
    admin_data = {'Username': 'Gil'}  
    AdminApp(admin_data)
