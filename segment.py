import re
import os
import sys
import hfst


def revert_spellrelax(word, seg, sep=' '):
    """
    Converts a segmented word to the original spelling
    (revert the changes by spellrelax).

    :param word: a word (str)
    :param seg: a segmented word (str)
    :return: a segmented word with original spelling (str)
    """

    if 'һ' in word:
        seg = seg.replace('х', 'һ')

    if seg.replace(sep, '').replace('в', 'ф').replace('̄', '') == word.replace('̄', ''):
        seg = seg.replace('в', 'ф')

    if seg.replace(sep, '').replace('̄', '') == word:
        seg = seg.replace('̄', '')

    if seg.replace(sep, '') == word:
        return seg

    elif '̄' in word or 'ӈ' in seg or 'в' in seg or 'с' in seg:
        seg_list = list(seg)
        word_list = list(word)
        j = 0

        for i in range(len(seg_list)):

            if len(word) <= j:
                seg_list = seg_list[:i]
                break

            if seg_list[i] == sep:
                continue

            elif seg_list[i] == word_list[j]:
                j += 1

            elif seg_list[i] == '̄':
                seg_list[i] = ''
                continue

            elif word_list[j] == '̄':
                seg_list.insert(i, '̄')
                j += 1

            elif seg_list[i] == 'ӈ':
                if len(word_list) > j + 1 and \
                    word_list[j] + word_list[j+1] == 'нг':
                    seg_list[i] = 'нг'
                    j += 2

                elif word_list[j] == 'н':
                    seg_list[i] = 'н'
                    j += 1

                else:
                    break

            elif word_list[j] == 'ф' and seg_list[i] == 'в':
                seg_list[i] = 'ф'
                j += 1

            elif word_list[j] == 'х' and seg_list[i] == 'с':
                seg_list[i] = 'х'
                j += 1

            elif word_list[j] == 'һ' and seg_list[i] == 'с':
                seg_list[i] = 'һ'
                j += 1

            elif word_list[j] == 'ш' and seg_list[i] == 'с':
                seg_list[i] = 'ш'
                j += 1

            else:
                break

        seg = ''.join(seg_list)

        if seg.replace(sep, '') == word:
            return seg
    return


def segment(word, segmenter, sep=' '):
    """
    Segments a word and returns the segmentations that correspond
    to the original spelling.

    :param word: a word (str)
    :param segmenter: a path to the HFST transducer for segmentation (str)
                      or HFST transducer (libhfst.HfstTransducer)
    :return: a list of segmentations in the original spellimg
    """

    if isinstance(segmenter, str):
        if not os.path.exists(segmenter):
            raise ValueError('The segmenter could not be found!')
        segmenter = hfst.HfstInputStream(path).read()

    segmentation = segmenter.lookup(word)

    res = []
    for seg in segmentation:
        seg = re.sub('·+', sep, seg[0])

        reverted = revert_spellrelax(word, seg)
        if reverted and reverted not in res:
            res.append(reverted)

    return res


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('segment.py <word>')
        sys.exit(-1)

    word = sys.argv[1]

    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = 'evn.segmenter.hfst'

    segmented = segment(word, path)

    if len(segmented) == 1:
        print(segmented[0])
    else:
        print(', '.join(segmented))
