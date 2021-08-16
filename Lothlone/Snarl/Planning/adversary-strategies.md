# Adversary Strategies

## Zombie

The zombie can only move one tile at a time, cannot leave the room it's spawned in, and cannot interact with walls in the same way a ghost can. While exploitable, to reduce possibile processing times, a simple greedy manhattan distance algorithm should be sufficient to produce reasonable AI. A pseudocode algorithm would be something like:

```
get cardinally neighboring tiles

filter out invalid successors (doors, walls/void, other adversaries, etc.)

if len(valid neighbors) == 0, stand still

if len(valid neighbors) == 1, take action to move to that neighbor

else:
    create a dict to store successors and their corresponding least-manhattan-distance

    for all players in room:
        for pos in valid successors:
            get manhattan distance from pos to player position(s)

            store pos as key in dict with manhattan distance as value,
            if pos already in dict, overwrite with any smaller distance


    filter valid actions by those with the least manhattan distance (according to dict)

    randomly choose action among remaining valid actions
```

This should result in an objective-oriented (go towards players fast) but beatable AI. By not having the AI hunt while players are not in the room, the AI will not camp the door tiles, making it so players should be able to enter a room and not expect to get blitzed.

## Ghost

The ghost algorithm should be relatively similar to a zombie, but it allows us to try out arbitrary values to create a ghost that tries it's best to hunt humans while simultaneous exploiting it's ability to teleport randomly by walking into room walls. Since ghosts can traverse hallways and by extension the whole map, it would be reasonable to simply have the ghost always move towards the player. There must be a distance threshhold to allow the ghost to try and teleport closer to a player (since it could technically move it further away!). However, to prevent the ghost from constantly doing this, an arbitrary cooldown should be added. Some pseudocode might look like this

```
get cardinally neighboring tiles

filter out invalid neighbors (now only other adversaries and hallway walls).

if len(valid neighbors) == 0: stand still

if len(valid neighbors) == 1: take the only valid action

else:
    for all players within Radius:
        for pos in valid successors:
            get manhattan distance from pos to player position(s)

            store pos as key in dict with manhattan distance as value,
            if pos already in dict, overwrite with any smaller distance


    filter valid actions by those with the least manhattan distance (according to dict)

    if the dict is not empty:
        set teleport cooldown to 0
        randomly choose action among remaining valid actions
    
    else:
        if our teleport cooldown is 0:
            if we're next to a room wall:
                teleport
            else:
                randomly choose action among valid tiles
        else:
            subtract 1 from teleport cooldown
            randomly choose action among valid tiles
```

Radius is an arbitrary variable that should decide when the ghost should roam (and maybe take a wall) or try and find a human. The teleport cooldown is a field of the ghost class that indicates whether it can teleport or not, so that it doesn't try to teleport all the time (since sometimes it may come across a player just by roaming.)
