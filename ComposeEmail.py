from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.validation import *
import ttkbootstrap.style as tbs
import ttkbootstrap.scrolled as tbsc
import tkinter.scrolledtext as tct
import ttkbootstrap.tooltip as tbt

import os
# Import all necessary files


# from tkextrafont import font

class ComposeEmail(tb.Toplevel):
    def __init__(self, sender) -> None:
        # configure the root window
        super().__init__(resizable=(False, False))
        self.title("Compose Email")
        self.geometry('900x900')

        # form variables
        self.sendto = tb.StringVar(value="")
        self.subject = tb.StringVar(value="")
        self.sender = sender
        self.content = tb.StringVar(value="")
        

        # Sign in to your account text
        compose_label = tb.Label(self, text = "Compose New Email", font=("Quicksand", 18, "bold"))
        compose_label.pack(pady=(32,0))

        # Error message telling the user email/password doesn't exist
        self.incorrect_label = tb.Label(self, text = "", font=("Quicksand", 10, "bold"))
        self.incorrect_label2 = tb.Label(self, text = "", font=("Quicksand", 10, "bold"))
        
        # Pack the error messages
        self.incorrect_label.pack(pady=(0,0))
        self.incorrect_label2.pack(pady=(0,0))

        # Hide the email and password error message
        self.incorrect_label.pack()
        self.incorrect_label2.pack()

        # Big Sign in to your account text
        self.lg_compose_label = tb.Label(self, text = "Compose New Email", font=("Quicksand", 20, "bold"))
        self.lg_compose_label.place(x=250, y=50)

        self.receiver_ent = self.createEntry(self, self.sendto, 'info', 'To', fontsize=13)
        self.subject_ent = self.createEntry(self, self.subject, 'info', 'Subject', fontsize=13)
        self.content_txt = self.createText(self, self.content, 'info', fontsize=13)
        self.submit_btn = self.button('Submit', 'solid', self.submit, fontsize=13)

# def button(self, label, type, command, fontsize=12, **pack):

        
        

        # Bind Enter to press Sign In
        # self.sign_in.config(takefocus=True)
        # self.sign_in.bind('<Return>', lambda event: self.signIn())
        # self.sign_in.focus_set()

            
    def createEntry(self, widget: tb.Window, variable: tb.StringVar, colour: str, placeholder: str, fontsize=12, **ent_misc) -> tb.Entry:
        ent_style = tb.Style()
        reference = 'secondary.TEntry'
        

        def addPlaceholder(event=None):
            if variable.get() == '':
                reference = 'secondary.TEntry'
                ent.configure(style=reference)
                ent.delete(0, 'end')
                ent.insert(0, placeholder.title())
        
        def removePlaceholder(event=None):
            reference = f'{colour}.TEntry'
            ent.configure(style=reference)
            if variable.get() == placeholder.title():
                ent.delete(0, 'end')


        ent = tb.Entry(widget, textvariable=variable, style=reference)
        ent.configure(font=('Quicksand', fontsize, 'bold'))
        
        # Add placeholder text
        ent.insert(0, placeholder.title())

        # Bind the Entry widget to the 'Focus in' event to remove the placeholder
        ent.bind('<FocusIn>', removePlaceholder)
        # Bind the Entry widget to the 'Focus out' event to add the placeholder
        ent.bind('<FocusOut>', addPlaceholder)

        ent_misc = {
            'padx' : 60,
            'pady' : 15,
            'side' : 'top'
        }
        ent_misc |= ent_misc

        ent.pack(fill='x', **ent_misc)

        return ent

    def createText(self, widget: tb.Window, variable: tb.StringVar, colour: str, fontsize=12, **txt_misc) -> tct.ScrolledText:
        self.txt_style = tb.Style()
        
        # Update the content everytime it changes
        def update_contents(*args):
            self.content.set(txt.get('1.0', 'end-1c'))
            # .config(text=self.content.get())
    
        txt = tct.ScrolledText(self, highlightbackground=self.txt_style.colors.get(colour), highlightthickness=3, font=("Quicksand", 13), height=10)
        txt.tag_config('normal', font=('Quicksand', fontsize))
        
        # Bind the update_content function to the scrolled text widget
        txt.bind('<<Modified>>', update_contents)

        # Set the scrolled text widget to modify the content variable whenever it changes
        txt.bind('<KeyRelease>', lambda event: txt.event_generate('<<Modified>>'))

        # Set the initial value of the content variable
        self.content.set(txt.get('1.0', 'end-1c'))
        
        txt_misc = {
            'padx' : 60,
            'pady' : 30,
            'side' : 'top'
        }
        txt_misc |= txt_misc
        txt.pack(fill='x', **txt_misc)
        


        return txt
 
    
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
    def submit(self):
        # Check if the file exists
        if not os.path.isfile('emaildatabase.txt'):
            # If the file doesn't exist, create a new one
            with open('emaildatabase.txt', 'w') as f:
                f.write('')

        # Get the content in the Scrolled Text widget
        def storeEmail(txt : tct.ScrolledText):
            content = txt.get('1.0', 'end').strip()
            
            with open('emaildatabase.txt', 'r') as contents:
                save = contents.read()

            with open('emaildatabase.txt', 'w') as contents:
                contents.write(f"{self.sender}\n{self.sendto.get()}\n{self.subject.get()}\n{content}\n\n")

            with open('emaildatabase.txt', 'a') as contents:
                contents.write(save)


            self.destroy()

        # If email address is wrong 
        if not self.isEmailAddress(self.sendto.get()):
            # Change the Entry widget from grey to red
            self.receiver_ent.config(bootstyle='danger')

            # Add error message text under the register label
            self.incorrect_label.config(text="The email address entered is not in the correct form", bootstyle = 'danger')

            # Remove the big 'Sign in to your account' Text
            self.lg_compose_label.place_forget()
            return
        
        # If message is empty
        elif not self.content:
            # Change the border colour to red
                self.content_txt.config(highlightbackground=self.txt_style.colors.get('danger'))
                # Add error message to the incorrect label
                self.incorrect_label.config(text="The message does not contain any text", bootstyle='danger')
                # Hide the large compose label
                self.lg_compose_label.place_forget()


        # If everything passes
        else:
            storeEmail(self.content_txt)



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