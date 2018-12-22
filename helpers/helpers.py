# takes the persons collection and calculates all the count for generating bar graph and pie chart
def getPersonsCount(persons):
    result = {}
    genders = ['Male', 'Female']
    for gender in genders:
        result[f'total{gender}s'] = persons.count_documents({"sex": f'{gender}'})
    relationships = ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried']
    for relation in relationships:
        result[f'total{splitAndCapitalize(relation)}s'] = persons.count_documents({"relationship": f'{relation}'})
    return result

# splits the string with dash and capitalizes and joins to convert to a json friendly format
def splitAndCapitalize(key):
    keySplit = key.split('-')
    keySplit = list(map(lambda x: x.capitalize(), keySplit))
    return ''.join(keySplit)
