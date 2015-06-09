"""
The two functions saves parameters, picture references and comments before and after
compilation in a tex file. Firstly, it only works with integrator.py
"""
from datetime import datetime

def dokufile(myfile):
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    inptex = input("what do you want to see?  (in quot. marks..)")
    myfile.write(inptex+"\\\ \n")
    myfile.write("\\begin{figure}[h!]\centering")
    return filename1
    
def savepictopdfandtex(title, filename1, plt, myfile):
    plt.savefig("../pics_zu_github" + str(filename1)  + str(title) + '.pdf')
    myfile.write("\includegraphics[scale = 0.3]{num/pics_zu_github/"+ filename1 + str(title) + '.pdf'+"}")
   
def enddoku(N_osc, spread, epsilon, N_time, tmax, myfile):
    myfile.write("\\caption{this plot was generated using integrator.py, integration with N\\_osc ="+repr(N_osc)+", ")
    myfile.write("omg = randn, spread = "+repr(spread)+", ")
    myfile.write("epsilon = "+repr(epsilon)+", ")
    myfile.write("N\\_time = "+repr(N_time)+", ")
    myfile.write("tmax = "+repr(tmax)+", ")
    #myfile.write(str(y)+",")
    inpt = input("your comment 'bout the plots? (in quotation marks, please..)  ")
    myfile.write(inpt)
    myfile.write("}\\end{figure}\n")
    myfile.close()