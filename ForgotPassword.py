from tkinter import *
import ttkbootstrap as tb
import os

class ForgotPassword(tb.Toplevel):
    def __init__(self) -> None:
        # configure the root window
        super().__init__(resizable=(False, False))
        self.title("Password Reset")
        self.geometry('600x650')

        # form variables
        self.email = tb.StringVar(value="")
        self.password = tb.StringVar(value="")
        self.confirm_password = tb.StringVar(value="")
        self.changed = False
   
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
        self.lg_login_label = tb.Label(self, text = "Reset your password", font=("Quicksand", 22, "bold"))
        self.lg_login_label.place(x=65, y=40, height=100)

        self.email_lblframe, self.email_ent = self.create_form_entry("Your email", self.email)

        self.password_lblframe, self.password_ent = self.create_form_entry("New Password", self.password, pady=(30,50))
        self.confirm_password_lblframe, self.confirm_password_ent = self.create_form_entry("Confirm new password", self.confirm_password, pady=(30,100))

        self.change_password = self.button("Change Password", "solid", self.changePassword, pady=(25,0))

    
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
    def changePassword(self):

        # Add the text Reset your password
        self.login_label.config(text="Reset your password")

        # Remove the big 'Reset your password' text
        self.lg_login_label.place_forget()

        def hasValue(email, password, confirm_password) -> bool:
            if (email and password and confirm_password) != "":
                print('It has value!')
                return True
            print("It doesn't have value!")
            return False

        # To check whether email and password exists in the user data 
        def isAccount(email) -> bool:
            
            # Check if the file exists
            if not os.path.isfile('userdata.txt'):
                # If the file doesn't exist, create a new one
                with open('userdata.txt', 'w') as f:
                    f.write('')

            # Open the file for reading
            with open('userdata.txt', 'r') as data:
                for line in data:
                    if not line:
                        continue
                    #Split the line into email and password using ','
                    stored_email, _ = line.strip().split(',')

                    # Check if the email and password match
                    if email == stored_email:
                        print("Email does exist!")
                        return True
            print("Email doesn't exist")
            return False
        
        def editAccount(email, new_password):
            # Check is the file exists 
            if not os.path.isfile('userdata.txt'):
                # If the file doesn't exist, create a new one
                with open('userdata.txt', 'w') as f:
                    f.write('')
            
            # Open the file for reading
            with open('userdata.txt', 'r') as data:
                lines = data.readlines()
            
            # Check if the email exists in the file
            index = -1
            for i in range(len(lines)):
                if email in lines[i]:
                    index = i
                    break
            
            if index == 1:
                print("Email does not exist!")
                return

            # Overwrite the old password with the new password
            lines[index] = f'{email},{new_password}\n'

            # Write the modified lines back to the file
            with open('userdata.txt', 'w') as data:
                data.writelines(lines)
        

        # To check whether the email and password matches with the verification entries
        def isConfirmed(password, confirm_password) -> bool:
            if password == confirm_password:
                print("It is confirmed!")
                return True
            print("It is not confirmed!")
            return False

        # If email, password and confirm_password has any value
        if not hasValue(self.email.get(), self.password.get(), self.confirm_password.get()):
            self.incorrect_label.config(text="Fill out the required information")

            # Change the labelframe colour to red
            self.email_lblframe.config(bootstyle='danger')
            self.password_lblframe.config(bootstyle='danger')
            self.confirm_password_lblframe.config(bootstyle='danger')

            # Change the highlight to grey of the entry widgets
            self.email_ent.config(bootstyle='secondary')
            self.password_ent.config(bootstyle='secondary')
            self.confirm_password_ent.config(bootstyle='secondary')

            # Return null to avoid running the other functions
            return

        # If email address exists in the user data.txt
        elif not isAccount(self.email.get()):
            # Add error message text under the register label that says "This email address is already in use"
            self.incorrect_label.config(text="This email does not exist in our records!")
            
            # Change the label frame widget color to red
            self.email_lblframe.config(bootstyle='danger')

            # Change the entry widget color to grey
            self.email_ent.config(bootstyle='secondary')

            # Return null to avoid running the other functions
            return
        
        # If password !== confirm_password
        elif not isConfirmed(self.password.get(), self.confirm_password.get()):
            # Add error message text under the register label that says "Passwords do not match"
        
            self.incorrect_label.config(text="Passwords do not match")

            # Remove the big 'Sign in to your account' Text
            self.lg_login_label.place_forget()

            # Return null to avoid running the other functions
            return
        
        # If everything is right
        elif (isAccount(self.email.get())) and isConfirmed(self.password.get(), self.confirm_password.get()) and hasValue(self.email.get(), self.password.get(), self.confirm_password.get()):
            # Append this to the txt file
            editAccount(self.email.get(), self.password.get())
            self.changed = True
            self.destroy()

            return True