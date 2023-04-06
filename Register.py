from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.validation import *
import os


class Register(tb.Window):
    def __init__(self) -> None:
        # configure the root window
        super().__init__(themename='darkly', resizable=(False, False))
        self.title("Register")
        self.geometry('600x650')

        # form variables
        self.email = tb.StringVar(value="")

        self.password = tb.StringVar(value="")
        self.confirm_password = tb.StringVar(value="")

        # Register the email validation callback
        isEmailAddress = self.register(self.isEmailAddress)

        # Sign in to your account text
        self.login_label = tb.Label(self, text = "", font=("Quicksand", 18, "bold"))
        self.login_label.pack(pady=(32,0))

        # Error message telling the user email/password doesn't exist
        self.incorrect_label = tb.Label(self, text = "", font=("Quicksand", 10, "bold"), bootstyle='danger')
        self.incorrect_label2 = tb.Label(self, text = "", font=("Quicksand", 10, "bold"), bootstyle='danger')
        
        # Pack the error messages
        self.incorrect_label.pack(pady=(0,0))
        self.incorrect_label2.pack(pady=(0,0))

        # Hide the email and password error message
        self.incorrect_label.pack()
        self.incorrect_label2.pack()

        # Big Sign in to your account text
        self.lg_login_label = tb.Label(self, text = "Register your account", font=("Quicksand", 22, "bold"))
        self.lg_login_label.place(x=65, y=40, height=100)

        self.email_lblframe, self.email_ent = self.create_form_entry("Your email", self.email, validation=(isEmailAddress, '%P'))

        self.password_lblframe, self.password_ent = self.create_form_entry("Password", self.password, pady=(30,100))
        self.confirm_password_lblframe, self.confirm_password_ent = self.create_form_entry("Confirm password", self.confirm_password, pady=(30,100))

        self.sign_up = self.button("Sign Up", "solid", self.signUp, pady=(25,0))

    
    def create_form_entry(self, label, variable, bootstyle='info', validation=None, **ent_misc):  
        
        lblframe = tb.LabelFrame(self, text=label.title(), bootstyle=bootstyle)
        ent_misc = {
            'padx' : 60,
            'pady' : (15,25),
            'side' : 'top'
        }
        ent_misc.update(ent_misc)
        lblframe.pack(fill=X, **ent_misc)

        # lblframe.pack(padx=60, pady=25, fill=X)
        
        ent = tb.Entry(lblframe, textvariable=variable, validate='focusout', validatecommand=validation)
        ent.config(font=("Quicksand", 12, "bold"), bootstyle='secondary')

        ent.pack(fill=X)

        if variable == self.password or variable == self.confirm_password:
            ent.config(show="*")

        return lblframe, ent
 
    
    def button(self, label, type, command, fontsize=12, **pack):
        # Check whether the type arg is valid
        btn_style = tb.Style()
        if type == "solid":
            reference = 'primary.TButton'
        elif type == "link":
            reference = 'primary.Link.TButton'
        elif type == "outline":
            reference = 'primary.Outline.TButton'
        else:
            raise TypeError("Type does not exist. Choose any from 'solid', 'outline', or 'link'")

        btn_style.configure(reference, font=("Quicksand", fontsize, 'bold'))

        btn = tb.Button(self, text=label, command=command, takefocus=False)
        btn.configure(bootstyle=f'primary, {type}', style=reference)

        btn_misc = {
            'padx' : 60,
            'pady' : 30,
            'side' : 'top'
        }
        btn_misc.update(pack)
        btn.pack(fill=X, **btn_misc)
    
    # Sign in button function
    def signUp(self):

        # Add the text Register your account
        self.login_label.config(text="Register your account")

        # Remove the big 'Register your account' text
        self.lg_login_label.place_forget()

        # To check whether email and password exists in the user data 
        def isAccount(email, password):
            
            # Check if the file exists
            if not os.path.isfile('userdata.txt'):
                # If the file doesn't exist, create a new one
                with open('userdata.txt', 'w') as f:
                    f.write('')

            # Open the file for reading
            with open('userdata.txt', 'r') as data:
                for line in data:
                    #Split the line into email and password using ','
                    stored_email, stored_password = line.strip().split(',')

                    # Check if the email and password match
                    if email == stored_email and password == stored_password:
                        print("It is true!")
                        return True
            print("It is false!")
            return False
        
        def addAccount(email, password):
            with open('userdata.txt', 'a') as data:
                data.write(f"{email},{password}\n")
        
        # To check whether the email and password matches with the verification entries
        def isConfirmed(email, password, confirm_password):
            if email and password == confirm_password:
                print("It is true! Haha")
                return True
            print("It is false! Haha")
            return False

        if (self.email.get() and self.password.get() and self.confirm_password.get()) is not "":
            self.incorrect_label.config(text="Fill out your information")

            self.email_lblframe.config(bootstyle='danger')
            self.email_ent.config(bootstyle='secondary')

        # Add error message text under the register label that says "This email address is already in use"
        elif isAccount(self.email.get(), self.password.get()):
            self.incorrect_label.config(text="This email address is already in use!")
            
            # Change the label frame widget color to red
            self.email_lblframe.config(bootstyle='danger')

            # Change the entry widget color to gray
            self.email_ent.config(bootstyle='secondary')


            

            return
        
        # Add error message text under the register label that says "Passwords do not match"
        elif not isConfirmed(self.email.get(), self.password.get(), self.confirm_password.get()):
            self.login_label.config(text="Register your account")
            self.incorrect_label.config(text="Passwords do not match")

            # Remove the big 'Sign in to your account' Text
            self.lg_login_label.place_forget()

            return
        
        
        # Change the email and password label frames color to red 
        else:
            # Change the labelframes from blue to red
            self.email_lblframe.config(bootstyle='danger')
            self.password_lblframe.config(bootstyle='danger')

            # Add some gray highlight on the entry widgets
            self.email_ent.config(bootstyle='secondary')
            self.password_ent.config(bootstyle='secondary')

            # Add error message text under the register label
            self.incorrect_label.config(text="The email address or password you entered is incorrect")
            self.incorrect_label2.config(text="or the account does not exist")

            # Append this to the txt file


            # Remove the big 'Sign in to your account' Text
            self.lg_login_label.place_forget()

    def isEmailAddress(self, email) -> bool:
            """
            Validate if an email address is valid or not

            Parameters:
            email (str): Email address to validate

            Returns:
            bool: True if email is valid, False otherwise
            """

            # Regular expression pattern for email validation
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            # Check if email matches pattern
            if re.match(pattern, email):
                return True
            else:               
                return False
            
            

    # Forgot password button function
    def forgotPassword(self):
        pass

    # Register account button function
    def registerAccount(self):
        pass    
     
if __name__ == "__main__":
    root = Register()
    root.mainloop()

    # Update Style
    # def dontExist(self):
    #     self.lblframe_ref = 'danger.TLabelframe'
    
    
        
    
