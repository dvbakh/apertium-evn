import re
from itertools import chain


def get_test_tags(analysis):
    """
    Makes a set with all test tags from the analyses of a wordform.

    :param analysis: a string with morphological tags in an Apertium stream format (str)
    :return: a set of test tags (set)

    :example:
    >>> analyses = (('бака<v><futcnt><p3><pl>', 0.0), \
                    ('бака<v><impf><nfut><p3><pl>', 0.0))
    >>> get_test_tags(analyses)
    {'<futcnt>', '<p3>', '<pl>', '<impf>', '<nfut>'}
    """

    test_tags = list(chain.from_iterable(ana[0].split('<')[2:]
                                         for ana in analysis))

    for i, tag in enumerate(test_tags):
        test_tags[i] = '<' + tag

    test_tags = set(test_tags)

    return test_tags


def get_ref_tags(glosses):
    """
    Makes a set with all reference tags from the glosses of a wordform from Siberian Lang.

    :param glosses: a dictionary with glosses (dict)
    :return: a set of reference tags (set)

    :example:
    >>> glosses = {"сделать-IPFV-NFUT-2SG": 4, \
                   "стать-FUTCNT-2SG": 1}
    >>> get_ref_tags(glosses)
    {'IPFV', 'NFUT', '2SG', 'FUTCNT'}
    """

    ref_tags = set()

    for gloss in glosses:

        if re.search('[-=]', gloss):
            ref_tags_splitted = re.split('[-=]+', gloss.strip('-='))

            # add the first tag to ref tags if it is not a translation
            if re.search('NEG|\d(SG|PL)|FOC', ref_tags_splitted[0].upper()):
                ref_tags.add(ref_tags_splitted[0])

            ref_tags.update(ref_tags_splitted[1:])

        # add the tag to ref tags if it is not a translation
        elif re.search('NEG|\d(SG|PL)|FOC', gloss.upper()):
            ref_tags.add(gloss)

        else:
            return 'skip'

    return ref_tags


def clean_ref_tag(ref_tag):
    """
    Removes additional symbols from glosses.

    :param ref_tag: a reference tag (str)
    :return: a corrected reference tag (str)

    :example:
    >>> clean_ref_tag('COM.FAM{*}.SLIP')
    'COM.FAM'
    """
    ref_tag = re.sub('\{.*?\}|\[.*?\]|\.SLIP|\?', '', ref_tag)
    ref_tag = ref_tag.strip('.]\?')
    return ref_tag


def evaluate_wordform(word, analyser, mapping, glosses,
                      tp, fp, fn, not_analysed, skipped):
    """
    Calculates true positives, false positives, false negatives between
    reference tags and test tags for a wordform and add to current numbers.
    If a wordform doesn't receive analysis, increases the number of not_analysed
    and adds the number of reference tags to false negatives.
    If a wordform doesn't have reference tags, increases the number of skipped.

    :param word: a word (str)
    :param analyser: a HFST transducer (libhfst.HfstTransducer)
    :param mapping: a mapping from reference tags to test tags (dict)
    :param glosses: a dictionary with glosses (dict)
    :param tp: true positives (int)
    :param fp: false positives (int)
    :param fn: false negatives (int)
    :param not_analysed: number of wordforms that don't receive analysis (int)
    :param skipped: number of wordforms that don't have reference tags (int)
    :return: a tuple of tp, fp, fn, not_analysed, skipped (tuple)
    """

    analysis = analyser.lookup(word)

    ref_tags = get_ref_tags(glosses)
    # skip words that do not contain tags
    if ref_tags == 'skip':
        skipped += 1
        return tp, fp, fn, not_analysed, skipped

    # finish if there are no analyses
    if not analysis:
        not_analysed += 1
        fn += len(ref_tags)
        return tp, fp, fn, not_analysed, skipped

    test_tags = get_test_tags(analysis)

    ref_tags_mapped = set()

    for gloss in ref_tags:
        ref_tag = mapping[clean_ref_tag(gloss).upper()]

        if isinstance(ref_tag, str):
            n = ref_tag.count('>')

            # if ref_tag doesn't contain <>,
            # then we should look for a test tag that contains the string in ref_tag
            # (this is for glosses like CONV that can correspond to any of the converbs)

            if n == 0:
                added = False
                for test_tag in test_tags:
                    if ref_tag in test_tag:
                        test_tags.remove(test_tag)
                        tp += 1
                        added = True
                        break

                # if it isn't found, then add to ref_tags_mapped
                # to count the difference between test and ref in the end
                if not added:
                    ref_tags_mapped.add(ref_tag)

            # if the ref_tag contains one <,
            # it directly corresponds to a test tag
            # so add to ref_tags_mapped

            elif n == 1:
                ref_tags_mapped.add(ref_tag)

            # if there are more than one tag in ref_tag,
            # we should split it to compare with test tags
            # (for example, 1PL(EXCL).ACC corresponds to <p1><pe><acc><def>)

            elif n > 1:
                ref_tags_splitted = ref_tag.split('>')
                ref_tags_splitted.remove('')

                for tag in ref_tags_splitted:
                    tag = tag + '>'
                    if tag in test_tags:
                        test_tags.remove(tag)
                        tp += 1

                    else:

                        # if it isn't found, then add to ref_tags_mapped
                        # to count the difference between test and ref in the end

                        ref_tags_mapped.add(tag)

        # if the ref_tag can correspond to more than one tag,
        # then we should check these tags in test tags
        # (for example, 1SG can correspond to <p1><sg> or to <px1sg>)

        elif isinstance(ref_tag, list):
            added = False
            for item in ref_tag:

                if isinstance(item, str) and item in test_tags:
                    test_tags.remove(item)
                    tp += 1
                    added = True
                    break

                elif isinstance(item, list) and set(item).issubset(test_tags):
                    test_tags = test_tags - set(item)
                    tp += 1
                    added = True
                    break

            if not added:
                fn += 1

    tp += len(test_tags & ref_tags_mapped)
    fp += len(test_tags - ref_tags_mapped)
    fn += len(ref_tags_mapped - test_tags)

    return tp, fp, fn, not_analysed, skipped