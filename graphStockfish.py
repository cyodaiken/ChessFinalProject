import matplotlib.pyplot as plt 
import numpy as np

x=['Basic Heuristic','Endgame Tables','Updated Heuristic','Opening Book']
y_white=[64.56,60.90,100.56,77.88]
y_white_err=[38.58,29.12,57.67,29.74]

y_black = [63.40, 67, 85.43, 92.47]
y_black_err=[30.28, 37.93, 48.82, 59.62]

width = 10
height = 8

X_axis = np.arange(len(x)) 

plt.figure(figsize=(width, height))

plt.bar(X_axis - 0.2, y_white, 0.4, label="White", color=['lightgray','lightgray','lightgray','lightgray'])
plt.bar(X_axis + 0.2, y_black, 0.4, label= 'Black', color=['black','black','black','black'])

plt.xticks(X_axis, x)
plt.title('Number of Moves to Lose Against Stockfish')
plt.xlabel('Features Used')
plt.ylabel('Number of Moves')
plt.legend()
plt.savefig('ABvS.png', dpi=400, transparent=True)
plt.errorbar(X_axis - 0.2, y_white, y_white_err, fmt='.', color='gray', elinewidth=2,capthick=10,errorevery=1, alpha=0.5, ms=4, capsize = 2)
plt.errorbar(X_axis + 0.2, y_black, y_black_err, fmt='.', color='gray', elinewidth=2,capthick=10,errorevery=1, alpha=0.5, ms=4, capsize = 2)
plt.show()