import json
import random


class SupportTracker:

    def __init__(self, json_filename):
        self.filename = json_filename
        with open(self.filename) as f:
            self.content = json.load(f)
        self.support_conversations_dict = {"A": 3, "B": 2, "C": 1, "N/A": 0}

    def save(self):
        """ Saves self. content to json_filename."""
        # print (self.content)
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.content))

    def get_total_progress(self):
        """ Returns as an integer percent (rounded down) the number of completed support conversations.
        """
        total_supports = 0
        curr_supports = 0
        for character in self.content:
            for partner_data in self.content[character]:
                total_supports += 3
                curr_supports += self.support_conversations_dict[partner_data["finished"]]
                # print (total_supports, curr_supports)
        return int(curr_supports / total_supports * 100)

    def get_current_pairs(self):
        """ Returns as list of tuples the currently active pairs in the form
        char1, char2, current support level
        """
        result = set([])
        for character in self.content:
            for partner_data in self.content[character]:
                if partner_data["in_progress"]:
                    char1, char2 = sorted([character, partner_data["partner"]])
                    result.add((char1, char2, partner_data["finished"]))
        return list(result)

    def get_finished_pairs(self):
        """ Returns as list of tuples the currently active pairs in the form
        char1, char2
        """
        result = set([])
        for character in self.content:
            for partner_data in self.content[character]:
                if partner_data["finished"] == "A":
                    char1, char2 = sorted([character, partner_data["partner"]])
                    result.add((char1, char2))
        return sorted(list(result))

    def get_unpaired_characters(self):
        """ Returns list of characters which are not currently paired. """
        result = []
        for char in self.content:
            skip = False
            for pair in self.get_current_pairs():
                if char == pair[0] or char == pair[1]:
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
        n = len(chars)
        check_idx = random.randint(0, n - 1)
        check_count = 0
        while check_count < n:
            curr = chars[check_idx]
            m = len(self.content[curr])
            partner_idx = random.randint(0, m - 1)
            partner_count = 0
            while partner_count < m:
                partner_data = self.content[curr][partner_idx]
                if partner_data["partner"] not in chars or partner_data["finished"] == "A":
                    partner_idx = (partner_idx + 1) % m
                    partner_count += 1
                else:
                    return curr, partner_data["partner"]
            check_idx = (check_idx + 1) % n
            check_count += 1
        return None

    def add_new_random_pair(self):
        """ Adds a random new pair to the tracker with no support level.
        """
        char1, char2 = self.get_new_pair()
        self.set_current(char1, char2)

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


def demo_update(tracker):
    tracker.reset_all()
    tracker.update_pair("Eirika", "Ephraim", "A")
    tracker.update_pair("Gilliam", "Franz", "A")
    tracker.update_pair("Kyle", "Colm", "A")
    tracker.update_pair("Joshua", "Natasha", "A")
    tracker.update_pair("Tethys", "Gerik", "A")
    tracker.update_pair("Artur", "Cormag", "A")
    tracker.update_pair("Innes", "Tana", "A")
    tracker.update_pair("Knoll", "Duessel", "A")
    tracker.update_pair("Dozla", "L'Arachel", "A")
    tracker.set_current("Eirika", "Ephraim")
    tracker.set_current("Gilliam", "Franz")
    tracker.set_current("Kyle", "Colm")
    tracker.set_current("Joshua", "Natasha")
    tracker.set_current("Tethys", "Gerik")
    tracker.set_current("Artur", "Cormag")
    tracker.set_current("Innes", "Tana")
    tracker.set_current("Knoll", "Duessel")
    tracker.set_current("Dozla", "L'Arachel")


if __name__ == "__main__":
    s = SupportTracker("support_data.json")
    demo_update(s)

