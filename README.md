
---

# **Gym Management System - Setup Instructions**

## **Important Steps**

### **1. Connect to MySQL Database**
- Ensure that you have a running **MySQL server**.
- Update your MySQL **username** and **password** in the `for_connect.py` file to match your MySQL credentials.

### **2. Run the SQL Script**
- **Run only** the `file1.sql` to set up the database schema and tables.
- **Do not modify or run** `file2.sql`.

### **3. Install Required Libraries**
Ensure that all the necessary Python libraries are installed. You can install the required libraries using pip:
```bash
pip install tkinter ttk mysql-connector pandas pillow dateutil tkcalendar
```

### **4. Set Up Admin Credentials**
- The default **Admin Username** and **Password** are as follows:
  - `ADMIN_USERNAME = "ITACHI_UCHHIA_THE_MAN_THE_MYTH_THE_LEGEND"`
  - `ADMIN_PASSWORD = "I_LOVE_YOU_IZUMI"`
- You can update these credentials in the `myfirst.py` file as per your requirement.

### **5. File and Directory Setup**
- Ensure that the `for_connect.py` file and any images required are located in the **same directory** as your other project files.

---

## **Running the Project**

### **1. Run the `myfirst.py` Script**
- Once you have set up the database, libraries, and files, **run the `myfirst.py`** script to start the Gym Management System.
- The script may take 10-15 seconds to start, as it initializes all the code in one file.
- Make sure that the MySQL database is connected and running while you execute the script.

---

## **Libraries Used**
The following libraries are used in the Gym Management System project:

1. **tkinter** - For creating the graphical user interface (GUI).
2. **ttk** - For themed widgets in the Tkinter GUI.
3. **messagebox** - For displaying popup message boxes in the GUI.
4. **mysql.connector** - For connecting Python with the MySQL database.
5. **datetime** - For working with date and time functionalities.
6. **dateutil.relativedelta** - For date manipulation (like calculating time differences).
7. **pandas** - For data manipulation and handling.
8. **PIL (Image, ImageTk)** - For image processing in the GUI.
9. **re** - For regular expressions to handle text patterns.
10. **tkcalendar (Calendar)** - For adding a calendar widget to the Tkinter GUI.
11. **Toplevel, Label, Frame, Listbox, Entry, Button** - Tkinter components for building the GUI.

---

### **Notes:**
- **Ensure all components are in the same directory** for smooth execution.
- If you encounter any issues, check your database connection and the installed libraries.

---

This version is organized, with **important instructions at the top**, followed by setup steps, running instructions, and additional details like the libraries used. You can now include this structured `README.txt` in your GitHub repository. Let me know if you'd like further adjustments!