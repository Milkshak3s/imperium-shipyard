"""
@file turrets.py

Module that contains classes and relevant data for a turret
"""
from shipyard.models.json_reader import get_file_data


class Turret:
    """
    Represents a single turret on a ship

    :param model_type: which type of model the turret is
    """
    def __init__(self, model_type):
        data = get_file_data("hull_turrets.json")

        self.data            = data
        self.name            = model_type                          # name of the model
        self.model           = data.get("models").get(model_type)  # model of the turret
        self.tonnage         = self.model.get("tonnage")           # size of the turret and addons
        self.addons          = list()                              # list of the addons for this turret
        self.max_wep         = self.model.get("num_weapons")       # max number of weapons per turret type
        self.weapons         = list()                              # list of the weapons on this turret
        self.cost            = self.model.get("cost")              # cost of the turret and addons

    def add_addon(self, part):
        """
        Handles adding an add-on to the turret
        :param part: Name of the add-on to add
        """
        addon = self.data.get("addons").get(part)

        # Appending addon and related costs to turret fields
        self.addons.append(addon)
        self.tonnage += addon.get("tonnage")

        if part == "Pop-up Turret":
            self.cost += addon.get("cost")
        if part == "Fixed Mounting":
            self.cost *= addon.get("turret_cost_modifier")

    def add_weapon(self, part):
        """
        Handles adding weapons to the turret
        :param part: Name of the weapon to add
        """
        if len(self.weapons) == self.max_wep:
            print("Error: cannot add '{}'. Max # of weapons reached for {}: {}/{}".format(
                part, self.name, len(self.weapons), self.max_wep))
            return

        weapon = self.data.get("weapons").get(part)

        self.weapons.append(weapon)
        self.cost += weapon.get("cost")

    def remove_weapon(self, part):
        """
        Handles removing a specific weapon from the turret
        :param part: Name of the weapon to remove
        """
        if len(self.weapons) == 0:
            print("Error: no weapons to remove.")
            return

        wep = self.data.get("weapons").get(part)

        # Check if any weapon matches this weapon. If none, print error.
        for w in self.weapons:
            if wep == w:
                self.weapons.remove(w)
                self.cost -= w.get("cost")
                return
        print("Error: {} not attached to {}".format(part, self.name))
