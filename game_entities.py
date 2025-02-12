"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: id number of location
        - name: name of location
        - brief_description: brief description of location
        - long_description: long description of location
        - available_commands: a list of available directional commands
        - items: a list of items in the location
        - visited: whether the user has already been in this location or not
        - dialogue: availability of a dialogue option in given location
        - current_dialogue: tracks the state of a dialogue at a location
        - conversation_success: Checks whether the dialogue was successful
        - music: sfx name that is supposed to play in a specific location

    Representation Invariants:
        - id_num > 0
        - name != ""
        - brief_description != ""
        - long_description != ""
        - music != ""
    """
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list
    visited: bool
    dialogue: dict
    current_dialogue: dict
    conversation_success: bool
    music: str

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id: int, name: str, brief_description: str, long_description: str,
                 available_commands: dict[str, int], items: list,
                 visited: bool = False, dialogue: Optional[dict] = None, music: Optional[str] = None) -> None:
        """Initialize a new location, along with its dialogue and other attributes."""

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited
        self.dialogue = dialogue if dialogue else {}
        self.current_dialogue = None
        self.conversation_success = False
        self.music = music

    def start_dialogue(self, game) -> None:
        """Start a dialogue at this location if available."""
        if self.dialogue:
            self.current_dialogue = self.dialogue
            return self._show_dialogue_block(game)
        return None

    def _show_dialogue_block(self, game) -> None:
        """Show the current dialogue block and handle player choices."""
        if not self.current_dialogue:
            return

        print("\n💬", self.current_dialogue["text"])  # Show NPC text

        if "options" in self.current_dialogue:
            if self.current_dialogue["text"] == "The barista flips the mug and reveals the \
encoded word: **V YBIR PFP111**":
                # Handle Caesar cipher puzzle
                player_guess = input("\n🔍 Enter the decoded word: ").strip().upper()
                correct_answer = self.caesar_cipher("V YBIR PFP111", 13)  # Decode

                if player_guess == correct_answer:
                    print("\n✅ Correct! The barista hands you the mug.")
                else:
                    print("\n❌ Wrong answer. The barista shakes their head. 'Nope. Guess it isn't yours after all.")
                    self.conversation_success = False
                return  # Exit after processing direct input

            # Show player choices
            for key, option in self.current_dialogue["options"].items():
                print(f"  {key}. {option['text']}")

            choice = input("\nChoose an option: ").strip()
            while choice not in self.current_dialogue["options"]:
                print("Invalid choice. Try again.")
                choice = input("\nChoose an option: ").strip()

            next_dialogue = self.current_dialogue["options"][choice]["next"]

            if next_dialogue == "end":
                self.current_dialogue = None  # End dialogue
                print("\n The conversation has ended.")
            else:
                self.current_dialogue = self.dialogue["branches"][next_dialogue]  # Move to next dialogue
                self._show_dialogue_block(game)  # Continue dialogue

    @staticmethod
    def caesar_cipher(text: str, shift: int) -> str:
        """Decodes strings using Caesar cipher."""
        result = ""
        for char in text:
            if char.isalpha():
                shift_amount = shift % 26
                if char.isupper():
                    new_char = chr(((ord(char) - ord('A') - shift_amount) % 26) + ord('A'))
                else:
                    new_char = chr(((ord(char) - ord('a') - shift_amount) % 26) + ord('a'))
                result += new_char
            else:
                result += char
        return result

    def look(self) -> None:
        """
        Display the long description of the current location
        """
        print(self.long_description)


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - start_position: where the item initially wasa
        - target_position: where the item must be
        - target_points: amount of points received after depositing an item

    Representation Invariants:
        - name != ""
        - start_position > 0
        - target_position > 0
        - target_points >= 0
    """
    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


class Player():
    """A player in our text adventure game world."""
    inventory: list[Item]
    score: int

    def __init__(self) -> None:
        self.inventory = []
        self.score = 0

    def display_inventory(self) -> None:
        """
        Displays a list of items that are currently present in a player's inventory
        """
        if self.inventory == [] or self.inventory is None:
            print("Oops, seems like you have nothing in your inventory.")
        else:
            print("Inventory:", ", ".join(item.name for item in self.inventory))

    def add_item(self, item: Item) -> None:
        """
        Add a new item to the player's inventory.
        """
        self.inventory.append(item)

    def remove_item(self, item: Item) -> None:
        """
        Removes an item from the player's inventory.
        """
        self.inventory.remove(item)

    def calc_score(self) -> int:
        """
        calculate the users score depending on the items they have deposited.
        """
        self.score = sum(item.target_points for item in self.inventory)
        return self.score


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
