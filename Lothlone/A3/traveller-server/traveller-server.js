class TownNetwork {
    // constructs a TownNetwork from a given array of town objects, which must have:
    // a 'town' attribute for the name of the town, and an 'adjoining-towns' attribute that is an
    // array of strings of the names of the neighboring towns
    constructor(loTown) {
        this.towns = loTown;
        this.characters = [];
    }
    
    // places a character in a given town. This adds the character to an array of character objects,
    // which contain 'name' and 'town' attributes
    placeCharacter(charName, townName) {
        if (this.doesTownExist(townName)) {
            this.characters.push({'name': charName, 'town': townName});
        } else {
            throw new Error(townName + ' is not in the list of Towns');
        }
    }

    // returns a boolean indicating if the given character can reach the given town by starting at
    // the town the character resides in and traveling only through towns which are unoccupied
    canCharacterReachTownUndisturbed(charName, destination) {
        if (!this.doesTownExist(destination)) {
            throw new Error(townName + ' is not in the list of Towns');
        }
        if (!this.doesCharacterExist(charName)) {
            throw new Error(charName + ' is not in the list of Characters');
        }
        
        // figure out what town the character starts at
        var start;
        for (var i = 0; i < this.characters.length; i++) {
            if (charName == this.characters[i]['name']) {
                start = this.characters[i]['town'];
            }
        }

        
                 

        // keep track of nodes visited so we don't revisit
        var visited = [];
        // nodes we've discovered but haven't explored yet
        // treated as a stack (recently discovered nodes searched first)
        var discovered = [start];
        // current node
        while (discovered.length != 0) {
            // explore next node
            var current = discovered.pop();
            visited.push(current)
            if (current == destination) {
                return true;
            }
            // find current town object in list of towns
            for (var i = 0; i < this.towns.length; i++) {
                var iTown = this.towns[i];
                if (current == iTown['town']) {
                    // add neighbors to "discovered" stack if we want to explore them
                    var neighbors = iTown['adjoining-towns'];
                    for (var j = 0; j < neighbors.length; j++) {
                        
                        // we only want to explore if we haven't before and the town is unoccupied
                        
                        if (!visited.includes(neighbors[j]) && !this.isTownOccupied(neighbors[j])) {
                            
                            if (discovered.includes(neighbors[j])) {
                                  // move neighbor to top of stack
                                  discovered.splice(j, 1);
                            }
                            // visit this neighbor next by moving it to the top of the stack
                            discovered.push(neighbors[j]);
                        }
                    }
                }
            }
        }
        return false;
    }
    // returns a boolean indicating if the given town exists in the network
    doesTownExist(townName) {
        for (var i = 0; i < this.towns.length; i++) {
            if (townName == this.towns[i]['town']) {
                return true;
            }
        }
        return false;
    }

    // returns a boolean indicating if the given character exists in the network
    doesCharacterExist(charName) {
        for (var i = 0; i < this.characters.length; i++) {
            if (charName == this.characters[i]['name']) {
                return true;
            }
        }
        return false;
    }

    // returns a boolean indicating if town is occupied. Occupied = true, unoccupied = false
    isTownOccupied(townName) {
        for (var i = 0; i < this.characters.length; i++) {
            if(townName == this.characters[i]['town']) {
                return true;
            }
        }
        return false;
    }
}

module.exports = {
    TownNetwork: TownNetwork
}




/*
// Test Code
var townlist = [{'town': 'Duskendale', 'adjoining-towns': ['King\'s Landing', 'Winterfell', 'The Twins']}, 
                {'town': 'Winterfell', 'adjoining-towns': ['Duskendale', 'The Twins']},
                {'town': 'King\'s Landing', 'adjoining-towns': ['Duskendale']},
                {'town': 'The Twins', 'adjoining-towns': ['Duskendale', 'Winterfell']},
                {'town': 'Braavos', 'adjoining-towns': []}];

var mytown = new TownNetwork(townlist);

mytown.placeCharacter('Jim Toob', 'The Twins');
mytown.placeCharacter('Jon Snow', 'Winterfell');

// This should return true
console.log(mytown.canCharacterReachTownUndisturbed('Jon Snow', 'King\'s Landing'))
// These should both return false; The Twins is occupied and Braavos is unreachable
console.log(mytown.canCharacterReachTownUndisturbed('Jon Snow', 'The Twins'))
console.log(mytown.canCharacterReachTownUndisturbed('Jon Snow', 'Braavos'))
*/