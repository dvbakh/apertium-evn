import re


letters = [['ś', 's'], ['ď', 'd']]
remove_pattern = re.compile("-Ø|̄|'|’|\(.+?\)")
separators_pattern = re.compile("[-=]+")


def get_macrons(cyrillic):
    """
    Get vowels + indexes before macrons.

    :param cyrillic: a string in Cyrillic
    :return: a list, which consists of tuples of vowels + indexes before macrons

    :example:
    >>> get_macrons('че̄рка̄шиним')
    [('е', 1), ('а', 4)]
    """

    macrons = []

    for c in range(len(cyrillic) - 1):

        if cyrillic[c+1] == '̄':
            vowel = cyrillic[c]
            index = c - cyrillic[:c].count('̄')
            macrons.append((vowel, index))

    return macrons


def add_macrons(cyrillic, macrons, sep=' '):

    """
    Add macrons using stored vowels + indexes.

    :param cyrillic: a string in Cyrillic (optionally segmented with spaces, etc.)
    :param macrons: a list, which consists of tuples of vowels + indexes before macrons
    :param sep: a separator used in segmentation
    :return: a string in Cyrillic with macrons

    :example:
    original word:   'че̄рка̄шиним'
    segmented word:  'черка шини м'
    expected output: 'че̄рка̄ шини м'

    >>> cyrillic = 'черка шини м'
    >>> macrons = [('е', 1), ('а', 4)]
    >>> add_macrons(cyrillic, macrons)
    'че̄рка̄ шини м'

    >>> cyrillic = 'бологида̄дӯ̄'
    >>> macrons = get_macrons(cyrillic)
    >>> segmented = 'боло гида ду'
    >>> add_macrons(segmented, macrons)
    'боло гида̄ дӯ'
    """

    result = list(cyrillic)
    m = 0
    ind = 0

    for i in range(len(result)):

        if result[i] == sep:
            continue

        elif ind == macrons[m][1] and \
             result[i] == macrons[m][0]:

            result[i] += '̄'
            ind += 1

            if m + 1 < len(macrons):
                m += 1
            else:
                break

        else:
            ind += 1

    return ''.join(result)


def check_next_segmented(cyrillic, c, segmented, s):
    """
    Check if a symbol in a in a segmented transcription should be skipped.

    :param cyrillic: a string in Cyrillic
    :param c: index of the current symbol in cyrillic
    :param segmented: a string with segmented transcription
    :param s: index of the current symbol in segmented
    :return: bool
    """

    iotised = all([cyrillic[c] in set('яеёюи'),
                   segmented[s] == 'j'])

    ts = all([cyrillic[c] == 'ц',
              segmented[s:s+2] == 'ts'])

    return iotised or ts


def check_next_cyrillic(cyrillic, c, segmented, s):
    """
    Check if a symbol in a Cyrillic string should be skipped.

    :param cyrillic: a string in Cyrillic
    :param c: index of the current symbol in cyrillic
    :param segmented: a string with segmented transcription
    :param s: index of a current symbol in segmented
    :return: bool
    """

    ng = all([segmented[s] == 'ŋ',
              cyrillic[c:c+2] == 'нг'])

    ss = all([segmented[s:s+3].count('s') == 1,
              cyrillic[c:c+2] == 'сс'])

    bz = all([segmented[s:s+2] == 'bz',
              cyrillic[c:c+2] == 'бо'])

    soft = cyrillic[c] == 'ь'

    return ng or ss or bz or soft


def segment(cyrillic, segmented, sep=' '):
    """
    Segment a Cyrillic string.

    :param cyrillic: a string in Cyrillic
    :param segmented: a string with segmented transcription
    :param sep: a separator used in segmentation
    :return: a segmented string in Cyrillic

    :example:
    >>> segment('уютчэӈнэркэл', 'uju-t-čə-ŋnə-rkə-l')
    'ую т чэ ӈнэ ркэ л'
    """

    if not separators_pattern.search(segmented):
        return cyrillic

    segmented = remove_pattern.sub('', segmented)
    segmented = separators_pattern.sub('-', segmented)
    for l in letters:
        segmented = segmented.replace(l[0], l[1])

    cyrillic = separators_pattern.sub('', cyrillic)
    macrons = get_macrons(cyrillic)
    cyrillic = cyrillic.replace('̄', '')

    result = ''
    c, s = 0, 0

    while c < len(cyrillic) and s < len(segmented):

        if check_next_segmented(cyrillic, c, segmented, s):
            s += 1

        elif segmented[s] == '-' or segmented[s] == '=':
            result += sep
            s += 1

        else:
            result += cyrillic[c]

            if not check_next_cyrillic(cyrillic, c, segmented, s):
                s += 1
            c += 1

    if macrons:
        result = add_macrons(result, macrons)
    result = result.replace(' ь', 'ь ')

    return result


def get_cyrillic_segmented(cyrillic, segmented_list, sep=' '):
    """
    Get possible segmentations for a string in Cyrillic.

    :param cyrillic: a string in Cyrillic
    :param segmented_list: a list of possible segmentations
    :param sep: a separator used in segmentation
    :return: a list of segmentations in Cyrillic

    >>> cyrillic = 'горово'
    >>> segmented = ['goro-wo', 'gorowo', 'gorowo=']
    >>> get_cyrillic_segmented(cyrillic, segmented)
    ['горо во', 'горово']
    """

    cyrillic_segmented = []

    for seg in segmented_list:

        if not seg:
            continue

        result = segment(cyrillic, seg, sep=sep)

        if separators_pattern.sub('', cyrillic) == re.sub(sep, '', result):
            if result not in cyrillic_segmented:
                cyrillic_segmented.append(result.strip(' '))

        else:
            print('The output letters don\'t match the input: {}, {}, {}'.format(cyrillic, seg, result))

    return list(cyrillic_segmented)
