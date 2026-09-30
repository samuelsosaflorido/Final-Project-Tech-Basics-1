In this file we decided to add a straightforward guide on how to go through the game in the different rooms so it's way easier to play the game.  
The initial logic was to grab different items in each of the rooms, thus affecting the end of the game.  
Due to some issues the hospital had problems so the ending could not be visualized nor the room. But the main point is to either grab codes (which can be obtained in the different letters that you find (except in the cell, here code is found through the riddle in the chest)), the keys or the medication fragments. 

# GENERAL SEQUENCE TO GET TO END
1. Enter maze (automatic)
2. Beat maze (don't get killed by rat (rat doesn't work though))
3. Find first room (either Yard, Cell or Cafeteria)
4. Solve puzzles in room1
5. Maze
6. Find and solve room2
7. Maze
8. Find and solve room3
9. Maze
10. Option to go to Hospital appears (every room has to be entered once, doens't matter which or if any items have been found though)
11. Player can now go directly to the Hospital or they stay in the maze to explore the rooms more
12. In the Hospital there are 3 different ways out, each requires 3 parts of each item-type (3 keys, 3 codes, 3 medicines)
    * Keys: Game starts from the beginning
    * Code: Game is won, player wakes up in the real prison/hospital
    * Medicine: Game is lost, player dies

13. It is (or should've been) also possible to go back to the maze from the hospital (to get missing items) 


We will go now through the different areas of the game: 

# YARD 
#### (Right exit maze)
After going through th maze, one of the main rooms of the game is the Yard. Following the previous logic, you can interact with the mouse with the different NPCS.  
For the Ghost Puzzle the player can use the keyboard to type the different answers to obtain the medication fragment of the Ghost, the oher items can be obtained using the mouse click button, as well as the dialogue options when interacting with the Skeleton Ghost.   
The movements here can be executed using both the WASD and the key arrows. In the previous demo of this area, the SPACE option was introduced as the player had to dig to obtain the medication fragment after obtaining the coordinates. This was later removed in order to simplify the logic of this area so it could be better programmed.  
There are also some issues with the TAB function which was intended for the inventory, sadly this cannot be seen but in previous versions the player could see an inventory interface where you could see the different slots and how many items does the player have.  


# CELL
#### (Left exit maze)
The cell also gets accessed from the maze. Going from left to right, the item to find or riddles to solve are:  
1. The Medicine: right next to the door, a chest can be found (chest can also be opened, but please don't do that yet as I haven't had time to add the possibility to close it again and opening it interferes with the task) --> if the player goes upwards and moves up to the chest from the left, the chest can be pushed (issue here: chest kinda close to the entrance to the room, so it frequently happens that the player gets kicked out into the maze again, it is possible to do though, just have to be careful) --> once the chest is pushed up to the table, it won't go any further --> a hint appears and the player can jump onto the chest --> now a bottle of medicine appears on the table, which can be picked up (no comfirmation on screen, just in the console)
2. The Code: to get the code, the chest has to be opened (always possible when the player is close to it, also after it has been pushed) --> inside there are coins and gems, gems have 3 different colors which correspond with the colors in the 3 squares of the riddle --> player has to count each number of gems and type them into the squares (the only trick here is the number of pink gems, it looks like there are only 6, but it's 7, noticable, because all the gems are exactly 4x4 except for one pink one, which is 6x4 (it's two next to each other) --> once the code is correctly put in, the player confirms with ENTER and the code gets moved to the inventory (also only visible in the console)
3. The Key: the key is the easiest to find, as it is simply hidden under the bed and slightly visible --> player has to go near it and can then pick it up --> key also gets moved to inventory (confirmation in console)

Other than these, there is nothing to be done in the cell. The player can go back to the maze with none, one or all of the items. 
To unlock the hospital area (which doesn't work, we miscalculated the time it would take to connect all the rooms) each room only has to be entered, it's not necessary to actually find any of the items.  

##### General Motions: 
The character can be moved through WASD (like in the other rooms).  
To push the chest you just go up to it, no button necessary. To jump on the chest, press 'SPACE'. To pick up the medicine, press 'E'.  
To open the chest, press 'E'. To input the numbers, use numbers, go forward with 'TAB' (clicking on the squares doesn't work, didn't have time to add it). To input code, press 'ENTER'. To exit the chest window, press 'ESC'.  
To pick up the key, press 'E'.  



# CAFETERIA
#### (Bottom exit maze)
In the Cafeteria there is a letter lying on a table on the right, a trashcan has spilled and a skeleton is standing behind the food counter. These are the three objects/NPCs you have to go to in order to find the needed objects. 

##### The Letter:
- has to be clicked on with the mouse and then the highlighted numbers are the right ones
- you have to remember it

##### The Trashcan:
- in the trashcan you find the key
- just click on it with the mouse and it gets added to the inventory

##### The Skeleton:
- click on the skeleton and it will ask you a question
- to give an answer simply type the corresponding number on the keyboard
- if the answer is correct, the medicine gets added to the inventory

General movement of the character is done by pressing WASD. 






