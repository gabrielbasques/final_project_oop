import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import pickle
from datetime import datetime


# ... other necessary imports ...

import pickle
from datetime import date, datetime
from typing import List

# base class for all employees
class Employee:
    def __init__(self, id_number=0, name="", department="", job_title="", basic_salary=0.0,
                 age=0, date_of_birth=None, passport_details=""):
        self.id_number = id_number
        self.name = name
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details

    # display employee details
    def display_details(self):
        dob_formatted = self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else "Not provided"
        details = (
            f"Name:\t\t{self.name}\n"
            f"ID Number:\t{self.id_number}\n"
            f"Department:\t{self.department}\n"
            f"Job Title:\t{self.job_title}\n"
            f"Basic Salary:\t{self.basic_salary}\n"
            f"Age:\t\t{self.age}\n"
            f"DOB:\t\t{dob_formatted}\n"
            f"Passport:\t{self.passport_details}"
        )
        if hasattr(self, 'manager_id') and self.manager_id:  # Check if the employee is a Salesperson and has a manager
            details += f"\nManager ID:\t{self.manager_id}"
        return details

    def calculate_salary_after_sales(self):
        total_commission = 0
        total_loss = 0

        for sale in self.sales:
            profit = sale.calculate_profit()
            loss = sale.calculate_loss()
            if profit > 0:
                total_commission += self.calculate_commission(profit)
            else:
                total_loss += loss

        # Deduct loss from salary if necessary
        self.basic_salary = self.basic_salary + total_commission - self.calculate_salary_loss(total_loss)
        return self.basic_salary

    def calculate_commission(self, profit):
        return profit * 0.065  # 6.5% commission rate

    # New method to calculate loss deduction from salary
    def calculate_loss_deduction(self, loss):
        return loss * 0.01  # 1% loss rate

# sales manager class
class Manager(Employee):
    def __init__(self, salespersons=None, **kwargs):
        self.salespersons = salespersons if salespersons is not None else []
        Employee.__init__(self, **kwargs)

    # calculate commission for the manager
    def calculate_comission(self, profit):
        return profit * 0.0325  # 3.25% commission rate for manager

    def calculate_loss_deduction(self, loss):
        return loss * 0.02  # 2% loss rate for manager
    # calculate salary considering potential loss
    def calculate_salary(self, loss):
        return self.basic_salary - (loss * 0.02)

    def calculate_salary_loss(self, total_loss):
        return total_loss * 0.02

    # add a salesperson to the manager's team
    def add_salesperson(self, salesperson):
        self.salespersons.append(salesperson)

    # remove a salesperson from the manager's team
    def remove_salesperson(self, salesperson_id):
        self.salespersons = [sp for sp in self.salespersons if sp.id_number != salesperson_id]

# salesperson class
class Salesperson(Employee):
    def __init__(self, manager_id="", **kwargs):
        self.manager_id = manager_id
        self.sales = []  # List to keep track of sales
        Employee.__init__(self, **kwargs)

    # calculate commission for the salesperson
    def calculate_commission(self, profit):
        return profit * 0.065

    # calculate salary considering potential loss
    def calculate_salary(self, loss):
        return self.basic_salary - (loss * 0.01)

    def calculate_salary_loss(self, total_loss):
        return total_loss * 0.01

    # record a sale made by the salesperson
    def make_sale(self, sale):
        self.sales.append(sale)

# house class
class House:
    def __init__(self, name = "",id_number="", declared_price=0.0, house_type="", built_up_area=0,
                 status="", number_of_rooms=0, number_of_bathrooms=0):
        self.name = name
        self.id_number = id_number
        self.declared_price = declared_price
        self.house_type = house_type
        self.built_up_area = built_up_area
        self.status = status
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms

    # display house details
    def display_details(self):
        return (
            f"Name:\t\t{self.name}\n"
            f"ID Number:\t{self.id_number}\n"
            f"Declared Price:\t{self.declared_price}\n"
            f"Type:\t\t{self.house_type}\n"
            f"Built-Up Area:\t{self.built_up_area} sqft\n"
            f"Status:\t\t{self.status}\n"
            f"Rooms:\t\t{self.number_of_rooms}\n"
            f"Bathrooms:\t{self.number_of_bathrooms}"
        )

# sale class
class Sale:
    def __init__(self, house, selling_price, sales_date, salesperson_id):
        self.house = house
        self.selling_price = selling_price
        self.sales_date = sales_date
        self.salesperson_id = salesperson_id

    def calculate_profit(self):
        return max(0, self.selling_price - self.house.declared_price)

    def calculate_loss(self):
        return max(0, self.house.declared_price - self.selling_price)

    def calculate_commission(self):
        profit = self.calculate_profit()
        if profit > 0:
            return profit * 0.065  # Commission percentage
        return 0
    # display sale details
    def display_details(self):
        # details to be displayed in a user-friendly format
        profit_or_loss = self.calculate_profit() or -self.calculate_loss()
        print(f"House ID: {self.house.id_number}, Selling Price: {self.selling_price}, "
              f"Sales Date: {self.sales_date.strftime('%Y-%m-%d')}, Salesperson ID: {self.salesperson_id}, "
              f"Profit/Loss: {profit_or_loss}")


# Load and Save Functions
def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []



# GUI Class Definition
# Application GUI
class RealEstateApp:
    def __init__(self, master):
        self.master = master
        master.title("Real Estate Management System")

        # Initialize the employees and houses lists
        self.employees = load_data(EMPLOYEES_FILE)
        self.houses = load_data(HOUSES_FILE)

        # Styling constants
        button_font = ("Arial", 12, "bold")
        button_padx = 10
        button_pady = 5
        frame_padx = 20
        frame_pady = 10
        frame_ipadx = 5
        frame_ipady = 5

        # Define frames
        self.top_frame = tk.Frame(master, padx=frame_padx, pady=frame_pady)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(master, padx=frame_padx, pady=frame_pady)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Add employee button
        self.add_employee_button = tk.Button(self.top_frame, text="Add Employee", font=button_font, padx=button_padx, pady=button_pady, command=self.add_employee)
        self.add_employee_button.grid(row=0, column=0, sticky="ew")

        # Add house button
        self.add_house_button = tk.Button(self.top_frame, text="Add House", font=button_font, padx=button_padx, pady=button_pady, command=self.add_house)
        self.add_house_button.grid(row=0, column=1, sticky="ew")

        # Delete employee button
        self.delete_employee_button = tk.Button(self.top_frame, text="Delete Employee", font=button_font, padx=button_padx, pady=button_pady, command=self.delete_employee)
        self.delete_employee_button.grid(row=1, column=0, sticky="ew")

        # Delete house button
        self.delete_house_button = tk.Button(self.top_frame, text="Delete House", font=button_font, padx=button_padx, pady=button_pady, command=self.delete_house)
        self.delete_house_button.grid(row=1, column=1, sticky="ew")

        # Display employees button
        self.display_employees_button = tk.Button(self.bottom_frame, text="Display Employees", font=button_font, padx=button_padx, pady=button_pady, command=self.display_employees)
        self.display_employees_button.grid(row=0, column=0, sticky="ew")

        # Display houses button
        self.display_houses_button = tk.Button(self.bottom_frame, text="Display Houses", font=button_font, padx=button_padx, pady=button_pady, command=self.display_houses)
        self.display_houses_button.grid(row=0, column=1, sticky="ew")

        # Show employee by ID button
        self.show_employee_button = tk.Button(self.bottom_frame, text="Show Employee by ID", font=button_font, padx=button_padx, pady=button_pady, command=self.show_employee_by_id)
        self.show_employee_button.grid(row=1, column=0, sticky="ew")

        # Show house by ID button
        self.show_house_button = tk.Button(self.bottom_frame, text="Show House by ID", font=button_font, padx=button_padx, pady=button_pady, command=self.show_house_by_id)
        self.show_house_button.grid(row=1, column=1, sticky="ew")

        # Display sales details button
        self.display_sales_button = tk.Button(self.bottom_frame, text="Display Sales Details", font=button_font, padx=button_padx, pady=button_pady, command=self.display_sales_details)
        self.display_sales_button.grid(row=2, column=0, sticky="ew")

        # Save data button
        self.save_data_button = tk.Button(self.bottom_frame, text="Save Data", font=button_font, padx=button_padx, pady=button_pady, command=self.save_data)
        self.save_data_button.grid(row=3, column=0, sticky="ew",columnspan=2)

        # Record sale button
        self.record_sale_button = tk.Button(self.bottom_frame, text="Record Sale", font=button_font, padx=button_padx, pady=button_pady, command=self.record_sale)
        self.record_sale_button.grid(row=2, column=1, sticky="ew")

        # Configure the grid for dynamic resizing
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(2, weight=1)

        # Set the minimum size of the window
        master.minsize(400, 200)

        # Set the starting size of the window
        master.geometry("600x400")

    def record_sale(self):
        # Prompt for the sales details
        salesperson_id = simpledialog.askstring("Record Sale", "Enter salesperson ID:")
        house_id = simpledialog.askstring("Record Sale", "Enter house ID:")
        selling_price = simpledialog.askfloat("Record Sale", "Enter selling price:")

        # Find the salesperson and the house
        salesperson = self.find_employee_by_id(salesperson_id)
        house = self.find_house_by_id(house_id)

        if not salesperson or not house:
            messagebox.showerror("Error", "Invalid salesperson ID or house ID.")
            return

        # Record the sale
        sales_date = datetime.now()  # assuming the sale is made now
        sale = Sale(house, selling_price, sales_date, salesperson_id)
        salesperson.sales.append(sale)

        # Calculate and apply commission and loss deduction
        profit = sale.calculate_profit()
        loss = sale.calculate_loss()

        if profit > 0:
            # Apply commission
            commission = salesperson.calculate_commission(profit)
            salesperson.basic_salary += commission
            # If the salesperson is a Salesperson, also apply the manager's commission
            if isinstance(salesperson, Salesperson):
                manager = self.find_employee_by_id(salesperson.manager_id)
                if manager:
                    manager.basic_salary += manager.calculate_commission(profit)
        elif loss > 0:
            # Deduct loss from salesperson's salary
            salesperson.basic_salary -= salesperson.calculate_loss_deduction(loss)
            # If the salesperson is a Salesperson, also deduct loss from the manager's salary
            if isinstance(salesperson, Salesperson):
                manager = self.find_employee_by_id(salesperson.manager_id)
                if manager:
                    manager.basic_salary -= manager.calculate_loss_deduction(loss)

        # Save the updated data
        save_data(self.employees, EMPLOYEES_FILE)
        messagebox.showinfo("Success", "Sale recorded successfully.")

    # Show house by ID function
    def show_house_by_id(self):
        house_id = simpledialog.askstring("Input", "Enter house ID:")
        house = self.find_house_by_id(house_id)
        if house:
            self.display_in_treeview([house],
                                     ['Name', 'ID Number', 'Declared Price', 'Type', 'Built-Up Area', 'Status', 'Rooms',
                                      'Bathrooms'], "House Details")
        else:
            messagebox.showinfo("House Details", "House not found.")

    def display_houses(self):
        self.display_in_treeview(self.houses,
                                 ['Name', 'ID Number', 'Declared Price', 'Type', 'Built-Up Area', 'Status', 'Rooms',
                                  'Bathrooms'], "All Houses")

    def display_employees(self):
        self.display_in_treeview(self.employees,
                                 ['Name', 'ID Number', 'Department', 'Job Title', 'Basic Salary', 'Age', 'DOB',
                                  'Passport', 'Manager ID'], "All Employees")

    def display_in_treeview(self, items, columns, title):
        details_window = tk.Toplevel(self.master)
        details_window.title(title)
        # Set a standard window size
        details_window.geometry("1000x400")  # Adjust the size as needed to fit your content

        tree = ttk.Treeview(details_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col, anchor='center')  # Center the text in the column heading
            tree.column(col, anchor="center", width=100)  # Adjust the width as needed

        for item in items:
            if isinstance(item, Employee):
                tree.insert("", "end", values=(
                    item.name, item.id_number, item.department, item.job_title, item.basic_salary,
                    item.age, item.date_of_birth.strftime('%Y-%m-%d') if item.date_of_birth else "Not provided",
                    item.passport_details, getattr(item, 'manager_id', 'N/A')
                ))
            elif isinstance(item, House):
                tree.insert("", "end", values=(
                    item.name, item.id_number, item.declared_price, item.house_type, item.built_up_area,
                    item.status, item.number_of_rooms, item.number_of_bathrooms
                ))

        tree.pack(expand=True, fill='both')
        # Center the treeview in the window
        details_window.grid_rowconfigure(0, weight=1)
        details_window.grid_columnconfigure(0, weight=1)
        details_window.transient(self.master)
        details_window.grab_set()
        self.master.wait_window(details_window)

        # Center the contents of each column
        for col in columns:
            tree.column(col, anchor="center")

        tree.pack(expand=True, fill='both')
        details_window.transient(self.master)
        details_window.grab_set()
        self.master.wait_window(details_window)
    # Show employee by ID function
    def show_employee_by_id(self):
        employee_id = simpledialog.askstring("Input", "Enter employee ID:")
        employee = self.find_employee_by_id(employee_id)
        if employee:
            # Create a new top-level window
            details_window = tk.Toplevel(self.master)
            details_window.title("Employee Details")

            # Create a Treeview widget
            tree = ttk.Treeview(details_window, columns=(
            "Name", "ID Number", "Department", "Job Title", "Basic Salary", "Age", "DOB", "Passport", "Manager ID"),
                                show='headings')

            # Define the column headings
            tree.heading("Name", text="Name")
            tree.heading("ID Number", text="ID Number")
            tree.heading("Department", text="Department")
            tree.heading("Job Title", text="Job Title")
            tree.heading("Basic Salary", text="Basic Salary")
            tree.heading("Age", text="Age")
            tree.heading("DOB", text="DOB")
            tree.heading("Passport", text="Passport")
            tree.heading("Manager ID", text="Manager ID")

            # Insert the employee details into the treeview
            tree.insert("", "end", values=(
            employee.name, employee.id_number, employee.department, employee.job_title, employee.basic_salary,
            employee.age, employee.date_of_birth, employee.passport_details, getattr(employee, 'manager_id', '')))

            # Pack the Treeview to the window
            tree.pack(expand=True, fill='both')

            # Open the window
            details_window.transient(self.master)  # Set to be on top of the main window
            details_window.grab_set()  # Modal focus
            self.master.wait_window(details_window)  # Wait here until the details_window is closed
        else:
            messagebox.showinfo("Employee Details", "Employee not found.")

    # Delete employee function
    def delete_employee(self):
        id_number = simpledialog.askstring("Input", "Enter employee ID to delete:")
        self.employees = [e for e in self.employees if e.id_number != id_number]
        messagebox.showinfo("Success", "Employee deleted successfully")

    def delete_house(self):
        id_number = simpledialog.askstring("Input", "Enter house ID to delete:")
        self.houses = [h for h in self.houses if h.id_number != id_number]
        messagebox.showinfo("Success", "House deleted successfully")

    def find_employee_by_id(self, employee_id):
        for emp in self.employees:
            if emp.id_number == employee_id:
                return emp
        return None

    def find_house_by_id(self, house_id):
        for house in self.houses:
            if house.id_number == house_id:
                return house
        return None

    def display_sales_details(self):
        employee_id = simpledialog.askstring("Input", "Enter employee ID:")
        month_year = simpledialog.askstring("Input", "Enter the month and year (MM-YYYY):")

        try:
            month, year = map(int, month_year.split('-'))
        except ValueError:
            messagebox.showerror("Error", "Invalid month and year format. Please use MM-YYYY.")
            return

        sales_details = []
        for emp in self.employees:
            if emp.id_number == employee_id:
                total_commission = 0
                total_sales = 0
                for sale in emp.sales:
                    if sale.sales_date.month == month and sale.sales_date.year == year:
                        profit = sale.calculate_profit()
                        loss = sale.calculate_loss()
                        if profit > 0:
                            total_commission += emp.calculate_commission(profit)
                        else:
                            emp.basic_salary -= emp.calculate_salary(loss)  # Deduct loss from salary if necessary
                        total_sales += sale.selling_price
                sales_details.append(f"Total Sales: {total_sales}, Total Commission: {total_commission}, "
                                     f"Expected Salary: {emp.basic_salary}")
                break
        if not sales_details:
            sales_details = ["No sales or employee not found."]

        messagebox.showinfo("Sales Details", "\n".join(sales_details))

        employee = self.find_employee_by_id(employee_id)
        if not employee:
            messagebox.showinfo("Error", "Employee not found.")
            return

        # Calculate commission and expected salary
        total_commission = sum([employee.calculate_commission(sale.calculate_profit()) for sale in employee.sales if
                                sale.sales_date.month == month and sale.sales_date.year == year])
        expected_salary = employee.basic_salary + total_commission

        messagebox.showinfo("Sales Details",
                            f"Total Commission: {total_commission}, Expected Salary: {expected_salary}")

    def add_employee(self):
        # Prompt user to enter employee details
        id_number = simpledialog.askstring("Input", "Enter employee ID:")
        name = simpledialog.askstring("Input", "Enter employee name:")
        department = simpledialog.askstring("Input", "Enter department:")
        job_title = simpledialog.askstring("Input", "Enter job title:")
        basic_salary = simpledialog.askfloat("Input", "Enter basic salary:")
        age = simpledialog.askinteger("Input", "Enter employee's age:")
        parsed_dob = None  # Initialize the variable outside the loop
        while True:
            dob_input = simpledialog.askstring("Input", "Enter date of birth (YYYY-MM-DD):")
            if dob_input is None:
                messagebox.showerror("Error", "Date of birth is required.")
                return  # Exit the function if no input is given

            try:
                parsed_dob = datetime.strptime(dob_input, '%Y-%m-%d').date()
                break  # Exit loop if parsing is successful
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

        passport_details = simpledialog.askstring("Input", "Enter passport details:")
        parsed_dob = str(parsed_dob)
        parsed_dob = datetime.strptime(parsed_dob, '%Y-%m-%d').date()

        # Create and add new employee
        if job_title.lower() == 'manager':
            new_employee = Manager(id_number=id_number, name=name, department=department,
                                   job_title=job_title, basic_salary=basic_salary, age=age,
                                   date_of_birth=parsed_dob, passport_details=passport_details)
        else:
            new_employee = Salesperson(id_number=id_number, name=name, department=department,
                                       job_title=job_title, basic_salary=basic_salary, age=age,
                                       date_of_birth=parsed_dob, passport_details=passport_details)
        self.employees.append(new_employee)

    def add_house(self):
        # Prompt user to enter house details
        name = simpledialog.askstring("Input", "Enter house name:")
        id_number = simpledialog.askstring("Input", "Enter house ID:")
        declared_price = simpledialog.askfloat("Input", "Enter declared price:")
        house_type = simpledialog.askstring("Input", "Enter house type (apartment, townhouse, villa):")
        built_up_area = simpledialog.askinteger("Input", "Enter built-up area (in sqft):")
        status = simpledialog.askstring("Input", "Enter house status (sold, available, reserved):")
        number_of_rooms = simpledialog.askinteger("Input", "Enter number of rooms:")
        number_of_bathrooms = simpledialog.askinteger("Input", "Enter number of bathrooms:")

        # Create and add new house
        new_house = House(name = name, id_number=id_number, declared_price=declared_price, house_type=house_type,
                          built_up_area=built_up_area, status=status, number_of_rooms=number_of_rooms,
                          number_of_bathrooms=number_of_bathrooms)
        self.houses.append(new_house)

    def display_employees(self):
        # Create a new window
        employees_window = tk.Toplevel(self.master)
        employees_window.title("All Employees")

        # Create a Treeview widget
        tree = ttk.Treeview(employees_window)
        tree['columns'] = ('ID Number', 'Name', 'Department', 'Job Title', 'Basic Salary', 'Age', 'DOB', 'Passport', 'Manager ID')

        # Define the column headings
        for col in tree['columns']:
            tree.heading(col, text=col)
            tree.column(col, anchor="w")

        # Insert the employee details into the treeview
        for emp in self.employees:
            tree.insert("", "end", values=(
                emp.id_number, emp.name, emp.department, emp.job_title, emp.basic_salary,
                emp.age, emp.date_of_birth.strftime('%Y-%m-%d') if emp.date_of_birth else "Not provided",
                emp.passport_details, getattr(emp, 'manager_id', '')
            ))

        # Pack the Treeview to the window
        tree.pack(expand=True, fill='both')

    def display_houses(self):
        # Create a new window
        houses_window = tk.Toplevel(self.master)
        houses_window.title("All Houses")

        # Create a Treeview widget
        tree = ttk.Treeview(houses_window)
        tree['columns'] = ('ID Number', 'Name', 'Declared Price', 'Type', 'Built-Up Area', 'Status', 'Rooms', 'Bathrooms')

        # Define the column headings
        for col in tree['columns']:
            tree.heading(col, text=col)
            tree.column(col, anchor="w")

        # Insert the house details into the treeview
        for house in self.houses:
            tree.insert("", "end", values=(
                house.id_number, house.name, house.declared_price, house.house_type, house.built_up_area,
                house.status, house.number_of_rooms, house.number_of_bathrooms
            ))

        # Pack the Treeview to the window
        tree.pack(expand=True, fill='both')

    def save_data(self):
        # Save employees and houses data to files
        save_data(self.employees, EMPLOYEES_FILE)
        save_data(self.houses, HOUSES_FILE)
        messagebox.showinfo("Success", "Data saved successfully")


# Application Entry Point
if __name__ == "__main__":
    EMPLOYEES_FILE = 'employees.pkl'
    HOUSES_FILE = 'houses.pkl'
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()

