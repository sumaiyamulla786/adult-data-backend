def getPersonsCount(persons):
    result = {}
    genders = ['Male', 'Female']
    for gender in genders:
        result[f'total{gender}s'] = persons.count_documents({"sex": f'{gender}'})
    relationships = ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried']
    for relation in relationships:
        result[f'total{kebabToCamel(relation)}s'] = persons.count_documents({"relationship": f'{relation}'})
    return result

def kebabToCamel(key):
    keySplit = key.split('-')
    keySplit = list(map(lambda x: x.capitalize(), keySplit))
    return ''.join(keySplit)
