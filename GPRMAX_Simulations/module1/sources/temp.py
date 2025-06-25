import numpy as np
import matplotlib.pyplot as plt

# parameters (choose a=1, d=2 for illustration; you can rescale mentally)
a = 1.0       # cylinder radius
d = 2.0       # center-to-plane distance
h = np.sqrt(d**2 - a**2)   # position of real line charge above plane

# computational grid in x-z plane (z>0)
x = np.linspace(-4*a, 4*a, 400)
z = np.linspace(0.0, 4*a, 400)
X, Z = np.meshgrid(x, z)

# potential (up to constant factor λ/2πϵ0, which we set to 1 for plotting)
V = 0.5 * np.log((X**2 + (Z - h)**2) / (X**2 + (Z + h)**2))

# electric-field components (E = -∇V)
dVdx, dVdz = np.gradient(V, x, z, edge_order=2)
Ex = -dVdx
Ez = -dVdz

# mask inside the conductor (circle centered at z=d, radius a)
mask = (X**2 + (Z - d)**2) < a**2
V_masked = np.ma.array(V, mask=mask)
Ex_masked = np.ma.array(Ex, mask=mask)
Ez_masked = np.ma.array(Ez, mask=mask)

# set up figure
fig, ax = plt.subplots(figsize=(6, 6))

# equipotential lines
contours = ax.contour(X, Z, V_masked, levels=np.linspace(-1.2, 1.2, 13), linewidths=0.8)
ax.clabel(contours, inline=True, fontsize=8)

# field lines (streamplot)
ax.streamplot(X, Z, Ex_masked, Ez_masked, density=1.2, linewidth=0.7, arrowsize=1)

# draw the conducting plane and cylinder outline
plane_x = np.linspace(-4*a, 4*a, 2)
ax.plot(plane_x, np.zeros_like(plane_x), lw=2)
circle = plt.Circle((0, d), a, color='black', fill=False, lw=2)
ax.add_artist(circle)

ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_title('Field lines (blue) and equipotentials (black) for a cylinder above a conducting plane')
plt.tight_layout()
plt.show()
