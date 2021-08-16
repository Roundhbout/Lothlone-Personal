# Traveller
The Traveller module shall be written in python 3.6.8.<br>

- A Town is a class with fields of name (string), neighbors (list of Towns), residents (list of Characters). 
- A Character is represented by a string which is the name of the character. The Town class will have a constructor which takes only the name of the town as a string and initializes the neighbors and residents fields as empty lists.<br>

Our town network will be represented as a list of Towns. 

- The town network will be initialized as an empty list, and we will have a function to add towns to the list, with a string argument for the name of the new Town to add, which must be unique.<br>

There will also be a function to add new edges connecting two town nodes, which will take the two town names as string arguments and mutate each Town to update its neighbors list to include the other town.<br>
There will also be a function to add a new Character to the town network, which takes the name of the character as a string, which must be a unique character name, and a string for the name of the town to which the character will be added.<br> 
The query function will take in the string representing the destination town and a string representing the character, and return a boolean value which depends on if the given character can reach the destination without passing through a town that has any characters.<br>
