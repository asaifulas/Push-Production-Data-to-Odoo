import os
from tkinter import Label, ttk, scrolledtext, messagebox, filedialog as fd
from tkinter.constants import END
from ttkthemes import ThemedTk
import odoorpc
import csv
  
url = "URL"
db = "db-name"

class utama():
    def __init__(self):
        # Create object
        self.username = email.get()
        self.password = passw.get()

        self.odoo = odoorpc.ODOO(url.replace("http://", ""), port=80)
        self.cre = odoorpc.ODOO(url.replace("http://", ""), port=80)
        try:
            self.odoo.login(db, self.username, self.password)
            self.cre.login(db, 'email', 'Pass') #give it full access
            self.window = ThemedTk(theme="arc")

            login.destroy()
            
            self.window.title("OdooPush")
            self.window.geometry("450x750")
            self.window.resizable(0, 0)
            self.window.iconbitmap("icon.ico")

            if (url == "trial url"):
                userlogin = self.username + "(Trial)"
                print('Login Trial')
            else:
                userlogin = self.username + "(Live)"
                print('Login Live')

            #user = self.odoo.env.user
            labelframe = ttk.Labelframe(self.window, text="Account Info")
            labelframe.grid(row=0, column=0, columnspan=4, sticky='w')

            ttk.Label(labelframe, text="User: "+userlogin).grid(row=0, column=0, columnspan=4, sticky="w")
            
            ttk.Label(labelframe, text="Manufacturing ID: ").grid(row=1, column=0, columnspan=1, sticky="w")
            self.var1 = ttk.Entry(labelframe, width=42)
            self.var1.grid(row=1,column=1, columnspan=3)


            workspace = ttk.Labelframe(self.window, text="Work Space")
            workspace.grid(row=2, column=0)

            self.garis = ttk.Label(labelframe, text="------------------------==||==------------------------")
            self.garis.grid(row=2, column=0, columnspan=10)
            self.moname = ttk.Label(labelframe)
            self.moname.grid(row=3, column=0, columnspan=3, sticky="w")
            self.worder = ttk.Label(labelframe)
            self.worder.grid(row=4, column=0, columnspan=3, sticky="w")
            self.wcenter = ttk.Label(labelframe)
            self.wcenter.grid(row=5, column=0, columnspan=3, sticky="w")
            self.qty = ttk.Label(labelframe)
            self.qty.grid(row=6, column=0, columnspan=3, sticky="w")

        
            ttk.Button(self.window, text="Inject", command=self.inject).grid(row=1, column=3)
            ttk.Button(self.window, text="Input", command=self.getfile).grid(row=1, column=0, sticky='w')
            ttk.Button(self.window, text="Ops", command=self.operation).grid(row=1, column=1, sticky='w')
            self.operationtag = ttk.Label(self.window, width=26, text=" ")
            self.operationtag.grid(row=1, column=2, sticky='w')

            ttk.Button(labelframe, text="Find", command=self.findMO).grid(row=1, column=5)

            textframe = ttk.Labelframe(self.window, text="Input", height=180)
            textframe.grid(row=2, column=0, columnspan=5, sticky='w')
            self.textin = scrolledtext.ScrolledText(textframe, width=55, height=27)
            
            self.textin.grid()
            self.labelbawah = ttk.Label(self.window, text="Option")
            self.labelbawah.grid(row=3, column=0, columnspan=5)
            self.labelbawah2 = ttk.Label(self.window, text="Input Configuration")
            self.labelbawah2.grid(row=4, column=0, columnspan=5)

            Label(self.window, text=" ").grid(row=5, column=0, columnspan=5)
            self.pgval = ttk.Label(self.window, text=str(0)+" %")
            self.pgval.grid(row=6, column=0, columnspan=5)
            self.pg = ttk.Progressbar(self.window, orient='horizontal', length=100, mode='determinate')
            
            self.pg.grid(row=7, column=0, columnspan=5 )
            Label(self.window, text=" ").grid(row=8, column=0, columnspan=5)
            ttk.Label(self.window, text="Copyright © **** ").grid(row=9, column=0, columnspan=4, sticky="e")

            self.window.mainloop()

        except:
            messagebox.showerror("Opps", "Wrong Email/Password")
            
    def findMO(self):
        self.moid = int(self.var1.get())
        print("Find MO: "+str(self.moid))
        self.moin = self.odoo.env['mrp.workorder'].browse(self.moid)
        self.moname.config(text="MO Name: "+str(self.moin.production_id.name))
        self.worder.config(text="Work Order: "+str(self.moin.name))
        self.wcenter.config(text="Work Center: "+str(self.moin.workcenter_id.name))
        self.qty.config(text="Quantity: "+str(self.moin.qty_production))
        
    def getfile(self):
        root = ThemedTk(theme="arc")
        root.withdraw()
        try:
            filename = fd.askopenfilename(initialdir = "/",title = "Select a File", filetypes = (("CSV files","*.csv"),))

            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                self.textin.configure(state='normal')
                for row in csv_reader:
                    for col in row:
                        self.textin.insert('end', col)
                        self.textin.insert('end', ",")
                    self.textin.insert('end', "\n")
                #self.textin.configure(state='disabled') 
        except:
            print("No File")
        root.destroy()
        #label_file_explorer.configure(text="File Opened: "+filename)
    def operation(self):
        root = ThemedTk(theme="arc")
        root.withdraw()
        try:
            filename = fd.askopenfilename(initialdir="/operation", title="Select a File", filetypes=(("oPush files", "*.oPush"),))
            self.codein=""
            with open(filename) as opushfile:
                csv_reader =  opushfile.readlines()
                line_count = 0
                name = os.path.basename(filename).split('.')
                self.operationtag.config(text=name[0])
                for row in csv_reader:
                    if (line_count == 0):
                        self.labelbawah.config(text=row.strip('\n\r'))
                    elif(line_count == 1):
                        self.labelbawah2.config(text=row.strip('\n\r'))
                    else:
                        self.codein += row
                        
                    line_count = line_count+1
                #self.textin.insert('end', self.codein)
        except:
            print("No File")
        root.destroy()
            
    def inject(self):
        self.pgval.config(text=str(0)+" %")
        self.pg['value'] = 0
        tinput = self.textin.get('1.0', END).splitlines()
        countline = 1
        print("Start Inject")
        for textline in tinput:
            exec(self.codein, {'cre': self.cre, 'odoo': self.odoo, 'moid': self.moid, 'datain': textline})
            prog = int((countline/len(tinput))*100)
            self.pgval.config(text=str(prog)+" %")
            self.pg['value'] = prog
            countline = countline+1

        print("Finish Inject")

# Create object
login = ThemedTk(theme="arc")
  
# Adjust size
login.title("Login")
login.geometry("280x60")
login.iconbitmap("icon.ico")
login.resizable(0, 0)

ttk.Label(login, text="Email: ").grid(row=0, column=0, columnspan=1, sticky="w")
email = ttk.Entry(login)
email.grid(row=0, column=1, columnspan=3)
ttk.Label(login, text="Password: ").grid(row=1, column=0, columnspan=1, sticky="w")
passw = ttk.Entry(login, show="*")
passw.grid(row=1, column=1, columnspan=3)
ttk.Label(login, text=" ").grid(row=2, column=0, columnspan=1, sticky="w")
ttk.Button(login, text="Login", command=utama).grid(row=1, column=4, sticky="")

login.mainloop()