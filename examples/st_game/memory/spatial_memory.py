"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: spatial_memory.py
Description: Defines the MemoryTree class that serves as the agents' spatial
memory that aids in grounding their behavior in the game world. 
"""
import json
import os

class MemoryTree: 
  def __init__(self, f_saved): 
    self.tree = {}
    if os.path.isfile(f_saved) and os.path.exists(f_saved): 
      with open(f_saved) as f:
        self.tree = json.load(f)


  def print_tree(self): 
    def _print_tree(tree, depth):
      dash = " >" * depth
      if type(tree) == type(list()): 
        if tree:
          print (dash, tree)
        return 

      for key, val in tree.items(): 
        if key: 
          print (dash, key)
        _print_tree(val, depth+1)
    
    _print_tree(self.tree, 0)
    

  def save(self, out_json):
    with open(out_json, "w") as outfile:
      json.dump(self.tree, outfile) 


  def get_str_accessible_sectors(self, curr_world): 
    """
    Returns a summary string of all the arenas that the persona can access 
    within the current sector. 

    Note that there are places a given persona cannot enter. This information
    is provided in the persona sheet. We account for this in this function. 

    INPUT
      None
    OUTPUT 
      A summary string of all the arenas that the persona can access. 
    EXAMPLE STR OUTPUT
      "bedroom, kitchen, dining room, office, bathroom"
    """
    x = ", ".join(list(self.tree[curr_world].keys()))
    return x


  def get_str_accessible_sector_arenas(self, sector): 
    """
    Returns a summary string of all the arenas that the persona can access 
    within the current sector. 

    Note that there are places a given persona cannot enter. This information
    is provided in the persona sheet. We account for this in this function. 

    INPUT
      None
    OUTPUT 
      A summary string of all the arenas that the persona can access. 
    EXAMPLE STR OUTPUT
      "bedroom, kitchen, dining room, office, bathroom"
    """
    curr_world, curr_sector = sector.split(":")
    if not curr_sector: 
      return ""
    x = ", ".join(list(self.tree[curr_world][curr_sector].keys()))
    return x


  def get_str_accessible_arena_game_objects(self, arena):
    """
    Get a str list of all accessible game objects that are in the arena. If 
    temp_address is specified, we return the objects that are available in
    that arena, and if not, we return the objects that are in the arena our
    persona is currently in. 

    INPUT
      temp_address: optional arena address
    OUTPUT 
      str list of all accessible game objects in the gmae arena. 
    EXAMPLE STR OUTPUT
      "phone, charger, bed, nightstand"
    """
    curr_world, curr_sector, curr_arena = arena.split(":")

    if not curr_arena: 
      return ""

    try: 
      x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena]))
    except: 
      x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena.lower()]))
    return x


  def add_tile_info(self, tile_info: dict):
      if tile_info["world"]: 
        if (tile_info["world"] not in self.tree): 
          self.tree[tile_info["world"]] = {}
      if tile_info["sector"]: 
        if (tile_info["sector"] not in self.tree[tile_info["world"]]): 
          self.tree[tile_info["world"]][tile_info["sector"]] = {}
      if tile_info["arena"]: 
        if (tile_info["arena"] not in self.tree[tile_info["world"]]
                                                  [tile_info["sector"]]): 
          self.tree[tile_info["world"]][tile_info["sector"]][tile_info["arena"]] = []
      if tile_info["game_object"]: 
        if (tile_info["game_object"] not in self.tree[tile_info["world"]]
                                                          [tile_info["sector"]]
                                                          [tile_info["arena"]]): 
          self.tree[tile_info["world"]][tile_info["sector"]][tile_info["arena"]] += [
                                                                  tile_info["game_object"]]









