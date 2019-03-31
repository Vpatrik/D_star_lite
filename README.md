# D* lite 

---
Based on original [article](https://www.uco.es/investiga/grupos/ava/node/26 "D* lite") from Sven Koenig.
Started as a fork of [mdeyo](https://github.com/mdeyo/d-star-lite "D* lite repo"), then diverted.
Visualization is also based on tutorials for Pygame.

---


## World generation

World can be generated by:
1. from .txt file - see example grid folder
2. random generation with specification of size
3. from blank world by left mouse button clicking on free grid

---

## Starting visualization

### Settings in <em>main.py</em>
 - viewing range of robot: <em>VIEWING_RANGE</em>
 - number of steps: <em>f_step</em>
 - heuristic type: 
  	-  1 - <em>euclidan</em>
  	-  2 - <em>diagonal</em>
 - manual and random world generation:
	- number of vertices in x axis: <em>x_div</em>
	- number of vertices in y axis: <em>y_div</em>
	- start vertex coordinates (string) : <em>start</em>
	- goal vertex coordinates (string) : <em>goal</em>
### Control
- one step: <em>space bar</em>
- multiple steps: <em>f key</em>
- add obstacle to vertex: <em>left mouse button</em>

---