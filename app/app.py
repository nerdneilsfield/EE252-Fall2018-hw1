from tkinter import *
from tkinter import ttk
from cds import *

tx = [
    0, 257, 258, 260, 261, 264, 265, 266, 272, 273, 274, 276, 277, 288, 289,
    290, 292, 293, 296, 297, 298, 320, 321, 322, 324, 325, 328, 329, 330, 336,
    337, 338, 340, 341, 512, 513, 514, 516, 517, 520, 521, 522, 528, 529, 530,
    532, 533, 544, 545, 546, 548, 549, 552, 553, 554, 576, 577, 578, 580, 581,
    584, 585, 586, 592, 593, 594, 596, 597, 640, 641, 642, 644, 645, 648, 649,
    650, 656, 657, 658, 660, 661, 672, 673, 674, 676, 677, 680, 681, 682, 771,
    774, 780, 783, 792, 795, 798, 816, 819, 822, 828, 831, 864, 867, 870, 876,
    879, 888, 891, 894, 960, 963, 966, 972, 975, 984, 987, 990
]


def calculate(*args):
    try:
        x = int(feet.get())
        x_sd = MinCostSD(x)
        meters.set(str(x_sd))
        exps.set(x_sd.expr())
        msds = x_sd.get_msds_str()
        if x > 2 and x < 3900 and x not in tx:
            res = x_sd.min_cost()
            mincost.set(res["cost"])
            minfactors.set(" * ".join([str(i) for i in res["sets"]]))
        else:
            mincost.set("Not a suitable number ")
            minfactors.set("Not a suitable number ")

        count = 6
        for msd in msds:
            # print(count)
            ttk.Label(
                mainframe, text=msd).grid(
                    column=2, row=count, sticky=(W, E))
            count = count + 1

    except ValueError:
        pass


root = Tk()
root.title("DIP ToolBox")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()
exps = StringVar()
mincost = StringVar()
minfactors = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=exps).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mincost).grid(column=2, row=4, sticky=(W, E))
ttk.Label(
    mainframe, textvariable=minfactors).grid(
        column=2, row=5, sticky=(W, E))
ttk.Button(
    mainframe, text="Calculate", command=calculate).grid(
        column=3, row=1, sticky=W)

ttk.Label(
    mainframe, text="Please enter a number").grid(
        column=1, row=1, sticky=E)

ttk.Label(
    mainframe, text="The CSD representation is: ").grid(
        column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Expression:").grid(column=1, row=3, sticky=E)
ttk.Label(
    mainframe, text="The Minimal cost is: ").grid(
        column=1, row=4, sticky=E)
ttk.Label(
    mainframe, text="By factorization of: ").grid(
        column=1, row=5, sticky=E)
ttk.Label(
    mainframe, text="The MSD representation is: ").grid(
        column=1, row=6, sticky=E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()

root.bind('<Return>', calculate)

root.mainloop()