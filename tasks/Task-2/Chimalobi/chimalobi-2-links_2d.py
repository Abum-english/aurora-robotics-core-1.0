
import numpy as np # this makes imports the numpy file already built in and np is what calls the function
import matplotlib.pyplot as plt #matplotlib is a function that allows plotting of graphs and the likes
from matplotlib.widgets import Slider # this makes the robotics arm slide while the code is running

# --- predefined link lengths (in arbitrary units) ---
L1 = 1.5 # L1 is giving a value
L2 = 1.0 # L2 is giving a value

def fk(theta1, theta2): # This is where the equation is written
    """Forward kinematics for a 2R planar arm (angles in radians)."""
    x1 = L1*np.cos(theta1) #*np multiplys li variable with numpy arrays
    y1 = L1*np.sin(theta1)
    x2 = x1 + L2*np.cos(theta1 + theta2) #np.cos is the cos() function within the NumPy library.
    y2 = y1 + L2*np.sin(theta1 + theta2) #np.sin is the sin() function within the NumPy library.
    return (0, 0), (x1, y1), (x2, y2) #(0,0) is the origin, (x1,y1) is the value of the first link, (x2,y2) is the value of the second link

# --- figure and axes ---
plt.figure(figsize=(7, 7)) # this creates a blank canvas that is 7 by 7 from the matplotlib.pyplot function
ax = plt.subplot(111) # this is where the x,y axis are defines
ax.set_aspect("equal", adjustable="box") # used to control the aspect ratio of an Axes object and how that aspect ratio is maintained.
ax.set_xlim(- (L1+L2+0.2), L1+L2+0.2) # Sets the x-axis view limits
ax.set_ylim(- (L1+L2+0.2), L1+L2+0.2) # Sets the y-axis view limits.
ax.grid(True, linestyle="--", linewidth=0.5) # adds a grid to an Axes object (ax) and customize its appearance.
ax.set_title("2-Link Planar Arm (use sliders below)") # Title of the graph

# initial angles (radians)
theta1_0 = np.deg2rad(30.0) # np.deg2rad() converts an angle from degrees to radians
theta2_0 = np.deg2rad(30.0)

# draw initial arm
base, joint, ee = fk(theta1_0, theta2_0) # base, joint, ee is the variable the function fk is assigned to
(link_line,) = ax.plot([base[0], joint[0], ee[0]], # ax.plot() method in Matplotlib is used to plot data on a set of axes.
                       [base[1], joint[1], ee[1]],
                       marker="o", linewidth=3)
ee_text = ax.text(0.02, 0.98, "", transform=ax.transAxes,
                  va="top", ha="left", fontsize=10,
                  bbox=dict(boxstyle="round", fc="w", ec="0.7")) #text() function is used to specify the location, alignment, orientation, and style of text. Location control involves setting x and y coordinates for text placement. Alignment can be adjusted both horizontally and vertically using the ha and va parameters

# --- slider axes (beneath plot) ---
slider_ax1 = plt.axes([0.15, 0.05, 0.7, 0.03]) # this is used to control the location of link 1 with respect to the origin
slider_ax2 = plt.axes([0.15, 0.01, 0.7, 0.03]) # this is used to control the location of link 2 with respect to the link 1

s_theta1 = Slider(slider_ax1, 'θ1 (deg)', -180.0, 180.0, valinit=np.rad2deg(theta1_0)) # this allows the link 1 to go a complete 360
s_theta2 = Slider(slider_ax2, 'θ2 (deg)', -180.0, 180.0, valinit=np.rad2deg(theta2_0)) # this allows the link 2 to go a complete 360

def update(_): #function update
    th1 = np.deg2rad(s_theta1.val) # passes the value assigned from s_theta1 to th 1 allowing th 1 to control theta 1 values
    th2 = np.deg2rad(s_theta2.val) # passes the value assigned from s_theta2 to th 1 allowing th 2 to control theta 2 values
    b, j, e = fk(th1, th2)
    link_line.set_data([b[0], j[0], e[0]], [b[1], j[1], e[1]])
    ee_text.set_text(f"EE: x={e[0]:.3f}, y={e[1]:.3f}\nθ1={np.rad2deg(th1):.1f}°, θ2={np.rad2deg(th2):.1f}°")
    plt.draw() # sets the x axis, y- axis 

s_theta1.on_changed(update) # this allows new values of s_theta1 from the update function to run continously without reruning the code repeatedly
s_theta2.on_changed(update) # this allows new values s_theta2 from the update function to run continously without reruning the code repeatedly
update(None)

plt.show() # this displays the grid that has been plotted
