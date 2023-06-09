from tkinter import *
import ttkbootstrap as tb
import os

# Import all necessary files
from Register import *
from ForgotPassword import *
from Homepage import *

class Login(tb.Window):
    def __init__(self) -> None:
        # configure the root window
        super().__init__(themename='darkly', resizable=(False, False))
        self.title("Login")
        self.geometry('600x650')

        # form variables
        self.email, self.password = tb.StringVar(value=""), tb.StringVar(value="")

        # Sign in to your account text
        tb.Label(self, text = "Sign in to your account", font=("Quicksand", 18, "bold")).pack(pady=(32,0))

        # Error message telling the user email/password doesn't exist
        self.incorrect_label = tb.Label(self, text = "", font=("Quicksand", 10, "bold"))
        self.incorrect_label2 = tb.Label(self, text = "", font=("Quicksand", 10, "bold"))
        
        # Pack the error messages
        self.incorrect_label.pack(pady=(0,0))
        self.incorrect_label2.pack(pady=(0,0))

        # Big Sign in to your account text
        self.lg_login_label = tb.Label(self, text = "Sign in to your account", font=("Quicksand", 20, "bold"))
        self.lg_login_label.place(x=80, y=50)

        self.email_lblframe, self.email_ent = self.create_form_entry("Your email", self.email)
        self.password_lblframe, self.password_ent = self.create_form_entry("Password", self.password, pady=(30,100))
        self.forgot_password = self.button("Forgot password?", 'link', self.openForgotPassword, 11, padx=(287,0), pady=0, side='top')
        self.sign_in = self.button("Sign In", "solid", self.signIn, pady=(15,0))

        self.signup_label = tb.Label(self, text = "Don't have an account yet?", font=("Quicksand", 11, "bold"))
        self.signup_label.pack(side='left', padx=(110,0), pady=(0,60))
        self.signup_button = self.button("Sign up", "link", self.openRegisterAccountWindow, 11, padx=(0,80), pady=(0,60), side='left')

    # Forgot password button function
    def openForgotPassword(self):
        self.closeCurrentOpenNew(ForgotPassword) # Open ForgotPassword.py

    # Register account button function
    def openRegisterAccountWindow(self):
        self.closeCurrentOpenNew(Register) # Open Register.py

    def closeCurrentOpenNew(self, window):
        '''
        Close the current window and open a new window of the specified type.

        Parameters: 
        window (python file) : The Python file containing the new window class to be executed.

        Returns:
        None
        '''

        self.withdraw() # Close the current window
        self.wait_window(window()) # Wait until window is destroyed 
        self.deiconify() # Show the sign in window again
        self.update() # Update the window to ensure it is displayed

    def create_form_entry(self, label, variable, bootstyle='info', **ent_misc):  
        
        lblframe = tb.LabelFrame(self, text=label.title(), bootstyle=bootstyle)
        ent_misc = {'padx' : 60, 'pady' : (15,25), 'side' : 'top'}
        ent_misc |= ent_misc
        lblframe.pack(fill=X, **ent_misc)

        ent = tb.Entry(lblframe, textvariable=variable)
        ent.config(font=("Quicksand", 12, "bold"))

        ent.pack(fill=X)

        if variable == self.password:
            ent.config(show="*")

        return lblframe, ent
 
    def button(self, label, type, command, fontsize=12, **pack):
        # Check whether the type arg is valid
        btn_style = tb.Style()
        if type == "link":
            reference = 'primary.Link.TButton'
        elif type == "outline":
            reference = 'primary.Outline.TButton'
        elif type == "solid":
            reference = 'primary.TButton'
        else:
            raise TypeError("Type does not exist. Choose any from 'solid', 'outline', or 'link'")

        btn_style.configure(reference, font=("Quicksand", fontsize, 'bold'))

        btn = tb.Button(self, text=label, command=command, takefocus=False)
        btn.configure(bootstyle=f'primary, {type}', style=reference)

        btn_misc = {'padx': 60, 'pady': 30, 'side': 'top'} | pack
        btn.pack(fill=X, **btn_misc)

        return btn
    
    # Sign in button function
    def signIn(self):
        # To check whether email and password exists in the user data 
        def isAccount(email, password):
            with open('userdata.txt', 'r') as data:
                for line in data:
                    #Split the line into email and password using ','
                    stored_email, stored_password = line.strip().split(',')

                    # Check if the email and password match
                    if email == stored_email and password == stored_password:
                        return True
            return False
    
        # Check if the file exists
        if not os.path.isfile('userdata.txt'):
            # If the file doesn't exist, create a new one
            with open('userdata.txt', 'w') as f:
                f.write('')
                
        # Destroy the root window if the credentials match
        if isAccount(self.email.get(), self.password.get()):        
            self.withdraw() # Close the current window

            self.wait_window(Homepage(self.email.get())) # Wait until Homepage.py is destroyed

            # Clear the password entry widgets
            self.password = tb.StringVar(value="")
            self.destroy()
        
        # Change the email and password label frames color to red 
        else:

            # Combine the Labelframe widget and Entry widget into a dictionary
            lblframe_ent_widgets = {
                self.email_lblframe : self.email_ent,
                self.password_lblframe : self.password_ent
            }

            for lblframe, ent in lblframe_ent_widgets.items():
                lblframe.config(bootstyle='danger') # Change the labelframes from blue to red
                ent.config(bootstyle='secondary') # Add some gray highlight on the entry widgets
            
            # Add error message text under the login label
            self.incorrect_label.config(text="The email address or password you entered is incorrect", bootstyle='danger')
            self.incorrect_label2.config(text="or the account does not exist", bootstyle='danger')

            # Remove the big 'Sign in to your account' Text
            self.lg_login_label.place_forget()

if __name__ == "__main__":
    root = Login()    
    root.mainloop()