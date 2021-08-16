Language and version: Node v6.17.1
 
We will be representing the Traveler Module as a class from a script called `traveller.js`. In order for other clients to access this class, we will be exporting `class TownNetwork` within the script. A client can this class as a module by using this:
```import { TownNetwork } from './modules/traveller.js';```.
 
To start with, we need a class called TownNetwork to represent the network of towns. This class should have a list of characters and a list of towns. A character will just be a JSON with two attributes: a string to represent a character’s name, and a string to represent the town that character is in. Each town in the list of towns is a JSON that contains a string to represent the name of the town and a list of strings to represent each town that the given town is directly connected to.
 
The constructor should take in a list of towns like this:
```
[{town: 'Duskendale', adjoining-towns: ['Winterfell', 'King's Landing']}
{town: 'Winterfell', adjoining-towns: ['Duskendale']}
{town: 'King's Landing', adjoining-towns: ['King's Landing']}]
```
and just set this list to the towns attribute in the class. It also should set the list of characters to an empty array.
 
We need a function inside the TownNetwork class that places a named character in a town. Basically what this means is that we will be adding to the list of characters that is initialized as an empty array. This function should take in two strings: the characters name and the name of the town the character is in. If the second string does not correspond to a name of an existing town in the list of towns then an error should be thrown. This function should not return anything.
 
We need another function inside the TownNetwork class that tells us if a given character can reach a given town without crossing paths with any other characters. This function will be called canCharacterReachTownUndisturbed. This function should take in a string to represent the characters name and a string to represent the towns name. If the character string does not correlate with an existing character name in the list of characters or if the town string does not correlate with an existing town name in the list of towns, an error should be thrown. Assuming no error is thrown this function needs to find every unique path from the town that the character currently is in to the given town. If and only if there is at least one path  between these two towns that has no people on it, then this function should return true, otherwise return false.

