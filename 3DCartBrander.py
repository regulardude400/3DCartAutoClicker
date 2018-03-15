import sys, re, os, importlib, win32com.client as win32
from gui3DCart import Ui_MainWindow
from PyQt5 import QtWidgets, uic, QtCore

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        
        #Load the GUI
        super(Ui, self).__init__()
        uic.loadUi('dialog.ui', self)
        self.show()

        #variables used to store the merchant's information.
        self.Gemail = ""
        self.Gtransid = ""
        self.Gusername = ""
        self.Gcontrolp = ""
        self.Gusernamep = ""
        self.Gpasswordp = ""
        self.Ghostftp = ""
        self.Gloginftp = ""
        self.Gpassftp = ""
        
        #Program Functions
        self.ClearTextBox.clicked.connect(self.clearText) #Clear text
        self.SaveTextToFile.clicked.connect(self.saveText)#Save text to file
        self.StartProgram.clicked.connect(self.runScript) #Runs the main script
        self.actionQuit.triggered.connect(self.quitProgram) #Quits Program
        self.actionAbout.triggered.connect(self.aboutProgram) #Open About in Menu
        
    def aboutProgram(self):
        infoAbout = QtWidgets.QMessageBox() ##Message Box that doesn't run
        infoAbout.setIcon(QtWidgets.QMessageBox.Information)
        infoAbout.setWindowTitle("About 3DCart Brander v1.0")
        infoAbout.setInformativeText("This program was created by Alvin Williams."
                                     "If you need help or troubleshooting please report"
                                     "the issues to me in person, via email alvin.williams1992@yahoo.com"
                                     "or via github using the issue tracker located here:\nhttps://github.com/regulardude400/3DCartBrander/issues")
        infoAbout.exec()
        
    def quitProgram(self):
        sys.exit() #Quit the program
        
    def runScript(self):
        self.parseEmail() #Parse the text file.
        self.createEmail() #Create the email to send and open it in outlook.
        self.sendftp() #Copy the necessary files to the merchant's 3dcart ftp

    def clearText(self):
        self.EmailTextBox.clear() #Clear the 3D Cart Email Text Box
            
    def saveText(self):
            with open("3dcart_info_Goes_Here.txt", 'w') as file: #Open the file
                    my_text = self.EmailTextBox.toPlainText() #Set the text to write
                    file.write(my_text) #Write that text to a file
                    file.close() #Close the file.
                    
    def parseEmail(self):
            try:
                    with open("3dcart_info_Goes_Here.txt", 'r') as file:
                            for i, lines in enumerate(file):
                                    
                                    #transaction center id credentials
                                    transid = re.search(r'TranCenter', lines)
                                    if transid:
                                            self.Gtransid = lines[15:]

                                    #email
                                    emailTo = re.search(r'Email address for merchant is', lines)
                                    if emailTo:
                                             self.Gemail = lines[31:]
                                             
                                    username = re.search(r'User Name', lines)
                                    if username:
                                            self.Gusername = lines[11:]
                                            
                                    #control panel 3d cart credentials
                                    controlp = re.search(r'Your control panel:', lines)
                                    if controlp:
                                            self.Gcontrolp = lines[21:]
                                            
                                    usernamep = re.search(r'Your username:', lines)
                                    if usernamep:
                                            self.Gusernamep = lines[16:]

                                    passwordp = re.search(r'Your password:', lines)
                                    if passwordp:
                                            self.Gpasswordp = lines[16:]
                                        
                                     #ftp settings
                                    hostftp = re.search(r'com\.3dcartstores\.com', lines)
                                    if ((hostftp) and i in range(40,70)):
                                            self.Ghostftp = lines[:-2]
                                            
                                    loginftp = re.search(r'\|', lines)
                                    if loginftp:
                                            self.Gloginftp = lines[7:-2]
                                            
                                    passftp = re.search(r'Password:', lines)
                                    if passftp and i in range(40,70):
                                            self.Gpassftp = lines[10:-2]
                            file.close()

            except IOError:
                    file = open("3dcart_info_Goes_Here.txt", 'w')
                    file.write("\\DELETE ME WITH 3DCart INFO FROM EMAIL IN OUTLOOK")
                    print("Please paste the 3D cart information in the file 3dcart_info.txt. "
                          "This file has been created for you in the same directory "
                          "where you ran the script or program.\n")
                    input('Press ENTER to exit')
                    exit()
                
    def createEmail(self):
        outlook = win32.Dispatch('outlook.application') #Open Outlook
        mail = outlook.CreateItem(0) #Create an email.
        mail.To = self.Gemail #Send to Merchant's email that we have parsed.
        mail.Subject = "Welcome to goEmerchant!" #Subject of email.
        text = """Greetings!

We have initiated your iteration of the Premium cart and following are the login credentials.  There is a migration process we’ll coordinate with you before your new Premium cart will be introduced to your customers.  In the interim your existing Total Package or Buy-Me Buttons will continue to provide the sales on your e-commerce site(s).  

You’ll enjoy the Premium cart benefits which include a responsive design which makes it easy for your customers to purchase on a mobile device, and many contemporary advanced e-commerce features and capabilities.  

The main phases of the migration process we’ll perform are: 
•         Initiate the Premium cart
•         Transfer any Total Package images
•         Transfer any Total Package departments (categories)
•         Transfer Total Package products
•         Forward the Buy-Me Buttons to the new platform

The migration will require some effort on your part to verify all data transferred and: 
•         Configure sales tax, shipping methods, email and other settings
•         Total Package merchants using the full e-commerce site will need to select a template and design their layout
•         Perform test transactions to validate the checkout process and order notifications 
 
Please note the final migration will be coordinated with you and will not occur without your knowledge and consent.    

Your loyalty as a respected long term merchant is very much appreciated.  

Your new shopping cart has been set up!  You will need to log into your GoEmerchant Transaction Center to set up your payment gateway and accept payments through your 3dCart store.

Transaction Center Login Information:

Transaction Center ID: """ + self.Gtransid + """Username: """ + self.Gusername + """Password: [Refer to your activation email or call 888-711-3800 opt tech support]

To log into your Transaction Center, go to this link: https://secure.goemerchant.com/secure/login/tc/login.aspx Enter your login credentials, and click Login.  For full instructions on logging into your Transaction Center, please see this support article: http://support.goemerchant.com/transaction-center.aspx?article=account-setup 

Once logged into your Transaction Center, go to the Security Settings Tab and Select Gateway Options.  You will need to enter your Transaction Center ID, Processor ID, and Gateway ID in your Online Payment Options in the store, so keep this page open.

To log into your 3dCart store, go to:\n""" + self.Gcontrolp + """Username: """ + self.Gusernamep + """Password: """ + self.Gpasswordp + """
FTP Information (Only necessary for making template changes):
Server/Host: """ + self.Ghostftp + """\nUsername: """ + self.Gloginftp + """\nPassword: """ + self.Gpassftp + """\nUpon first login to your store, you will be presented with a Setup Tutorial.  You may follow the steps outlined in the tutorial, or in this setup article to set up your cart: http://support.goemerchant.com/shopping-cart-software.aspx?article=shopping-cart-setup-guide 

From the Store Manager in Settings > Payment > Online Methods, you will need to enter your Transaction Center ID, Gateway ID and Processor ID to accept credit cards.  Details on this step can be found here: http://support.goemerchant.com/shopping-cart-software.aspx?article=shopping-cart-setup-guide#online-payment-methods 

If you are using a custom URL, you will need to configure an A Record in your domain name’s DNS settings.  Instructions on how to do so can be found here:
http://support.goemerchant.com/shopping-cart-software.aspx?article=setting-up-custom-url 

If you need any assistance, please contact Support at (888) 711-3800, or by email at support@goemerchant.com.  

Thank you,
Alvin

GoEmerchant Tech Support
support@goemerchant.com
Phone: 888-711-3800 Opt 3
Fax: 866-926-4499
"""
        mail.Body = text #Set body to the text above.
        if mail.Display(False): #Open the email that we want to compose to outlook.
           mail.Display(True)

    def sendftp(self):
        #This method is for writing the script that will be read by winscp.
        #At the end we will invoke the program with cmd and tell winscp to read
        #the script that we create in this method.
        
        text2write = "open \"ftps://" + self.Gloginftp + ':' + self.Gpassftp +'@'+ self.Ghostftp + '\"\n'
        text2write += 'cd /keys\n'
        text2write += 'put "F:\Company Shared Folders\Tech Support\\3dCart Branding\gw_ids.txt"\n'
        text2write += 'put "F:\Company Shared Folders\Tech Support\\3dCart Branding\gw_ids1.txt"\n'
        text2write += 'cd ../web/assets\n'
        text2write += 'put "F:\Company Shared Folders\Tech Support\\3dCart Branding\\brandv7"\n'
        text2write += "exit"
        
        with open("scpScript.txt", 'w') as scpfile:
            scpfile.write(text2write)
            scpfile.close()
                
        dirScpFile = os.path.realpath(scpfile.name)
        result = '"' + dirScpFile + '"'
        command = "winscp.com /script=" + result
        os.system("start cmd /k " + command)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
