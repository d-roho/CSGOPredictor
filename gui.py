import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import time
import random
from MainApp import pred

def gui_initialization():
	mpl.rcParams['toolbar'] = 'None'
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)


	def animate(i):
		CT = [0]
		T = [0]
		CT[0] = pred[0]
		T[0] = pred[1]
		X = "Preds"
		teams = ["CT\n", "T\n"]
		iterator = 0
		 
		ax.clear()
		ax.barh(X, CT, color="b")
		ax.barh(X, T, left=CT, color="orange")
		ax.set_yticklabels([])
		ax.set_xticklabels([])
	 
		for bar in ax.containers:
			lab = teams[iterator] + str(pred[iterator]) 
			labels = [lab]
			ax.bar_label(bar, labels=labels, label_type='center', fontsize = 16, color="w", fontweight='bold')
			iterator +=1

def gui_start():
	from gui import gui_initialization
	ani = animation.FuncAnimation(fig, animate, interval=1000)
	plt.show()