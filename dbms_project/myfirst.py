import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta 
import pandas as pd
from PIL import Image, ImageTk
from for_connect import create_connection
import re
from tkcalendar import Calendar
from tkinter import Toplevel, Label, Frame, Listbox, Entry, Button
#from logini import  show_login_frame

def show_login_frame():
    # Clear existing widgets
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Ensure the frame is properly sized before setting the background image
    login_frame.update_idletasks()

    # Load and set the background image only once and ensure it is correctly updated
    bg_image_path = r"C:\Users\HP\Desktop\5th SEM\DBMS\dbms_project\3d-gym-equipment.jpg"
    
    # Resize and load the image again when revisiting
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((login_frame.winfo_width(), login_frame.winfo_height()))  # Resize to fit frame
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to hold the image as background
    bg_label = tk.Label(login_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the entire frame

    # Keep reference to bg_photo to avoid garbage collection
    bg_label.image = bg_photo

    # Enlarged "Login" label with triple the font size
    login_label = tk.Label(
        login_frame, 
        text="WELCOME to Gym Management System !",
        font=("Arial", 40, "bold"),  # Triple the size
        bg="black",  # Set background to black
        fg="white",  # Set text color to white
        #anchor="w",  # Align to the left
    )
    login_label.pack(pady=30, anchor="w", padx=40)

    # Enlarged Username label with improved color
    username_label = tk.Label(
        login_frame,
        text="Username:",
        bg="black",  # Set background to black
        fg="white",  # Set text color to white
        font=("Helvetica", 24, "bold"),  # Double font size
        anchor="w",  # Align to the left
    )
    username_label.pack(pady=15, anchor="w", padx=40)

    username_entry = tk.Entry(
        login_frame,
        relief="solid",
        font=("Helvetica", 24),  # Double font size
        width=20,  # Doubling the width
        bg="#E6E6FA",  # Light background color for input field
        fg="#333333",  # Dark text for readability
        borderwidth=2  # Border for better focus visibility
    )
    username_entry.pack(pady=15, ipadx=10, ipady=5, anchor="w", padx=40)  # Adjusted padding for larger entry

    # Enlarged Password label with improved color
    password_label = tk.Label(
        login_frame, 
        text="Password:", 
        bg="black",  # Set background to black
        fg="white",  # Set text color to white
        font=("Helvetica", 24, "bold"),  # Bold and double font size
        anchor="w",  # Align to the left
    )
    password_label.pack(pady=15, anchor="w", padx=40)

    password_entry = tk.Entry(
        login_frame, 
        show='*', 
        relief="solid",
        font=("Helvetica", 24),  # Double font size
        width=20,
        bg="#E6E6FA",  # Light background color for input field
        fg="#333333",  # Dark text for readability
        borderwidth=2  # Border for better focus visibility
    )
    password_entry.pack(pady=15, ipadx=10, ipady=5, anchor="w", padx=40)

    # Enlarged Login button
    login_button = tk.Button(
        login_frame, 
        text="Login", 
        command=lambda: login_user(username_entry.get(), password_entry.get()),
        bg="black",  # Set background to dark black
        fg="white",  # Set text color to white
        font=("Arial", 24, "bold"),  # Double font size
        relief="flat", 
        padx=20, pady=10  # Doubled padding
    )
    login_button.pack(pady=30, anchor="w", padx=40)

    # Enlarged Register button
    register_button = tk.Button(
        login_frame, 
        text="Don't have an account? Register", 
        command=show_register_frame, 
        bg="black",  # Set background to dark black
        fg="white",  # Set text color to white
        font=("Arial", 20, "bold"),  # Double font size
        relief="flat", 
        padx=10, pady=10  # Increased padding
    )
    register_button.pack(pady=15, anchor="w", padx=40)

    # Button to ask if the user is a trainer
    trainer_button = tk.Button(
        login_frame, 
        text="Are you a Trainer?", 
        command=show_trainer_login_form,
        bg="black",  # Set background to dark black
        fg="white",  # Set text color to white
        font=("Arial", 20, "bold"),  # Bold and double font size
        relief="flat", 
        padx=10, pady=10
    )
    trainer_button.pack(pady=15, anchor="w", padx=40)


def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Login WHERE Username = %s AND Password = %s", (username, password))
    result = cursor.fetchone()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Show admin dashboard or privileged functions
        show_admin_dashboard()
    elif result:
        login_id = result[0]  # Assuming Login_ID is at index 0
        client_id = get_client_id(login_id)  # Check if it's a client
        trainer_id = get_trainer_id(login_id)  # Check if it's a trainer

        # If it's a trainer, redirect to trainer's page
        if trainer_id:
            messagebox.showinfo("Trainer Login", "Welcome Trainer. Redirecting to your page.")
            show_trainer_page(trainer_id)
        elif client_id:
            # If it's a client, check membership status
            membership_end_date = check_membership(client_id)
            if membership_end_date:
                if membership_end_date < datetime.now().date():
                    messagebox.showinfo("Membership Status", "Your membership has expired. Please choose a workout type to proceed.")
                    show_workout_type_selection(client_id)
                else:
                    messagebox.showinfo("Login Success", "Login successful. Opening client dashboard.")
                    open_main_page(login_id)
            else:
                # No membership exists for the client
                messagebox.showinfo("No Membership", "You don't have an active membership. Please choose a workout type to proceed.")
                show_workout_type_selection(client_id)
        else:
            messagebox.showerror("Login Error", "Incorrect username or password.")
    else:
        messagebox.showerror("Login Error", "Incorrect username or password.")
    
    cursor.close()
    conn.close()



def check_membership(client_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EndDate FROM Membership WHERE Client_ID = %s", (client_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def register_user(username, password, phone, email):
    # Check if any field is empty
    if not username or not password or not phone or not email:
        messagebox.showerror("Error", "All fields are mandatory. Please fill all fields.")
        return False, "All fields are mandatory. Please fill all fields."
    
    
    # Validate the phone number
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Phone number must be 10 digits and contain only numbers.")
        return False, "Phone number must be 10 digits and contain only numbers."

    
    # Validate the email
    if not re.match(r"[^@]+@gmail\.com$", email):
        messagebox.showerror("Invalid Email")

        return False, "INVALID EMAIL"
    
    # Validate the password
    if len(password) < 8:
        messagebox.showerror("Error", "INVALID EMAIL")
        return False, "Password must be at least 8 characters long."
    
    # If validations pass, proceed with the database insertion
    conn = create_connection()
    cursor = conn.cursor()
    
    # Check if the username already exists
    cursor.execute("SELECT * FROM Login WHERE Username = %s", (username,))
    if cursor.fetchone():
        messagebox.showerror("User already exists, Please log in")
        return False, "User already exists. Please log in."
    
    # Insert new user into Login table
    cursor.execute("INSERT INTO Login (Username, Password) VALUES (%s, %s)", (username, password))
    login_id = cursor.lastrowid  # Get the last inserted Login_ID
    
    # Insert user details into Client table
    cursor.execute("INSERT INTO Client (Name, Contact, Email, Login_ID) VALUES (%s, %s, %s, %s)",
                   (username, phone, email, login_id))  # Use the provided phone and email
    
    messagebox.showinfo("Sucess","user registered successfully")
    conn.commit()
    cursor.close()
    conn.close()
    
    # Show the login frame after successful registration
    
    show_login_frame()
    
    # Return success
    
    return True, "User registered successfully."


def get_client_id(login_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Client_ID FROM Client WHERE Login_ID = %s", (login_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def show_workout_type_selection(client_id):
    for widget in login_frame.winfo_children():
        widget.destroy()
        bg_image_path = r"C:\Users\HP\Desktop\5th SEM\DBMS\dbms_project\3d-gym-workouttype.webp"
    
# Resize and load the image again when revisiting
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((login_frame.winfo_width(), login_frame.winfo_height()))  # Resize to fit frame
    bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the image as background
    bg_label = tk.Label(login_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the entire frame

# Keep reference to bg_photo to avoid garbage collection
    bg_label.image = bg_photo


    workout_types = {
        'Gym': 1000,
        'Zumba': 800,
        'Yoga': 750,
        'Aero': 800
    }

    workout_label = tk.Label(login_frame, text="Choose Workout Type:", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333333")
    workout_label.pack(pady=20)

    selected_workout = tk.StringVar()

    # Create a frame to contain radio buttons and center them
    workout_frame = tk.Frame(login_frame, bg="#f5f5f5")
    workout_frame.pack(pady=20)

    # Create radio buttons for each workout type and make them bigger
    for workout, price in workout_types.items():
        radio_button = tk.Radiobutton(workout_frame, 
                                      text=f"{workout} - ₹{price}", 
                                      variable=selected_workout, 
                                      value=workout, 
                                      font=("Arial", 18),  # Increase font size
                                      bg="#f5f5f5", 
                                      fg="#333333", 
                                      anchor="w",  # Align text to the left
                                      width=20)  # Increase width to make radio button bigger
        radio_button.pack(pady=10, anchor="w")  # Adds some padding and ensures text aligns to left

    duration_label = tk.Label(login_frame, text="Duration (in months):", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333333")
    duration_label.pack(pady=10)

    duration_entry = tk.Entry(login_frame, relief="solid", font=("Arial", 18), width=15)  # Bigger font for the entry
    duration_entry.pack(pady=10)

    upi_label =tk.Label(login_frame, text="Enter Your Upi ID ",font=("Arial",18,"bold"),bg="#f5f5f5",fg="#333333")
    upi_label.pack(pady=10)
    
    upi_entry=tk.Entry(login_frame, relief="solid",font=("Arial", 18), width=15)
    upi_entry.pack(pady=10)


    # Center the payment button and make it bigger
    payment_button = tk.Button(login_frame, 
                               text="Proceed to Payment", 
                               command=lambda: process_payment(selected_workout.get(), duration_entry.get(),upi_entry.get(), client_id),
                               bg="#4caf50", 
                               fg="white", 
                               font=("Arial", 16, "bold"), 
                               relief="flat", 
                               padx=20, pady=10)
    payment_button.pack(pady=30)
def show_trainer_page(trainer):
    import tkinter as tk
    from tkinter import messagebox
    
    trainer_id = trainer[0]  # Assuming first column is trainer ID
    expertise = trainer[2]
    
    # Create a new window for the trainer's page
    trainer_page = tk.Toplevel()
    trainer_page.title(f"{trainer[1]}'s Page")  # Trainer name
    trainer_page.config(bg="#000000")  # Blackest background
    
    # Create a frame with black background
    frame = tk.Frame(trainer_page, bg="#000000")  # Black background
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Create a frame for the main content area (trainer name & expertise)
    main_frame = tk.Frame(frame, bg="#000000")
    main_frame.pack(anchor="n", pady=10)
    
    # Display trainer information with larger font and white text color
    tk.Label(main_frame, text=f"Trainer Name: {trainer[1]}", font=("Arial", 48), bg="#000000", fg="#FFFFFF", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Label(main_frame, text=f"Expertise: {expertise}", font=("Arial", 36), bg="#000000", fg="#FFFFFF", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    # Establish database connection to fetch schedules and clients
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Error", "Unable to connect to the database!")
        return

    # Create a cursor object
    cursor = conn.cursor()

    # Create a frame for the schedule and client table
    schedule_frame = tk.Frame(frame, bg="#000000")
    schedule_frame.pack(fill="x", padx=20, pady=10)

    # Fetch and display the schedule for the trainer
    cursor.execute("""
        SELECT S.Date, S.Time 
        FROM Schedule S 
        INNER JOIN Trainer_Schedule TS ON S.Schedule_ID = TS.Schedule_ID 
        WHERE TS.Trainer_ID = %s
    """, (trainer_id,))
    schedules = cursor.fetchall()

    # Fetch and display clients associated with the trainer
    cursor.execute("""
        SELECT DISTINCT C.Name 
        FROM Client C 
        INNER JOIN Client_Workout_Type CW ON C.Client_ID = CW.Client_ID 
        INNER JOIN Trainer_Workout_Type TW ON CW.Workout_Type_ID = TW.Workout_Type_ID 
        WHERE TW.Trainer_ID = %s
    """, (trainer_id,))
    clients = cursor.fetchall()
    
    # If both schedules and clients are available, display them side-by-side
    if schedules or clients:
        # Create a table-like structure for displaying schedules and clients side-by-side
        table_frame = tk.Frame(schedule_frame, bg="#000000")
        table_frame.pack(fill="x", padx=20, pady=10)

        # Table headers with larger font
        tk.Label(table_frame, text="Schedule", font=("Arial", 32), bg="#333333", fg="#FFFFFF", relief="solid", width=25, anchor="center").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(table_frame, text="Clients", font=("Arial", 32), bg="#333333", fg="#FFFFFF", relief="solid", width=25, anchor="center").grid(row=0, column=1, padx=5, pady=5)
        
        # Display the schedules and clients
        for i, (schedule, client) in enumerate(zip(schedules, clients), 1):
            tk.Label(table_frame, text=f"{schedule[0]} at {schedule[1]}", font=("Arial", 28), bg="#444444", fg="#FFFFFF", relief="solid", anchor="w", width=25).grid(row=i, column=0, padx=5, pady=5)
            tk.Label(table_frame, text=client[0], font=("Arial", 28), bg="#444444", fg="#FFFFFF", relief="solid", anchor="w", width=25).grid(row=i, column=1, padx=5, pady=5)

        # If schedules or clients are missing, show respective labels
        if not schedules:
            tk.Label(table_frame, text="No schedules available", font=("Arial", 28), bg="#444444", fg="#FFFFFF", relief="solid", width=25, anchor="center").grid(row=1, column=0, padx=5, pady=5)
        if not clients:
            tk.Label(table_frame, text="No clients assigned", font=("Arial", 28), bg="#444444", fg="#FFFFFF", relief="solid", width=25, anchor="center").grid(row=1, column=1, padx=5, pady=5)
    else:
        tk.Label(frame, text="No schedules or clients available", font=("Arial", 28), bg="#000000", fg="#FFFFFF").grid(row=2, column=0, pady=10)

    # Close the cursor and connection after use
    cursor.close()
    conn.close()


def process_payment(workout_type, duration, upi, client_id):
    if workout_type == '':
        messagebox.showerror("Payment Error", "Please select a workout type.")
        return

    try:
        duration = int(duration)
        if duration < 1:
            raise ValueError("Duration must be at least 1 month.")
    except ValueError:
        messagebox.showerror("Payment Error", "Please enter a valid duration.")
        return

    payment_amounts = {'Gym': 1000, 'Zumba': 800, 'Yoga': 750, 'Aero': 800}
    total_amount = payment_amounts[workout_type] * duration
    
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if Client_ID exists
        cursor.execute("SELECT Client_ID FROM Client WHERE Client_ID = %s", (client_id,))
        if not cursor.fetchone():
            raise ValueError("Client does not exist.")

        # Insert payment information
        cursor.execute("""
            INSERT INTO Payment (Amount, Date, Client_ID, UPI_ID) 
            VALUES (%s, %s, %s, %s)
        """, (total_amount, datetime.now().date(), client_id, upi))
        payment_id = cursor.lastrowid
        
        # Insert membership information
        cursor.execute("""
            INSERT INTO Membership (Type, StartDate, EndDate, Client_ID) 
            VALUES (%s, %s, %s, %s)
        """, (workout_type, datetime.now().date(), 
              datetime.now().date() + relativedelta(months=duration), client_id))
        
        # First, get or create the workout type ID
        cursor.execute("SELECT Workout_Type_ID FROM Workout_Type WHERE Type = %s", (workout_type,))
        result = cursor.fetchone()
        
        if result:
            workout_type_id = result[0]
        else:
            # Insert new workout type if it doesn't exist
            cursor.execute("INSERT INTO Workout_Type (Type) VALUES (%s)", (workout_type,))
            workout_type_id = cursor.lastrowid
        
        # Now insert into Client_Workout_Type table
        cursor.execute("""
            INSERT INTO Client_Workout_Type (Client_ID, Workout_Type_ID)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE Workout_Type_ID = VALUES(Workout_Type_ID)
        """, (client_id, workout_type_id))
        cursor.execute(""" INSERT INTO transaction_record (description,payment_id,date) values (%s,%s,NOW())""",(workout_type,payment_id))
        
        # No need to call conn.begin(), just commit the transaction
        conn.commit()
        messagebox.showinfo("Payment Success", 
                          f"Payment of ₹{total_amount} successful. Membership activated for {duration} months.")
        
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"{str(e)}")
    finally:
        cursor.close()
        conn.close()
        show_login_frame()


def open_main_page(login_id):
    # Fetch the Client_ID or Trainer_ID based on the Login_ID
    client_id = get_client_id(login_id)
    trainer_id = get_trainer_id(login_id)
    
    # Assuming you are using tkinter and show_login_frame is a function defined elsewhere in your code.

    login_button = tk.Button(
        login_frame, 
        text="Login page", 
        command=show_login_frame,  # Function to call when button is clicked
        bg="black",  # Set background color to black
        fg="white",  # Set text color to white
        font=("Arial", 14, "bold"),  # Set font style
        relief="flat",  # Button style
        padx=10,  # Horizontal padding
        pady=5  # Vertical padding
    )

    login_button.pack(pady=20)  # Add button to the frame with some padding


    if not client_id and not trainer_id:
        messagebox.showerror("Login Error", "No client or trainer found with this login.")
        
        return

    for widget in login_frame.winfo_children():
        widget.destroy()

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Display Client or Trainer Information
        if client_id:
            # Fetch client details along with their schedules and trainer details
            cursor.execute("""
                SELECT c.Name, cs.Schedule_ID, s.Date, s.Time, t.Name AS Trainer_Name 
                FROM Client c
                JOIN Client_Schedule cs ON c.Client_ID = cs.Client_ID
                JOIN Schedule s ON cs.Schedule_ID = s.Schedule_ID
                JOIN Trainer_Schedule ts ON s.Schedule_ID = ts.Schedule_ID
                JOIN Trainer t ON ts.Trainer_ID = t.Trainer_ID
                WHERE c.Client_ID = %s
            """, (client_id,))

            schedules = cursor.fetchall()

            # Check if schedules are found for the client
            if not schedules:
                messagebox.showinfo("No Schedules", "No schedules found for the client.")
                conn.close()
                return

            # Set up the main page layout
            main_label = tk.Label(login_frame, text="Welcome to the Gym Management System!", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#333333")
            main_label.pack(pady=20)

            # Display client name
            client_name_label = tk.Label(login_frame, text=f"Client: {schedules[0][0]}", font=("Arial", 16), bg="#f5f5f5", fg="#333333")
            client_name_label.pack(pady=10)

            # Display schedules
            schedule_frame = tk.Frame(login_frame, bg="#f5f5f5")
            schedule_frame.pack(pady=10)

            for schedule in schedules:
                schedule_label = tk.Label(schedule_frame, text=f"Schedule Date: {schedule[2]}, Time: {schedule[3]}, Trainer: {schedule[4]}", font=("Arial", 14), bg="#f5f5f5", fg="#333333")
                schedule_label.pack(pady=5)

        elif trainer_id:
            # Fetch trainer details and their schedules
            cursor.execute("""
                SELECT t.Name AS Trainer_Name, ts.Schedule_ID, s.Date, s.Time, c.Name AS Client_Name
                FROM Trainer t
                JOIN Trainer_Schedule ts ON t.Trainer_ID = ts.Trainer_ID
                JOIN Schedule s ON ts.Schedule_ID = s.Schedule_ID
                JOIN Client_Schedule cs ON s.Schedule_ID = cs.Schedule_ID
                JOIN Client c ON cs.Client_ID = c.Client_ID
                WHERE t.Trainer_ID = %s
            """, (trainer_id,))

            schedules = cursor.fetchall()

            # Check if schedules are found for the trainer
            if not schedules:
                messagebox.showinfo("No Schedules", "No schedules found for the trainer.")
                conn.close()
                return

            # Set up the main page layout
            main_label = tk.Label(login_frame, text="Welcome to the Gym Management System!", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#333333")
            main_label.pack(pady=20)

            # Display trainer name
            trainer_name_label = tk.Label(login_frame, text=f"Trainer: {schedules[0][0]}", font=("Arial", 16), bg="#f5f5f5", fg="#333333")
            trainer_name_label.pack(pady=10)

            # Display schedules
            schedule_frame = tk.Frame(login_frame, bg="#f5f5f5")
            schedule_frame.pack(pady=10)

            for schedule in schedules:
                schedule_label = tk.Label(schedule_frame, text=f"Schedule Date: {schedule[2]}, Time: {schedule[3]}, Client: {schedule[4]}", font=("Arial", 14), bg="#f5f5f5", fg="#333333")
                schedule_label.pack(pady=5)

        # Exit button
        exit_button = tk.Button(login_frame, text="Exit", command=root.quit, bg="#ff6b6b", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5)
        exit_button.pack(pady=20)

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_register_frame():
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Set the background image for the register screen
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Ensure the frame is properly sized before setting the background image
    login_frame.update_idletasks()

    # Load and set the background image only once and ensure it is correctly updated

    bg_image_path = r"C:\Users\HP\Desktop\5th SEM\DBMS\dbms_project\3d-gym-trainer.jpg"
    
    # Resize and load the image again when revisiting
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((login_frame.winfo_width(), login_frame.winfo_height()))  # Resize to fit frame
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to hold the image as background
    bg_label = tk.Label(login_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the entire frame

    # Keep reference to bg_photo to avoid garbage collection
    bg_label.image = bg_photo

    # Create the register frame widgets (text, buttons, entries)
    register_label = tk.Label(login_frame, text="Register", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333333")
    register_label.pack(pady=30, anchor="w", padx=40)  # Increased space after the first label

    username_label = tk.Label(login_frame, text="Username:", font=("Arial", 18), bg="#f5f5f5", fg="#333333")
    username_label.pack(pady=5, anchor="w", padx=40)  # Align left with padding
    username_entry = tk.Entry(login_frame, relief="solid", font=("Arial", 18), width=24)  # Reduced width to 60%
    username_entry.pack(pady=10, anchor="w", padx=40)  # Increased space after entry

    password_label = tk.Label(login_frame, text="Password:", font=("Arial", 18), bg="#f5f5f5", fg="#333333")
    password_label.pack(pady=5, anchor="w", padx=40)  # Align left with padding
    password_entry = tk.Entry(login_frame, show='*', relief="solid", font=("Arial", 18), width=24)  # Reduced width to 60%
    password_entry.pack(pady=10, anchor="w", padx=40)  # Increased space after entry

    phone_label = tk.Label(login_frame, text="Phone Number:", font=("Arial", 18), bg="#f5f5f5", fg="#333333")
    phone_label.pack(pady=5, anchor="w", padx=40)  # Align left with padding
    phone_entry = tk.Entry(login_frame, relief="solid", font=("Arial", 18), width=24)  # Reduced width to 60%
    phone_entry.pack(pady=10, anchor="w", padx=40)  # Increased space after entry

    email_label = tk.Label(login_frame, text="Email ID:", font=("Arial", 18), bg="#f5f5f5", fg="#333333")
    email_label.pack(pady=5, anchor="w", padx=40)  # Align left with padding
    email_entry = tk.Entry(login_frame, relief="solid", font=("Arial", 18), width=24)  # Reduced width to 60%
    email_entry.pack(pady=10, anchor="w", padx=40)  # Increased space after entry

    # Register button with updated style (larger size)
    register_button = tk.Button(login_frame, text="Register", command=lambda: register_user(username_entry.get(), password_entry.get(), phone_entry.get(), email_entry.get()), 
                                 bg="black", fg="white", font=("Arial", 20, "bold"), relief="flat", padx=20, pady=15)
    register_button.pack(pady=30, anchor="w", padx=40)  # Increased button size and space after button

    # Login button with updated style (larger size)
    login_button = tk.Button(login_frame, text="Already have an account? Login", command=show_login_frame, 
                             bg="black", fg="white", font=("Arial", 14, "bold"), relief="flat", padx=15, pady=10)
    login_button.pack(pady=10, anchor="w", padx=40)  # Increased button size and space after button


def get_trainer_id(login_id):
    # Assuming you have a method to get the Trainer ID based on Login_ID
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Trainer_ID FROM Trainer WHERE Login_ID = %s", (login_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


ADMIN_USERNAME = "ITACHI_UCHHIA_THE_MAN_THE_MYTH_THE_LEGEND"
ADMIN_PASSWORD = "I_LOVE_YOU_IZUMI"


# Function to validate the login


# Function to display the admin dashboard with edit, delete, update options
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def show_admin_dashboard():
    # Destroy existing widgets to clear the screen
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Set background image
    bg_image_path = r"C:\Users\HP\Desktop\5th SEM\DBMS\dbms_project\3d-gym-admin-dash.jpg"
    bg_image = Image.open(bg_image_path).resize((login_frame.winfo_width(), login_frame.winfo_height()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(login_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo

    # Admin Dashboard title
    admin_label = tk.Label(
        login_frame, text="Admin Dashboard", font=("Arial", 48, "bold"),
        bg="black", fg="white"
    )
    admin_label.pack(anchor="w", padx=30, pady=30)

    # Button configuration for uniform styling
    button_config = {
        "bg": "#ADD8E6", "fg": "blue", "font": ("Arial", 24, "bold"),
        "relief": "flat", "activebackground": "#B0C4DE", "anchor": "w"
    }

    # Buttons for Admin Dashboard
    delete_button = tk.Button(login_frame, text="Delete User", command=delete_user, **button_config)
    delete_button.pack(anchor="w", padx=30, pady=20)

    update_button = tk.Button(login_frame, text="Update User Details", command=update_user_details, **button_config)
    update_button.pack(anchor="w", padx=30, pady=20)

    add_trainer_button = tk.Button(login_frame, text="Add Trainer", command=open_add_trainer_form, **button_config)
    add_trainer_button.pack(anchor="w", padx=30, pady=20)

    assign_schedule_button = tk.Button(login_frame, text="Assign Schedule", command=assign_schedule, **button_config)
    assign_schedule_button.pack(anchor="w", padx=30, pady=20)

    # New button to see transaction records
    view_transactions_button = tk.Button(
        login_frame, text="View Transaction Records", command=view_transaction_records, **button_config
    )
    view_transactions_button.pack(anchor="w", padx=30, pady=20)

    # Button to go back to login page
    go_back_button = tk.Button(
        login_frame, text="Go Back to Login Page", command=show_login_frame, **button_config
    )
    go_back_button.pack(anchor="w", padx=30, pady=20)

def view_transaction_records():
    # Create a new top-level window for transaction records
    transaction_window = tk.Toplevel(login_frame)  # Assuming login_frame is defined
    transaction_window.title("Transaction Records")
    transaction_window.config(bg="#000000")  # Set background to black
    
    # Use grid for layout management inside the window
    transaction_window.grid_rowconfigure(0, weight=0)  # Heading row should not expand
    transaction_window.grid_rowconfigure(1, weight=0)  # Row for table headers
    transaction_window.grid_rowconfigure(2, weight=1)  # Data rows should expand
    transaction_window.grid_columnconfigure(0, weight=1)  # Allow resizing of columns

    # Heading for the transaction records
    tk.Label(transaction_window, text="Transaction Records", font=("Arial", 36, "bold"), bg="#000000", fg="#FFFFFF").grid(row=0, column=0, pady=10, sticky="w")

    # Fetch transaction data from the database
    transactions = fetch_transaction_records()
    
    if not transactions:
        tk.Label(transaction_window, text="No records found.", font=("Arial", 16), bg="#000000", fg="#FFFFFF").grid(row=2, column=0, pady=10)
        return

    # Create a frame to hold the headings and the transaction records in a grid layout
    headings_frame = tk.Frame(transaction_window, bg="#000000")
    headings_frame.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="ew")

    # Display headings with a different background color
    tk.Label(headings_frame, text="Transaction ID", font=("Arial", 20, "bold"), bg="#333333", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(headings_frame, text="Description", font=("Arial", 20, "bold"), bg="#333333", fg="#FFFFFF", relief="solid", width=30, anchor="center").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(headings_frame, text="Date", font=("Arial", 20, "bold"), bg="#333333", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=2, padx=5, pady=5)
    tk.Label(headings_frame, text="Amount", font=("Arial", 20, "bold"), bg="#333333", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=3, padx=5, pady=5)

    # Create a frame to hold the rows of transaction data
    rows_frame = tk.Frame(transaction_window, bg="#000000")
    rows_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

    # Display transaction records in table-like structure
    for idx, record in enumerate(transactions, 1):
        row_frame = tk.Frame(rows_frame, bg="#444444")
        row_frame.grid(row=idx, column=0, padx=20, pady=5, sticky="ew")

        # Display the data in rows
        tk.Label(row_frame, text=record["Transaction_ID"], font=("Arial", 16), bg="#444444", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(row_frame, text=record["Description"], font=("Arial", 16), bg="#444444", fg="#FFFFFF", relief="solid", width=30, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(row_frame, text=record["Date"], font=("Arial", 16), bg="#444444", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(row_frame, text=f"Rs{record['Amount']:.2f}", font=("Arial", 16), bg="#444444", fg="#FFFFFF", relief="solid", width=15, anchor="center").grid(row=0, column=3, padx=5, pady=5)

    # Add a close button to close the transaction window
    close_button = tk.Button(transaction_window, text="Close", command=transaction_window.destroy, font=("Arial", 16), bg="#444444", fg="#FFFFFF")
    close_button.grid(row=len(transactions) + 3, column=0, pady=20, sticky="ew")

    # Ensure that columns are stretched uniformly when window is resized
    transaction_window.grid_columnconfigure(0, weight=1, uniform="equal")

# Assuming login_frame is defined and set up elsewhere in your code
def fetch_transaction_records():
    conn = create_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    query = """
    SELECT tr.Transaction_ID, tr.Description, tr.Date, p.Amount 
    FROM Transaction_Record tr
    JOIN Payment p ON tr.Payment_ID = p.Payment_ID
    """
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    # Return the records as a list of dictionaries
    return [{"Transaction_ID": record[0], "Description": record[1], "Date": record[2], "Amount": record[3]} for record in records]


def populate_client_trainer_listboxes(client_listbox, trainer_combobox):
    conn = create_connection()
    cursor = conn.cursor()

    clients = []
    trainers = []

    try:
        # Fetch clients with workout type, username, and membership duration
        cursor.execute("""
            SELECT c.Client_ID, c.Name AS Client_Name, w.Type AS Workout_Type, c.Login_ID AS Username,
            DATEDIFF(m.EndDate, CURDATE()) AS Membership_Duration
            FROM Client c
            JOIN Client_Workout_Type cw ON c.Client_ID = cw.Client_ID
            JOIN Workout_Type w ON cw.Workout_Type_ID = w.Workout_Type_ID
            JOIN Membership m ON c.Client_ID = m.Client_ID
            WHERE m.EndDate > CURDATE();
                       """)
        clients = cursor.fetchall()
        for client in clients:
            client_listbox.insert(tk.END, f"{client[1]} - {client[2]} ")

        # Fetch trainers with workout type and username
        cursor.execute("""
            SELECT t.Trainer_ID, t.Name AS Trainer_Name, w.Type AS Workout_Type, t.Login_ID AS Username
            FROM Trainer t
            JOIN Trainer_Workout_Type tw ON t.Trainer_ID = tw.Trainer_ID
            JOIN Workout_Type w ON tw.Workout_Type_ID = w.Workout_Type_ID;
                       """)
        trainers = cursor.fetchall()
        trainer_names = [f"{trainer[1]} - {trainer[2]}" for trainer in trainers]
        trainer_combobox['values'] = trainer_names

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

    return clients, trainers

def process_assign_schedule(client_listbox, trainer_combobox, schedule_date, schedule_time, clients, trainers):
    # Get selected client and trainer
    client_selections = client_listbox.curselection()
    trainer_selection = trainer_combobox.get()

    if not client_selections or not trainer_selection:
        messagebox.showerror("Selection Error", "Please select both a client and a trainer.")
        return

    client_info = client_listbox.get(client_selections[0])  # Get first client selected
    trainer_info = trainer_selection  # Get the selected trainer from the combobox

    # Extract workout types from the selected client and trainer
    client_workout_type = client_info.split(" - ")[1]
    trainer_workout_type = trainer_info.split(" - ")[1]

    # Ensure workout types match
    

    # Proceed with schedule assignment if types match
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Schedule (Date, Time) VALUES (%s, %s)", (schedule_date, schedule_time))
        schedule_id = cursor.lastrowid

        # Insert assignments for the selected client and trainer
        client_id = clients[client_selections[0]][0]
        trainer_id = trainers[trainer_combobox.current()][0]
        cursor.execute("INSERT INTO Client_Schedule (Client_ID, Schedule_ID) VALUES (%s, %s)", (client_id, schedule_id))
        cursor.execute("INSERT INTO Trainer_Schedule (Trainer_ID, Schedule_ID) VALUES (%s, %s)", (trainer_id, schedule_id))

        conn.commit()
        messagebox.showinfo("Schedule Assigned", "Schedule successfully assigned to client and trainer.")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def assign_schedule():
    # Function to open a new window to assign schedules
    assign_window = tk.Toplevel(login_frame)
    assign_window.title("Assign Schedule")

    tk.Label(assign_window, text="Assign Schedule to Client and Trainer", font=("Arial", 24)).pack(pady=10)

    # Frame to hold client and trainer widgets side by side for better UI layout
    frame = tk.Frame(assign_window)
    frame.pack(pady=10)

    # Listbox for clients
    client_listbox_label = tk.Label(frame, text="Clients (Workout Type, Username, Membership Duration):", font=("Arial", 14))
    client_listbox_label.grid(row=0, column=0, sticky="w")
    client_listbox = tk.Listbox(frame, font=("Arial", 12), width=50, height=8, selectmode=tk.SINGLE)
    client_listbox.grid(row=1, column=0, pady=5)

    # Combobox for trainers (Dropdown)
    trainer_combobox_label = tk.Label(frame, text="Trainers (Workout Type, Username):", font=("Arial", 14))
    trainer_combobox_label.grid(row=0, column=1, padx=20, sticky="w")
    trainer_combobox = ttk.Combobox(frame, font=("Arial", 12), width=50)
    trainer_combobox.grid(row=1, column=1, pady=5)

    # Populate Listboxes with Clients and Trainers
    clients, trainers = populate_client_trainer_listboxes(client_listbox, trainer_combobox)

    # Schedule date input field using Calendar
    schedule_date_label = tk.Label(assign_window, text="Schedule Date:", font=("Arial", 18))
    schedule_date_label.pack()
    schedule_date_calendar = Calendar(assign_window, date_pattern="yyyy-mm-dd")
    schedule_date_calendar.pack(pady=5)

    # Schedule time input field
    schedule_time_label = tk.Label(assign_window, text="Schedule Time (HH:MM:SS):", font=("Arial", 18))
    schedule_time_label.pack()
    schedule_time_entry = tk.Entry(assign_window, font=("Arial", 18))
    schedule_time_entry.pack(pady=5)

    # Assign Button
    assign_button = tk.Button(assign_window, text="Assign", font=("Arial", 16),
                              command=lambda: process_assign_schedule(
                                  client_listbox, trainer_combobox,
                                  schedule_date_calendar.get_date(), schedule_time_entry.get(),
                                  clients, trainers
                              ))
    assign_button.pack(pady=20)# Assuming you have a Tkinter main loop here to run the UI
    
def add_trainer(name, contact, expertise, password):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Check if the username already exists in the Login table
        check_query = """
            SELECT Username FROM Login WHERE Username = %s
        """
        cursor.execute(check_query, (name,))
        existing_username = cursor.fetchone()

        if existing_username:
            # Username is already taken
            messagebox.showerror("Error", "This username cannot be taken!")
            return

        # Insert the login details into the Login table first
        insert_login_query = """
            INSERT INTO Login (Username, Password)
            VALUES (%s, %s)
        """
        cursor.execute(insert_login_query, (name, password))
        login_id = cursor.lastrowid  # Get the last inserted Login_ID

        # Insert the new trainer details into the Trainer table
        insert_trainer_query = """
            INSERT INTO Trainer (Name, Contact, Expertise, Password, login_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_trainer_query, (name, contact, expertise, password, login_id))
        trainer_id = cursor.lastrowid  # Get the last inserted trainer ID

        # Check if the workout type exists in the Workout_Type table
        cursor.execute("SELECT Workout_Type_ID FROM Workout_Type WHERE Type = %s", (expertise,))
        result = cursor.fetchone()

        if result:
            workout_type_id = result[0]
        else:
            # Insert new workout type if it doesn't exist
            cursor.execute("INSERT INTO Workout_Type (Type) VALUES (%s)", (expertise,))
            workout_type_id = cursor.lastrowid

        # Link the trainer to the workout type in Trainer_Workout_Type
        insert_trainer_workout_query = """
            INSERT INTO Trainer_Workout_Type (Trainer_ID, Workout_Type_ID)
            VALUES (%s, %s)
        """
        cursor.execute(insert_trainer_workout_query, (trainer_id, workout_type_id))

        # Commit the transaction
        conn.commit()

        # Show success message
        messagebox.showinfo("Success", "Trainer added successfully!")

    except mysql.connector.Error as err:
        # Display error message if there's an issue
        conn.rollback()
        messagebox.showerror("Error", f"Failed to add trainer: {err}")
    finally:
        cursor.close()
        conn.close()
    
    show_admin_dashboard()



def open_add_trainer_form():
    # Destroy current widgets in login_frame
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Title for Add Trainer Form
    form_label = tk.Label(
        login_frame,
        text="Add Trainer",
        font=("Arial", 36, "bold"),
        bg="#E6E6FA",
        fg="#333333"
    )
    form_label.pack(pady=20)

    # Trainer Name Entry
    name_label = tk.Label(login_frame, text="Trainer Name:", font=("Arial", 18), bg="#E6E6FA")
    name_label.pack()
    name_entry = tk.Entry(login_frame, font=("Arial", 18))
    name_entry.pack(pady=5)

    # Contact Entry
    contact_label = tk.Label(login_frame, text="Contact:", font=("Arial", 18), bg="#E6E6FA")
    contact_label.pack()
    contact_entry = tk.Entry(login_frame, font=("Arial", 18))
    contact_entry.pack(pady=5)

    # Expertise Dropdown
    expertise_label = tk.Label(login_frame, text="Expertise:", font=("Arial", 18), bg="#E6E6FA")
    expertise_label.pack()
    expertise_options = ["Gym", "Aero", "Zumba", "Yoga"]
    expertise_var = tk.StringVar()
    expertise_dropdown = ttk.Combobox(login_frame, textvariable=expertise_var, values=expertise_options, font=("Arial", 18))
    expertise_dropdown.set("Select Expertise")
    expertise_dropdown.pack(pady=5)
    
    # Password Entry
    password_label = tk.Label(login_frame, text="Password:", font=("Arial", 18), bg="#E6E6FA")
    password_label.pack()
    password_entry = tk.Entry(login_frame, font=("Arial", 18), show="*")
    password_entry.pack(pady=5)

   

    # Submit Button
    submit_button = tk.Button(
        login_frame,
        text="Add Trainer",
        command=lambda: add_trainer(
            name_entry.get(),
            contact_entry.get(),
            expertise_var.get(),
            password_entry.get()
            #login_id_entry.get()
        ),
        bg="#32CD32",
        fg="white",
        font=("Arial", 24, "bold"),
        relief="flat",
        padx=20, pady=10
    )
    submit_button.pack(pady=20)
    back_to_login= tk.Button( login_frame,text="GO BACK TO LOGIN PAGE",command=show_login_frame,bg="#32CD32",
                             fg="white",font=("Arial",24,"bold"), relief="flat",padx=20,pady=10)
    back_to_login.pack(pady=(20, 40), padx=20, anchor="w")


# Function to delete user
def delete_user():
    try:
        # Using context manager to ensure connection and cursor are properly handled
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='believeinyou',
            database='gym_aero_yoga_zumba_management'
        ) as conn:
            if not conn.is_connected():
                messagebox.showerror("Database Error", "Failed to connect to the database.")
                return

            with conn.cursor() as cursor:
                # Fetch user details
                cursor.execute("SELECT Client_ID, Name, Email FROM Client")
                user_details = cursor.fetchall()

                if not user_details:
                    messagebox.showinfo("Delete User", "No users found.")
                    return

                # Create the delete window
                delete_window = tk.Toplevel(root)
                delete_window.title("Delete User")
                delete_window.geometry("500x400")

                # Add users to listbox
                user_listbox = tk.Listbox(delete_window, width=50, font=("Arial", 16))
                user_listbox.pack(pady=20)

                for user in user_details:
                    user_listbox.insert(tk.END, f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

                # Delete the selected user
                def delete_selected_user():
                    conn=create_connection()
                    cursor = conn.cursor()

                    selected_user = user_listbox.curselection()
                    if selected_user:
                        user_data = user_listbox.get(selected_user)
                        client_id = int(user_data.split(",")[0].split(":")[1].strip())
                        print(f"Deleting user with ID {client_id}")  # Debugging line

                        try:
                            # Delete from Client table first to trigger the AFTER DELETE trigger
                            cursor.execute("DELETE FROM Client WHERE Client_ID = %s", (client_id,))
                            print(f"Deleted from Client table for client ID {client_id}")  # Debugging line

                            # Now delete the associated Login record
                            cursor.execute(
                                "DELETE FROM Login WHERE Login_ID = (SELECT Login_ID FROM Client WHERE Client_ID = %s)", 
                                (client_id,)
                            )
                            print(f"Deleted from Login table for client ID {client_id}")  # Debugging line

                            conn.commit()
                            messagebox.showinfo("Delete User", f"User with ID {client_id} has been deleted.")
                            delete_window.destroy()
                            cursor.close()
                            conn.commit()

                        except mysql.connector.Error as err:
                            messagebox.showerror("Database Error", f"Error deleting user: {err}")

                    else:
                        messagebox.showerror("Delete Error", "Please select a user to delete.")

                delete_button = tk.Button(
                    delete_window, text="Delete Selected User", command=delete_selected_user,
                    bg="#FF6347", fg="white", font=("Arial", 16, "bold")
                )
                delete_button.pack(pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


    

# Function to update user details
def update_user_details():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Fetch all client details
        cursor.execute("SELECT Client_ID, Name, Email, Contact FROM Client")
        user_details = cursor.fetchall()

        if not user_details:
            messagebox.showinfo("Update User", "No users found.")
            return

        # Create a new window to display the user list
        update_window = tk.Toplevel(root)
        update_window.title("Update User")
        update_window.geometry("500x500")

        # Create a listbox to display user details
        user_listbox = tk.Listbox(update_window, width=50, font=("Arial", 14))
        user_listbox.pack(pady=10)

        # Add users to the listbox
        for user in user_details:
            user_listbox.insert(tk.END, f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Contact: {user[3]}")

        # Frame for entry fields
        fields_frame = tk.Frame(update_window)
        fields_frame.pack(pady=20)

        # Function to allow updating the selected user's details
        def update_selected_user():
            selected_user = user_listbox.curselection()
            if selected_user:
                user_data = user_listbox.get(selected_user)
                client_id = int(user_data.split(",")[0].split(":")[1].strip())  # Extract Client_ID

                conn_nested = create_connection()
                cursor_nested = conn_nested.cursor()

                try:
                    # Fetch current user details
                    cursor_nested.execute("SELECT Name, Email, Contact FROM Client WHERE Client_ID = %s", (client_id,))
                    current_user_data = cursor_nested.fetchone()

                    # Clear any existing widgets in fields_frame
                    for widget in fields_frame.winfo_children():
                        widget.destroy()

                    # Create fields for updating details
                    name_label = tk.Label(fields_frame, text="Name:", font=("Arial", 14))
                    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
                    name_entry = tk.Entry(fields_frame, font=("Arial", 14))
                    name_entry.insert(0, current_user_data[0])
                    name_entry.config(state="disabled")  # Make the name field non-editable
                    name_entry.grid(row=0, column=1, padx=5, pady=5)

                    email_label = tk.Label(fields_frame, text="Email ID:", font=("Arial", 14))
                    email_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
                    email_entry = tk.Entry(fields_frame, font=("Arial", 14))
                    email_entry.insert(0, current_user_data[1])
                    email_entry.grid(row=1, column=1, padx=5, pady=5)

                    contact_label = tk.Label(fields_frame, text="Contact Number:", font=("Arial", 14))
                    contact_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
                    contact_entry = tk.Entry(fields_frame, font=("Arial", 14))
                    contact_entry.insert(0, current_user_data[2])
                    contact_entry.grid(row=2, column=1, padx=5, pady=5)

                    # Function to update user details in the database
                    def save_updates():
                        new_email = email_entry.get()
                        new_contact = contact_entry.get()

                        conn_save = create_connection()
                        cursor_save = conn_save.cursor()

                        try:
                            # Update user details in the database
                            cursor_save.execute("UPDATE Client SET Email = %s, Contact = %s WHERE Client_ID = %s",
                                                (new_email, new_contact, client_id))
                            conn_save.commit()

                            messagebox.showinfo("Update User", f"User with ID {client_id} has been updated.")
                            update_window.destroy()  # Close the update window

                        except mysql.connector.Error as err:
                            messagebox.showerror("Database Error", f"Error updating user: {err}")

                        finally:
                            # Ensure the connection and cursor are closed properly in save_updates
                            if cursor_save:
                                cursor_save.close()
                            if conn_save:
                                conn_save.close()

                    # Save button to apply the changes
                    save_button = tk.Button(fields_frame, text="Save Changes", command=save_updates, bg="#32CD32", fg="white", font=("Arial", 14, "bold"))
                    save_button.grid(row=3, column=1, pady=20)

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error fetching user: {err}")

                finally:
                    # Ensure the connection and cursor are closed properly in update_selected_user
                    if cursor_nested:
                        cursor_nested.close()
                    if conn_nested:
                        conn_nested.close()

            else:
                messagebox.showerror("Update Error", "Please select a user to update.")

        # Add a button to trigger the update
        update_button = tk.Button(update_window, text="Select and Update User", command=update_selected_user, bg="#FF6347", fg="white", font=("Arial", 14, "bold"))
        update_button.pack(pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        # Ensure the connection and cursor are closed properly in update_user_details
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Function to display the login frame


def show_trainer_login_form():
    # Clear existing widgets
    for widget in login_frame.winfo_children():
        widget.destroy()

    # Load the background image
    background_image = Image.open("C:/Users/HP/Desktop/5th SEM/DBMS/dbms_project/3d-gym-trainer.jpg")
    background_image = background_image.resize((login_frame.winfo_width(), login_frame.winfo_height()))  # Resize to fit the frame
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Set background image label
    background_label = tk.Label(login_frame, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_photo  # Keep a reference to prevent garbage collection

    # Title for Trainer Login Form
    form_label = tk.Label(
        login_frame,
        text="Trainer Login",
        font=("Arial", 36, "bold"),
        bg="#E6E6FA",
        fg="#333333",
        anchor="w",  # Align the text to the left
    )
    form_label.pack(pady=(20, 10))  # More space on top, less on bottom

    # Trainer Name Entry
    name_label = tk.Label(login_frame, text="Trainer Name:", font=("Arial", 18), bg="#E6E6FA", anchor="w")
    name_label.pack(padx=20, pady=(0, 10), anchor="w")  # 2 lines of gap below label
    name_entry = tk.Entry(login_frame, font=("Arial", 18))
    name_entry.pack(padx=20, pady=(0, 40), anchor="w")  # 4 lines of gap below entry

    # Password Entry
    password_label = tk.Label(login_frame, text="Password:", font=("Arial", 18), bg="#E6E6FA", anchor="w")
    password_label.pack(padx=20, pady=(0, 10), anchor="w")  # 2 lines of gap below label
    password_entry = tk.Entry(login_frame, font=("Arial", 18), show="*")
    password_entry.pack(padx=20, pady=(0, 40), anchor="w")  # 4 lines of gap below entry

    # Submit Button
    submit_button = tk.Button(
        login_frame,
        text="Login as Trainer",
        command=lambda: trainer_login(name_entry.get(), password_entry.get()),
        bg="#32CD32",
        fg="white",
        font=("Arial", 24, "bold"),
        relief="flat",
        padx=20, pady=10
    )
    submit_button.pack(pady=(20, 40), padx=20, anchor="w")  # Aligned to left and added gap
    back_to_login= tk.Button( login_frame,text="GO BACK TO LOGIN PAGE",command=lambda:show_login_frame(),bg="#32CD32",
                             fg="white",font=("Arial",24,"bold"), relief="flat",padx=20,pady=10)
    back_to_login.pack(pady=(20, 40), padx=20, anchor="w")



# Function to handle trainer login logic
def trainer_login(name, password):
    # Establish database connection
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Error", "Unable to connect to the database!")
        return

    # Create a cursor object
    cursor = conn.cursor()

    # Check the trainer credentials (Assuming you have a Trainer table in the DB)
    cursor.execute("SELECT * FROM Trainer WHERE Name = %s AND Password = %s", (name, password))
    trainer = cursor.fetchone()  # This will return a tuple, not just the ID

    if trainer:
        # If trainer exists, show the trainer page
        show_trainer_page(trainer)  # Pass the full trainer record (not just the ID)
    else:
        messagebox.showerror("Error", "Invalid trainer credentials!")

    # Close the cursor and connection after use
    cursor.close()
    conn.close()




# Create main application window
import tkinter as tk


    # Create the main Tkinter window
root = tk.Tk()
root.title("Gym Aero Yoga Zumba Management System")
    
    # Set the window to open in full screen
root.state("zoomed")  # 'zoomed' makes the window open maximized in Windows

global login_frame, register_frame
    
# Create frames for login and registration
login_frame = tk.Frame(root, bg="#f5f5f5")
login_frame.pack(expand=True, fill='both')
    
register_frame = tk.Frame(root, bg="#f5f5f5")
register_frame.pack(expand=True, fill='both')
    
    # Show the login frame first
show_register_frame()

    # Start the Tkinter event loop
root.mainloop()

# Ensure that the GUI only runs when the script is executed directly

