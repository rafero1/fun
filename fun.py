from collections import OrderedDict

class Roman:
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    @staticmethod
    def write(num):
        def roman_num(num):
            for r in Roman.roman.keys():
                x, y = divmod(num, r)
                yield Roman.roman[r] * x
                num -= (r * x)
                if num <= 0:
                    break

        return "".join([a for a in roman_num(num)])

class Rank:
    def __init__(self, exp_cost, stat_gain):
        self.exp_cost = exp_cost
        self.stat_gain = stat_gain

class RankGroup:
    def __init__(self, rank_array):
        self.rank_array = rank_array

    def get_max_rank(self):
        return len(self.rank_array)

    def get_rank(self, rank):
        return self.rank_array[rank-1]

    def get_cumulative_stat_gain(self, rank):
        return sum([r.stat_gain for r in self.rank_array[:rank]])

class Scaling:
    def __init__(self, base, stat):
        self.base = base
        self.stat = stat

class Skill:
    # TODO mastery reward
    def __init__(self, name, rank, rank_group, s_type, element, targets, value, base_cost, scaling, description=""):
        self.name = name
        self.rank = rank
        self.rank_group = rank_group
        self.s_type = s_type
        self.element = element
        self.targets = targets
        self.value = value
        self.base_cost = base_cost
        self.scaling = scaling
        self.description = description

    def get_num_ranks(self):
        return self.rank_group.get_max_rank()

    def get_name_at_rank(self, rank):
        return "{} {}".format(self.name, Roman.write(rank))

    def get_name_rank(self):
        return self.get_name_at_rank(self.rank)

    def get_value_at_rank(self, rank, stat):
        return (self.value + self.rank_group.get_cumulative_stat_gain(rank)) * (self.scaling.base * stat)

    def get_value(self, stat):
        return self.get_value_at_rank(self.rank, stat)

class Actor:
    # resistances
    def __init__(self, name, hp, mp, str, dex, con, int, wis, cha, skills):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.skills = skills

    def get_skill(self, name):
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def get_stat(self, stat):
        return self.__getattribute__(stat)

    def set_stat(self, stat, value):
        return self.__setattr__(stat, value)

    def use_skill(self, skill, target):
        if skill.s_type == "attack":
            target.dec_hp(skill.get_value(self.get_stat(skill.scaling.stat)))
        elif skill.s_type == "heal":
            target.inc_hp(skill.get_value(self.get_stat(skill.scaling.stat)))
        self.dec_mp(skill.base_cost)

    def inc_hp(self, hp):
        self.hp += hp

    def dec_hp(self, hp):
        self.hp -= hp

    def inc_mp(self, mp):
        self.mp += mp

    def dec_mp(self, mp):
        self.mp -= mp

skills = [
    Skill("Fireball", 1, RankGroup([Rank(0, 0), Rank(25, 5), Rank(50, 4), Rank(100, 3)]), "attack", "fire", 1, 5, 5, Scaling(.2, "int"), "A fireball."),
    Skill("Fire Shower", 1, RankGroup([Rank(0, 0), Rank(25, 5), Rank(50, 4), Rank(100, 3)]), "attack", "fire", 3, 10, 5, Scaling(.2, "int"), "A shower of fire."),
]

char = Actor(
    name="Test",
    hp=50,
    mp=15,
    str=10,
    dex=10,
    con=10,
    int=10,
    wis=10,
    cha=10,
    skills=[skills[0], skills[1]]
)

for skill in char.skills:
    for i in range(1, skill.get_num_ranks()+1):
        print("{}: {}".format(skill.get_name_at_rank(i), skill.get_value_at_rank(i, char.get_stat(skill.scaling.stat))))
