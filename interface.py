import tkinter as tk
import solver


class App(tk.Tk):
    def __init__(self, title, size, cfont=None):
        super().__init__()
        self.solution = (('*', 0.0))
        self.geometry(f'{size[0]}x{size[1]}')
        self.size = size
        self.bind('<Escape>', self.kill)
        self.resizable(False, False)
        self.title(title)
        self.cfont = cfont
        self.equations = []
        self.eq_entry = []
        self.n = 0
        self.ecanvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.ecanvas.yview)
        self.eframe = tk.Frame(self.ecanvas)
        self.warnings = []

    def kill(self, event):
        self.destroy()

    def step1(self):
        row = tk.Frame(self)
        lab = tk.Label(row, width=30, text='Enter number of equations:', anchor='w')
        lab['font'] = self.cfont
        self.noentry = tk.Entry(row, font=self.cfont)
        self.noentry.insert(0, "2")
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        self.noentry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        btn = tk.Button(self)
        btn['text'] = 'Done'
        btn['width'] = 10
        btn['command'] = self.get_no_of_equations
        btn.pack(side=tk.TOP, pady=20)

    def get_no_of_equations(self):
        self.n = int(self.noentry.get())
        print(f"N = {self.n}")
        self.step2()

    def create_new(self):
        self.equations.clear()
        self.eq_entry.clear()
        self.warnings.clear()
        self.ecanvas.destroy()
        self.scroll_y.destroy()
        self.eframe.destroy()
        del self.ecanvas, self.scroll_y, self.eframe
        self.ecanvas = tk.Canvas(self, bd=0, relief='ridge', highlightthickness=0)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.ecanvas.yview)
        self.eframe = tk.Frame(self.ecanvas)

    def enable_scrolling(self):
        self.ecanvas.create_window(0, 0, anchor='nw', window=self.eframe)
        self.ecanvas.update_idletasks()
        self.ecanvas.configure(scrollregion=self.ecanvas.bbox('all'), yscrollcommand=self.scroll_y.set)
        self.ecanvas.pack(fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)
        self.scroll_y.pack(fill=tk.Y, side=tk.RIGHT)

    def step2(self):
        self.create_new()
        for i in range(self.n):
            row = tk.Frame(self.eframe, padx=self.winfo_width() / 20)
            lab = tk.Label(row, width=20, font=self.cfont, anchor='w')
            lab['text'] = '{} Equation:'.format(i + 1)
            ent = tk.Entry(row, font=self.cfont)
            warning = tk.StringVar()
            # warning.set('Only 1 char variables allowed')
            lab2 = tk.Label(row, fg="red", textvariable=warning)
            self.warnings.append(warning)
            temp = self.cfont.split()
            # print(temp)
            lab2['font'] = temp[0] + ' ' + str(int(temp[1]) - 4) + ' bold'
            del temp
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            lab2.pack(side=tk.RIGHT, expand=1)
            ent.pack(side=tk.RIGHT, fill=tk.X)
            self.eq_entry.append(ent)
        btn = tk.Button(self.eframe, width=15)
        btn['text'] = 'Solve!'
        btn['font'] = self.cfont
        btn['command'] = self.got
        btn.pack(side=tk.LEFT, padx=self.size[0] / 2.5, pady=10)
        self.enable_scrolling()

    def got(self):
        self.get_equations()
        valid = solver.validata_warn(self.equations, self.warnings)
        if not valid:
            self.equations.clear()
        else:
            self.solution = solver.get_solution(self.equations)
            self.display_solution()

        # self.warnings[0].set('guraojoijsfoiajfoi')
        # self.solution = solver.get_solution(self.equations)
        # self.display_solution()

    def get_equations(self):
        print(len(self.eq_entry))
        for entry in self.eq_entry:
            self.equations.append(entry.get())

    def display_solution(self):
        self.create_new()
        heading = tk.Label(self.eframe, width=30)
        heading['font'] = self.cfont.split()[0] + ' ' + str(int(self.cfont.split()[1]) + 5)
        if self.solution[0] == ('*', 0.0):
            heading['text'] = 'Error !!'
            heading.pack(side=tk.TOP, pady=40)
            self.enable_scrolling()
            return
        else:
            heading['text'] = 'Solution'
        heading.pack(side=tk.TOP, pady=40)
        for a, b in self.solution:
            row = tk.Frame(self.eframe, padx=self.winfo_width() / 10)
            lab = tk.Label(row, width=20, font=self.cfont, anchor='w')
            lab['text'] = '{} = {}'.format(a, b)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=self.winfo_height()/50)
            lab.pack(side=tk.LEFT)
        self.enable_scrolling()

    def start(self):
        self.step1()
        self.mainloop()

# remember to add if warning then clear warnings and equations
