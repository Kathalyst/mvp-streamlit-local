import erdantic as erd
from erdantic.examples.pydantic import Party
from dataclasses import dataclass

# Easy one-liner
erd.draw(Party, out="diagram5.png")

# Or create a diagram object that you can inspect and do stuff with
# diagram = erd.create(Party)
# diagram.models
# #> [PydanticModel(Adventurer), PydanticModel(Party), PydanticModel(Quest), PydanticModel(QuestGiver)]
# diagram.draw("diagram.png")

print(Party)
print(type(Party))
# print(Party.members)
print(Party.model_fields)

# Python program to illustrate use of exec to
# execute a given code as string.

# function illustrating how exec() functions.
def exec_code():
	LOC = """
a = 5
def factorial(num):
	fact=1
	for i in range(1,num+1):
		fact = fact*i
	return fact
print(factorial(5))
"""
	exec(LOC)
	
# Driver Code
exec_code()


class Function:
    def __init__(self, name):
        self.function_name = name

@dataclass
class Experiment:
	funct3: Function
	funct: Function
	name: str
	integer: int 

@dataclass
class Experiment2:
      func: Function


diagram = erd.create(Experiment)

diagam.draw("diagram4.png")

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Alignment(str, Enum):
    LAWFUL_GOOD = "lawful_good"
    NEUTRAL_GOOD = "neutral_good"
    CHAOTIC_GOOD = "chaotic_good"
    LAWFUL_NEUTRAL = "lawful_neutral"
    TRUE_NEUTRAL = "true_neutral"
    CHAOTIC_NEUTRAL = "chaotic_neutral"
    LAWFUL_EVIL = "lawful_evil"
    NEUTRAL_EVIL = "neutral_evil"
    CHAOTIC_EVIL = "chaotic_evil"


@dataclass
class Adventurer:
    """A person often late for dinner but with a tale or two to tell.

    Attributes:
        name (str): Name of this adventurer
        profession (str): Profession of this adventurer
        level (int): Level of this adventurer
        alignment (Alignment): Alignment of this adventurer
    """

    name: str
    profession: str
    level: int
    alignment: Alignment


@dataclass
class QuestGiver:
    """A person who offers a task that needs completing.

    Attributes:
        name (str): Name of this quest giver
        faction (str): Faction that this quest giver belongs to
        location (str): Location this quest giver can be found
    """

    name: str
    faction: Optional[str]
    location: str


@dataclass
class Quest:
    """A task to complete, with some monetary reward.

    Attributes:
        name (str): Name by which this quest is referred to
        giver (QuestGiver): Person who offered the quest
        reward_gold (int): Amount of gold to be rewarded for quest completion
    """

    name: str
    giver: QuestGiver
    reward_gold: int


@dataclass
class Party:
    """A group of adventurers finding themselves doing and saying things altogether unexpected.

    Attributes:
        name (str): Name that party is known by
        formed_datetime (datetime): Timestamp of when the party was formed
        members (List[Adventurer]): Adventurers that belong to this party
        active_quest (Optional[Quest]): Current quest that party is actively tackling
    """

    name: str
    formed_datetime: datetime
    members: List[Adventurer]
    active_quest: Optional[Quest]

