"""
The town network will be initialized as an empty list, 
and we will have a function to add towns to the list, 
with a string argument for the name of the new Town to add, which must be unique.
"""

town_network = []


class Town(): 
	"""
	A Town is a class with fields of name (string), 
	neighbors (list of Towns), residents (list of Characters).

	Attributes: 
	name : str 
	neighbors: [town] initialized as empty list, store town object 
	residents: [character] initialized as empty list store character obj
	"""

	global town_network 

	def __init__(self, name):
		self.name = name 
		self.neighbors = []
		self.residents = []


class Character(): 
	"""
	A Character is represented by a string which is the name of 
	the character. The Town class will have a constructor which 
	takes only the name of the town as a string and initializes 
	the neighbors and residents fields as empty lists.

	attributes: 
	name: string that represents name of character
	"""
	def __init__(self, name):
		self.name = name 


def get_town(town_name):
	"""
	gets the town based on given name 

	parameters:
	town_name: string argument for name of town  
  str -> Town
	"""
	global town_network
	for town in town_network: 
		if town.name == town_name: 
			return town

def network_add_town(town_name): 
	"""
	adds town to the town network 
	
	parameters:
	town_name: string argument for name of town  
  str -> void
	"""
	global town_network
	new_town = Town(town_name)
	town_network.append(new_town)

def connect_town(town_name1, town_name2): 
	"""
	adds town each other's town list
	
	parameters:
	town_name1 / town_name2: string arugmenst to location town and
	add to each other towns list 
  str, str -> void
	raises: 
	exception if one or more town is not present in the network 

	"""
	global town_network 
	for town in town_network:
		if town.name == town_name1: 
			town1 = town 
		if town.name == town_name2: 
			town2 = town 
	if town1 is not None and town2 is not None: 
		town1.neighbors.append(town2)
		town2.neighbors.append(town1)
	else: 
		raise Exception("one or more town is not present in network")

def add_character_to_town(town_name, character_name):
	"""
	adds character to town
	
	parameters:
	town_name: string argument for name of town 
	character_name: string argument as character name to create new character 
	to add to the town 
	str, str -> void
	raises: 
	Exception if the town does not exist 

	"""
	if character_uniqueness(character_name):
		for town in town_network:
			if town.name == town_name:
				new_character = Character(character_name)
				town.residents.append(new_character)
				return
	raise Exception("town does not exist")

def character_uniqueness(character_name): 
	"""
	returns boolean 

	checks if the character already exists
	
	parameters:
	character_name: string argument for character 
  str -> boolean
	"""
	global town_network

	for town in town_network: 
		if character_name in town.residents: 
			return False

	return True

def list_residents(town):
	"""
	returns a list of characters' names 

	paramters: 
	town: a town object 
  Town -> list of str
	"""
	return [char.name for char in town.residents]

def can_reach_destination_alone(town_name, character_name):
	"""
	returns boolean to see if character can reach a designated town object
	without running into another character 

	paramters: 
	town_name: string arugment for name of town 
	character_name: string arugment for name of character 
  str, str -> boolean
	"""
	global town_network 

	initial_town = character_location(character_name)

	dp = {}
	memoize = []

	for town in town_network: 
		if town not in dp: 
			if len(town.residents) == 0: 
				dp[town] = True 
			else: 
				dp[town] = False 

	dp[initial_town] = True

	print(dp)

	if recurse_town(dp, initial_town, town_name, memoize) == None: 
		return False 
	else: 
		return True 
		


def recurse_town(town_dict, init_town, dest_town, memoize):
	"""
	a helper function to recurse through the towns 

	parameters:
	town_dict: dictionary of towns k=town name, v= boolean for if list of residents is empty
	init_town: starting town for the function 
	dest_town: name of town trying to be reached
	memoize: list of towns that have already been checked by the function 
  dict of Town, Town, str, list of Town -> Boolean
	"""
	if town_dict[init_town] == False: 
		#print("case1")
		return

	if init_town.name == dest_town: 
		#print("case2")
		return True
		
	if init_town.name not in memoize:
		memoize.append(init_town.name)
	
	for town in init_town.neighbors:
		if town.name in memoize: 
			continue 
		else: 
			return recurse_town(town_dict, town, dest_town, memoize)


def character_location(character_name):
	"""
	returns the initial location of the given character 

	paramters: 
	character_name: string argument as the name of the character
  str -> Town

	raises: 
	exception that the character does not exist if a town is not returned
	"""
	global town_network

	for town in town_network: 
		if character_name in list_residents(town): 
			return town 

	raise Exception("character does not exist")

	
#scripting
#network_add_town("boston")
#network_add_town("boston2")
#network_add_town("boston3")
#network_add_town("boston4")

#print(town_network)

#connect_town("boston", "boston3")
#connect_town("boston3", "boston4")
#connect_town("boston3", "boston2")
#add_character_to_town("boston", "nathan")
#add_character_to_town("boston2", "justin")
#print(list_residents(get_town("boston")))
#print(can_reach_destination_alone("boston4", "nathan"))
