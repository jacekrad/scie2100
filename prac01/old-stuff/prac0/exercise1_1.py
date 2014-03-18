def baseCounts(str, alphabet):
    d = {}
    for ch in alphabet:
        cnt = str.count(ch)
        d[ch] = cnt
    return d
