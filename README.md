# Sudoku Visualizer
### Sudoku visualizer in pygame
This Sudoku Visualizer project is part of an assignment in the Project INDA course at KTH Royal Institute of Technology.
The main use is for showing a visualization of a Sudoku Solving Algorithm. The application also provides manual play, and a puzzle generator with 3 difficulties.

### Modules

#### pygame
Pygame provides a template that makes it easy to build the base logic of the game.
It also provides easy access to display graphics, map mouse and keyboard to specific actions, and tracking a lot of processes that is supposedly to happen around the same time.
#### os
The os package has mostly been used as a structured way to handle paths to images.

### How to run
  _Coming soon..._
  (For now, one can clone the repository)

### Project Tools
#### ChatGPT
ChatGPT also called CGPT has been a helpful multi-use tool.
These are some ways it has been used:
<ul style="list-style-type: disc; padding-left: 1em;">
  <li style="margin-bottom: 0;">Guidance when there is something new to learn or one does not know what to do</li>
  <li style="margin-bottom: 0;">Inspiration for structural solutions and features</li>
  <li style="margin-bottom: 0;">Questions that is both programing and non-programming related</li>
  <li style="margin-bottom: 0;">Creating this list in html</li>
</ul>


#### Paint.NET
Paint.NET has been the main source of images for the projects.
The project uses pygame graphics as much as possible.
Paint.NET images has mostly been used for button and sudoku number graphics.


### Menu
The menu room is the gateway of the application, leading the user to where it wants to go. <br><br>
<img src=./images/screenshot_menu.png width="400"><br><br>
The menu currently contains:
<ul style="list-style-type: disc; padding-left: 1em;">
  <li style="margin-bottom: 0;">The Play button leads to the game room where the user may play sudoku and use the Sudoku Solving Algorithm to solve what is left of the puzzle.</li>
  <li style="margin-bottom: 0;">The Demo button also leads to the game room, but with a preset puzzle which is used to present the Sudoku Solving Algorithm.</li>
  <li style="margin-bottom: 0;">The Settings button leads to the settings room.</li>
</ul>

### Game
In the game room one gets directly to the sudoku board with difficulty options to the left and functional buttons to the right.<br><br>
<img src=./images/screenshot_game_empty.png width="400"><br>
<img src=./images/screenshot_game_hard_empty.png width="400"><br>
<img src=./images/screenshot_game_hard_solved.png width="400"><br>
<img src=./images/screenshot_game_manual_solved.png width="400"><br><br>
The difficulty options are represented as radio buttons, and each difficulty represents a given amount of hints.
<ul style="list-style-type: disc; padding-left: 1em;">
  <li style="margin-bottom: 0;">Easy → 45</li>
  <li style="margin-bottom: 0;">Medium → 35</li>
  <li style="margin-bottom: 0;">Hard → 29</li>
</ul>

And on the right side there are functional buttons:
<ul style="list-style-type: disc; padding-left: 1em;">
  <li style="margin-bottom: 0;">Generate: makes a new randomized puzzle with hints according to the current difficulty.</li>
  <li style="margin-bottom: 0;">Solve: starts the Sudoku Solving Algorithm from given point in the puzzle.</li>
  <li style="margin-bottom: 0;">Clear: removes all non-generated values from the board.</li>
  <li style="margin-bottom: 0;">Reset: removes all values from the board.</li>
  <li style="margin-bottom: 0;">Demo: runs the Sudoku Solving Algorithm on a preset puzzle.</li>
</ul>

### Settings
Settings room is the place for adjusting variables to either fit the specific computer environment, or further the user experience.<br><br>
<img src=./images/screenshot_settings.png alt="" width="400"><br><br>
Settings
Settings currently contains:
<ul style="list-style-type: disc; padding-left: 1em;">
  <li style="margin-bottom: 0;">The fullscreen/windowed button which changes the window size from window to fullscreen and vice versa.</li>
  <li style="margin-bottom: 0;">The back button which returns to the menu.</li>
</ul>
