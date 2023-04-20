from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.validation import *
import ttkbootstrap.style as tbs
import ttkbootstrap.scrolled as tbsc
import tkinter.scrolledtext as tct
import ttkbootstrap.tooltip as tbt

# Import all necessary files
from ComposeEmail import *

class Homepage(tb.Toplevel):
    def __init__(self, email) -> None:
        # configure the root window
        super().__init__(resizable=(False, False))
        self.title("Homepage")
        self.geometry('1700x1050')
    
        # form variables
        self.email = email
        self.valid_colours = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
        

        # Creating the navigation frame (the grey frame)
        self.nav_frame = tb.Frame(self) # maybe secondary?
        self.grid_rowconfigure(0, weight=1) # Expands the frame to the bottom of the window
        self.grid_columnconfigure(0, weight=1) # Makes the first column expandable

        self.nav_frame.grid(row=0, column=0, sticky='nsew', rowspan=2, columnspan=1) # Set navigation frame location on window
        
        self.inner_frame = tb.Frame(self, bootstyle='secondary') # Create inner frame widget
        self.inner_frame.grid(row=0, column=1, sticky='nsew', rowspan=2, columnspan=3) # Set inner frame location to window

        self.search_frame = tb.Frame(self.inner_frame, bootstyle='secondary') # Create search frame widget
        self.list_frame = tbsc.ScrolledFrame(self.inner_frame, bootstyle='dark', autohide=True) # Create scrolled frame widget
        
        self.mail_frame = Frame(self.inner_frame, highlightthickness=1, highlightbackground="#474747", bg='white') # Create mail frame widget
        
        self.grid_columnconfigure(1, weight=11) # Makes the second column non-expandable
        self.grid_rowconfigure(1, weight=1) # Expands the frame to the bottom of the window

        self.inner_frame.grid_rowconfigure(0, weight=1) # Giving the search frame 1/10 of the entire space
        self.inner_frame.grid_rowconfigure(1, weight=9) # Giving the list frame 9/10 of the entire space
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=2)


        # Set search and list frames locations on window
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
            padx=25,
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

        self.sent = self.button(
            self.nav_frame,
            'Sent',
            'light',
            'outline',
            self.sentEmails,
            13,
            pady=45
        )
        
        # List of all the buttons that won't have any functionality in the program (Merely design purposes)
        button_details = [
            ("Starred", "secondary", "outline", None, 13, "disabled"), # Starred button
            ("Drafts", "secondary", "outline", None, 13, "disabled"), # Drafts button
            ("Trash", "secondary", "outline", None, 13, "disabled") # Trash button
        ]

        # Loop through the dictionary and create a button for each key-value pair
        for label, colour, style, command, fontsize, state in button_details:
            btn = self.button(self.nav_frame, label, colour, style, command, fontsize, state=state)
            self.toolTip(btn)
            
        # Add a search entry widget
        self.search = tb.Entry(self.search_frame, bootstyle='dark', takefocus=True)
        self.search.insert(0, "Search")
        self.search.config(font=("Quicksand", 14, 'bold'), state='readonly')
        self.search.pack(fill='x', padx= (12,1000), pady=17)
        self.toolTip(self.search)

        # List emails
        self.createList(self.list_frame, 'inbox')

        # Default text on mail_frame
        self.default_text = tb.Label(self.mail_frame, text='Select an item to read', font=("Quicksand", 13, 'bold'), bootstyle='light')
        self.default_text.pack(fill='y', expand=True)


    def toolTip(self, widget):
        # Create a tooltip when a user hovers over a widget
        tbt.ToolTip(widget, text="This feature will be updated soon", bootstyle='secondary-inverse')
    
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

        # Configure the button style
        btn_style.configure(reference, font=("Quicksand", fontsize, 'bold'))

        # Create the button widget
        btn = tb.Button(widget,
                        text=label, 
                        command=command, 
                        takefocus=False)
        btn.configure(bootstyle=f'{colour}, {type}', style=reference, state=state)

        # Pack the button and any additional arguments
        btn_misc = {
            'padx' : 25,
            'pady' : 45,
            'side' : 'top'
        } | pack
        btn.pack(fill=X, **btn_misc)

        # Return the button widget
        return btn
    
    def createList(self, widget, type: str):
        # Open the email database file and read its contents
        with open("emaildatabase.txt", 'r') as f:
            contents = f.read()

        # Split the contents of the file into a list of emails using regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        emails = re.split(r"(?<=\n\n)(?=\S+@[^\s@]+\.[^\s@]+\b)", contents)

        # Iterate through each email in the list. 
        for email in emails:
            # Use regex to find the receiver's email and split the email into different parts
            components = email.split('\n')
            sender = components[0]
            receiver = ''
            subject = ''
            content = ''

            for i in range(1, len(components)):
                if re.match(email_pattern, components[i]):
                    receiver = components[i]
                    subject = components[i+1]
                    content = '\n'.join(components[i+2:])
                    break

            # If the receiver is not equal to the logged in email and is 'inbox', skip this email
            if type == 'inbox':
                text = sender
                if self.email != receiver:
                    continue
            
            # If the sender is not equal to the logged in email and is 'sent', skip this email
            elif type == 'sent':
                text = receiver
                if self.email != sender:
                    continue

            # Create a Label widget and insert the sender and the subject
            sender_label = tb.Label(widget, text=f'{text}', bootstyle = 'secondary-inverse', font=('Quicksand', 14, 'bold'), borderwidth=2)
            sender_label.pack(fill='x')
            subject_label = tb.Label(widget, text=f'{subject}', bootstyle='secondary-inverse', font=('Quicksand', 12))
            subject_label.pack(fill='x', pady=(0,40))

            # Bind the Label widgets to Mouse Click 1 to open the email
            sender_label.bind('<Button-1>', lambda event, s=sender, r=receiver, sub=subject, con=content: self.openEmail(s, r, sub, con))
            subject_label.bind('<Button-1>', lambda event, s=sender, r=receiver, sub=subject, con=content: self.openEmail(s, r, sub, con))

    def create_form_entry(self, label, variable, bootstyle='info', **ent_misc):  
        # Create a new Entry widget with the specified variable.
        ent = tb.Entry(textvariable=variable)

        # Configure the font of the Entry widget to use the Quicksand font with size 12 and bold style.
        ent.config(font=("Quicksand", 12, "bold"))

        # Pack the Entry widget into the parent container with fill=X to expand it horizontally.
        ent.pack(fill=X)

        # Return the Entry widget object.
        return ent
    

    def newEmail(self):  # Open a small window to compose a new email 
        self.withdraw() # Withdraw the current window    
        self.wait_window(ComposeEmail(self.email)) # Wait until ComposeEmail.py is destroyed
        
        # Destroy any children of the list_frame widget
        for child in self.list_frame.winfo_children():
            child.destroy()

        # Create a new list frame for the inbox
        self.createList(self.list_frame, 'inbox')

        self.deiconify() # Show the Homepage window again
        self.update() # Update the window to ensure it is displayed
        
    
    def openInbox(self): # Open the inbox of the emails
        # Delete the email preview list
        children = self.list_frame.winfo_children()

        # Loop through the list and destroy each child widget
        for child in children:
            child.destroy()

        # Get new data and insert it into the list
        self.createList(self.list_frame, 'inbox')
        self.update()

    def sentEmails(self): # Open the emails the sender has sent. 
        # Clear the email preview list
        children = self.list_frame.winfo_children()

        for child in children:
            child.destroy()

        self.createList(self.list_frame, 'sent')
        self.update()
        

    def openEmail(self, sender, receiver, subject, content):
        # Initiate Styling
        style = tb.Style()

        for child in self.mail_frame.winfo_children():
            if hasattr(self, 'st'):
                child.destroy()

        # Open the email from the email preview
        self.st = tct.ScrolledText(self.mail_frame, highlightbackground=style.colors.dark, highlightthickness=2)
        self.st.pack(fill='both', expand='yes')
        
        # Destroy the default text
        self.default_text.destroy()

        # Combine the text and the styling of the text into one dictionary
        text_style = {
            f'From: {sender}\n\n' : 'bold',
            f'To: {receiver}\n\n' : 'bold',
            f'Subject: {subject}\n\n' : 'bold',
            f'{content}' : 'normal'
        }

        # Add the text and its styling to every line
        for text, style in text_style.items():
            self.st.insert(INSERT, text, style)
        
        self.st.tag_config("bold", font=('Quicksand', 15, 'bold')) # Set the text to 'bold'
        self.st.tag_config("normal", font=('Quicksand', 15)) # Set the text to 'normal'

        # Make ScrolledText read-only
        self.st.config(state=DISABLED)