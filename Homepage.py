from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.validation import *
import ttkbootstrap.style as tbs
import ttkbootstrap.tooltip as tbt
import os


# Import all necessary files
from Login import *
from Register import *
from ForgotPassword import *

# from tkextrafont import font

class Homepage(tb.Window):
    def __init__(self) -> None:
        # configure the root window
        super().__init__(themename='darkly', resizable=(False, False))
        self.title("Homepage")
        self.geometry('1700x1050')

        # form variables
        self.valid_colours = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']

        # Creating the navigation frame (the grey frame)
        self.nav_frame = tb.Frame(self) # maybe secondary?
        self.grid_rowconfigure(0, weight=1) # Expands the frame to the bottom of the window
        self.grid_columnconfigure(0, weight=1) # Makes the first column expandable


        self.nav_frame.grid(row=0, column=0, sticky='nsew', rowspan=2, columnspan=1)
        

        self.inner_frame = tb.Frame(self, bootstyle='secondary') # Theme colour? # Currently at danger colour for debugging purposes
        self.inner_frame.grid(row=0, column=1, sticky='nsew', rowspan=2, columnspan=3)

        self.search_frame = tb.Frame(self.inner_frame, bootstyle='secondary')
        self.list_frame = tb.Frame(self.inner_frame, bootstyle='danger')
        self.mail_frame = tb.Frame(self.inner_frame, bootstyle='warning')

        self.grid_columnconfigure(1, weight=11) # Makes the second column non-expandable
        self.grid_rowconfigure(1, weight=1) # Expands the frame to the bottom of the window

        self.inner_frame.grid_rowconfigure(0, weight=1) # Giving the search frame 1/10 of the entire space
        self.inner_frame.grid_rowconfigure(1, weight=9) # Giving the list frame 9/10 of the entire space

        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=2)
    


        self.search_frame.grid(row=0, column=0, sticky='nsew', rowspan=2, columnspan=3)
        self.list_frame.grid(row=1, column=0, sticky='nsew', rowspan=2, columnspan=3)
        self.mail_frame.grid(row=0, column=1, sticky='nsew', rowspan=2, columnspan=3)




        # Buttons for the navigation frame
        self.compose = self.button(
            self.nav_frame,
            "Compose", 
            'primary',
            'solid',
            self.newEmail,
            15,
            padx=45,
            pady=60
            )
        
        self.inbox = self.button(
            self.nav_frame,
            "Inbox",
            'light',
            "outline",
            self.openInbox,
            13,
            pady = 45
        )
        
        # List of all the buttons that won't have any functionality in the program (Merely design purposes)
        button_details = [
            ("Sent", "secondary", "outline", None, 13, "disabled"), # Sent button
            ("Starred", "secondary", "outline", None, 13, "disabled"), # Starred button
            ("Drafts", "secondary", "outline", None, 13, "disabled"), # Drafts button
            ("Trash", "secondary", "outline", None, 13, "disabled") # Trash button
        ]

        # Loop through the dictionary and create a button for each key-value pair
        for label, colour, style, command, fontsize, state in button_details:
            btn = self.button(self.nav_frame, label, colour, style, command, fontsize, state=state)
            self.toolTip(btn)
            
    
        # Add a search entry widget
        self.search = tb.Entry(self.search_frame, bootstyle='secondary', takefocus=True)
        self.search.insert(0, "Search")
        self.search.config(font=("Quicksand", 14, 'bold'), state='readonly')
        self.search.pack(fill='x', padx= (25,1000), pady=25)

     
    def button(self, widget, label, colour, type, command, fontsize=12, state='enabled', **pack):
        
        # Check whether colour is valid
        if all(i != colour for i in self.valid_colours):
            raise TypeError("Colour does not exist.")

        # Check whether the type arg is valid
        btn_style = tb.Style()
        if type == "link":
            reference = f'{colour}.Link.TButton'
        elif type == "outline":
            reference = f'{colour}.Outline.TButton'
        elif type == "solid":
            reference = f'{colour}.TButton'
        else:
            raise TypeError("Type does not exist. Choose any from 'solid', 'outline', or 'link'")

        btn_style.configure(reference, font=("Quicksand", fontsize, 'bold'))

        btn = tb.Button(widget, text=label, command=command, takefocus=False)
        btn.configure(bootstyle=f'{colour}, {type}', style=reference, state=state)

        btn_misc = {
            'padx' : 60,
            'pady' : 45,
            'side' : 'top'
        } | pack
        btn.pack(fill=X, **btn_misc)
        return btn
    
    def toolTip(self, widget):
        tbt.ToolTip(widget, text="This feature is not yet available", bootstyle='secondary-inverse')

    def newEmail(self):
        # Open a small window to compose a new email
        pass
    
    def openInbox(self):
        # Open the inbox of the emails
        pass

if __name__ == "__main__":
    root = Homepage()
    root.mainloop()