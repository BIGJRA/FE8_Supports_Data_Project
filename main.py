import requests
import lxml.html as lh
import json


def get_table_rows(url, strip_word=None):
    """ Takes as input a string containing url.
    Returns a dictionary in the form of a tuple:
    Index 0 contains the table column name,
    Index 1 is a list of the text in the entries going down."""

    # Page handles the contents of url
    page = requests.get(url)

    # Store the contents of page
    doc = lh.fromstring(page.content)

    # Parse data stored in <tr> tags
    tr_elements = doc.xpath('//tr')

    # Create empty list
    col = []
    i = 0
    # For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        # print ('%d:"%s"' % (i, name))
        col.append((name, []))

    # Since out first row is the header, data is stored on the second row onwards
    for j in range(1, len(tr_elements)):
        # T is our jth row
        row_j = tr_elements[j]

        # column
        i = 0

        # Iterate through each element of the row
        for t in row_j.iterchildren():
            data = t.text_content()

            # Here it skips the row if the first element is strip_word. Helps solve a problem
            # in the serenes forest link which has internal table headers.
            if strip_word is not None and data == strip_word:
                break

            # Append the data to the empty list of the ith column
            col[i][1].append(data)
            # Increment i for the next column
            i += 1

    return {title: column for (title, column) in col}


def convert_to_character_dict(dictionary):
    """ Takes as input a column: values dictionary format that is obtained from serenes forest
    and returns a dictionary with key: character and values: list of support partners,
    represented as tuples (name, base, rate)."""

    result = {}
    for pos, character_name in enumerate(dictionary["Character"]):
        character_name = character_name.replace(' ', '')
        result[character_name] = []
        for option_num in range(1, len(dictionary)):

            # ignores if the text is simply "-"
            content = dictionary[f"Option {option_num}"][pos]
            if content == "–":
                break

            # extracts the three parts from data
            data = content.split()
            data_dict = {
                "partner" : data[0],
                "base" : int(data[1]),
                "rate" : int(data[-1][1:]),
                "finished" : False,
                "in_progress": False
                }
            result[character_name].append(data_dict)

    return result


def write_to_json(filename, dictionary):
    with open(filename, 'w') as f:
        f.write(json.dumps(dictionary))


if __name__ == "__main__":
    serenes = "https://serenesforest.net/the-sacred-stones/characters/supports/"
    d = get_table_rows(serenes, strip_word="Character")
    d = convert_to_character_dict(d)
    write_to_json('file.json', d)
