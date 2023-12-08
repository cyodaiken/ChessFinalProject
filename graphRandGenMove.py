import matplotlib.pyplot as plt 
import numpy as np

x=['Basic Heuristic','Endgame Tables','Updated Heuristic','Opening Book']
y_white=[40.25,41.44,37.02,34.98]
y_white_err=[12.92,12.93,15.06,14.54]
y_black = [42.76, 41.66, 42.02, 38.02]
y_black_err=[10.51, 9.74, 13.31, 14.54]

width = 10
height = 8

X_axis = np.arange(len(x)) 

plt.figure(figsize=(width, height))

plt.bar(X_axis - 0.2, y_white, 0.4, label="White", color=['lightgray','lightgray','lightgray','lightgray'])
plt.bar(X_axis + 0.2, y_black, 0.4, label= 'Black', color=['black','black','black','black'])

plt.xticks(X_axis, x)
plt.title('Number of Moves to Win Against Random Move Generator')
plt.xlabel('Features Used')
plt.ylabel('Number of Moves')
plt.legend()
plt.savefig('ABvRG.png', dpi=400, transparent=True)
plt.errorbar(X_axis - 0.2, y_white, y_white_err, fmt='.', color='gray', elinewidth=2,capthick=10,errorevery=1, alpha=0.5, ms=4, capsize = 2)
plt.errorbar(X_axis + 0.2, y_black, y_black_err, fmt='.', color='gray', elinewidth=2,capthick=10,errorevery=1, alpha=0.5, ms=4, capsize = 2)
plt.show()