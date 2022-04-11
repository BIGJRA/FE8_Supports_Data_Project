""" SupportTracker class for JSON and GUI interactivity
"""
import json
import random

from data.sorts import fe8_sort, fe7_sort


class SupportTracker:
    """ SupportTracker class for data load and GUI representation
    """
    def __init__(self, json_filename):
        self.filename = json_filename
        if "fe7" in self.filename:
            self.game = "fe7"
        elif "fe8" in self.filename:
            self.game = "fe8"
        else:  # placeholder for errors
            self.game = "fe8"
        with open(self.filename, encoding='utf-8') as file:
            self.content = json.load(file)
        self.support_conversations_dict = {"A": 3, "B": 2, "C": 1, "N/A": 0}

    def get_game(self):
        """
        :return: str
        Returns the name of the game (fe7, fe8)
        """
        return self.game

    def save(self):
        """ Saves self. content to json_filename."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.content))

    def get_rank(self, char1, char2):
        """
        :param char1: str
        :param char2: str
        :return: str
        Returns the rank as a string of the support between the pair
        """
        for thing in self.content[char1]:
            if thing['partner'] == char2:
                return thing['finished']
        return "No pairing found."

    def get_in_progress(self, char1, char2):
        """
        :param char1: str
        :param char2: str
        :return: str
        Returns the progress/status as a string of the support between the pair
        """
        for thing in self.content[char1]:
            if thing['partner'] == char2:
                return thing['in_progress']
        return "No pairing found."

    def get_total_progress(self):
        """ Returns as an integer percent the number of completed support conversations.
        """
        total_supports = 0
        curr_supports = 0
        for character in self.content:
            for partner_data in self.content[character]:
                total_supports += 3
                curr_supports += self.support_conversations_dict[partner_data["finished"]]
        return int(curr_supports / total_supports * 100)

    def get_all_pairs(self):
        """
        :return: list[str]
        Returns list of strings which represent all support pairs
        """
        result = set([])
        for character in self.content:
            for partner_data in self.content[character]:
                pair = [character, partner_data["partner"]]
                if self.game == 'fe8':
                    pair.sort(key=fe8_sort.index)
                else:  # self.game == 'fe7':
                    pair.sort(key=fe7_sort.index)
                result.add((pair[0], pair[1], partner_data["finished"]))
        return list(result)

    def get_current_pairs(self):
        """ Returns as list of tuples the currently active pairs in the form
        char1, char2, current support level
        """
        result = set([])
        for character in self.content:
            for partner_data in self.content[character]:
                # print (character, partner_data)
                if partner_data["in_progress"]:
                    pair = [character, partner_data["partner"]]
                    if self.game == 'fe8':
                        pair.sort(key=fe8_sort.index)
                    else:  # self.game == 'fe7':
                        pair.sort(key=fe7_sort.index)
                    result.add((pair[0], pair[1], partner_data["finished"]))
        return list(result)

    # '''def get_finished_pairs(self):
    #     """ Returns as list of tuples the currently active pairs in the form
    #     char1, char2
    #     """
    #     result = set([])
    #     for character in self.content:
    #         for partner_data in self.content[character]:
    #             if partner_data["finished"] == "A":
    #                 pair = [character, partner_data["partner"]]
    #                 pair.sort(key=lambda x: fe8_sort.index(x))
    #                 result.add((pair[0], pair[1], partner_data["finished"]))
    #     return sorted(list(result))'''

    def get_unpaired_characters(self):
        """ Returns list of characters which are not currently paired. """
        result = []
        for char in self.content:
            skip = False
            for pair in self.get_current_pairs():
                if char in (pair[0], pair[1]):
                    skip = True
                    break
            if not skip:
                result.append(char)
        return result

    def get_new_pair(self):
        """ Returns random tuple of characters with potential pairing from the unpaired characters.
        Only picks from the characters which have not yet reached A support.
        """
        chars = self.get_unpaired_characters()
        num_chars = len(chars)
        check_idx = random.randint(0, num_chars - 1)
        check_count = 0
        while check_count < num_chars:
            curr = chars[check_idx]
            num_partners = len(self.content[curr])
            partner_idx = random.randint(0, num_partners - 1)
            partner_count = 0
            while partner_count < num_partners:
                partner_data = self.content[curr][partner_idx]
                if partner_data["partner"] not in chars or partner_data["finished"] == "A":
                    partner_idx = (partner_idx + 1) % num_partners
                    partner_count += 1
                else:
                    return curr, partner_data["partner"]
            check_idx = (check_idx + 1) % num_chars
            check_count += 1
        return None

    def add_new_random_pair(self):
        """ Adds a random new pair to the tracker with no support level.
        """
        pair = self.get_new_pair()
        if pair is None:
            return
        self.set_current(pair[0], pair[1])

    def update_pair(self, char1, char2, level):
        """ Updates the entry for char1, char2 to be the given support level.
        """
        i = 0
        while self.content[char1][i]["partner"] != char2:
            i += 1
        self.content[char1][i]["finished"] = level
        i = 0
        while self.content[char2][i]["partner"] != char1:
            i += 1
        self.content[char2][i]["finished"] = level
        self.save()

    def set_current(self, char1, char2, is_current=True):
        """ Sets char1, char2 to have in_progress value is_current.
        """

        i = 0
        while self.content[char1][i]["partner"] != char2:
            i += 1
        self.content[char1][i]["in_progress"] = is_current
        i = 0
        while self.content[char2][i]["partner"] != char1:
            i += 1
        self.content[char2][i]["in_progress"] = is_current

        self.save()

    def start_new_run(self):
        """ Resets all pairs to be not current. """
        for char in self.content:
            for partner_data in self.content[char]:
                partner_data["in_progress"] = False
        self.save()

    def reset_all(self):
        """ Resets all pairs to default. """
        for char in self.content:
            for partner_data in self.content[char]:
                partner_data["finished"] = "N/A"
                partner_data["in_progress"] = False
        self.save()

    def find_char_index(self, char_name):
        """
        :param char_name: string
        :return: int
        Returns the index in the tracker that the character name's data is located at for storage
        """


if __name__ == "__main__":
    s = SupportTracker("data/fe8_support_data.json")
