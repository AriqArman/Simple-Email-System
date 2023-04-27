# Simple Email System

A Simple Email GUI System using Python's Tkinter Module and TTKBootstrap.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ttkbootstrap.
```bash
pip install ttkbootstrap
```
## Usage
To run the Email System Application, follow these steps:
1. Make sure you have Python 3 installed on your computer 
2. Clone the repository: `git clone https://github.com/AriqArman/Simple-Email-System.git`
3. Navigate to the project directory
4. Open the `EmailApppy` file in your Python IDE of choice
5. Run the program by clicking the "Run" button or using the keyboard shortcut for your IDE

## Examples
Here's an example of how to use the Email System:
1. (Optional) Download the [Quicksand](https://fonts.google.com/specimen/Quicksand) font 
2. Launch the program by following the steps above
3. Enter your email address and password when prompted
4. Select the "COMpose Email" option from the menu
5. Enter the recipient's email address, a subject line, and the body of the email.
6. Click "Send" to send the email.

## Troubleshooting
1. I've altered or modified the userdata.txt and now the program doesn't work
  - The `userdata.txt` file follows the format:
  `(user's email address),(user password)
  `
  - The new line (`\n`) at the bottom is **necessary** and should **not** be removed from the text file

2. I've altered or modified the emaildatabase.txt and now some of the email contents are missing
  - The `emaildatabase.txt` file follows the format:
  ```
  (sender address)
  (recipient address)
  (subject heading)
  (email content)
  
  (sender address)
  ...
  ```
  - The new line (`\n`) followed by the `sender address` is **necessary** and should **not** altered as well. 

3. Some of the content in the email are missing
  - If an email content contains a newline (`\n`) statement followed by an email address, the email address and the content following that would not be displayed in the program 
    - This is due to a Regex expression where the emails are split once it meets a new line statement (`\n`) adjacent to an email address. 
    - If you found out the hard way, open the `emaildatabase.txt` file and remove the entire email which is positioned at the top of the text file.
    - To put it simply: avoid adding an email address in the content section when composing a new email

4. Starred, Drafts, Trash and Search don't work. Why?
  - Those features are not implemented in this program as it is desgined to be a purely _Simple_ Email System. 
  - The reason of adding these buttons and search bar is purely for **design purposes** as without them, the program would look empty and pale.
    - If you hover over the buttons, a tooltip appears saying "This feature will be updated soon"

5. Why are the placements of the widgets completely wrong?
  - The placement of the widgets are caused by the differences of monitor screen sizes as well as the resolution. 
  - If you are running this program on a 1920x1080 screen, it is most likely that the widgets and their placements are not user friendly at all. 
  - To see the true design of this program, watch the Demonstration Video file attached in this repository.

6. Are you planning to improve on this program more?
  - As things currently stand, improving the program by adding additional functionalities would make the user experience better. However, I plan on to moving to different projects specifically web development as it prevents placement issues as mentioned as well as custom font issues.


