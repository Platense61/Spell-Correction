# def fromBigTxt():
#     global big
#     big = file('big.txt').read()
#     N = len(big)
#     s = set()
#     for i in xrange(6, N):
#         c = big[i]
#         if ord(c) > 127 and c not in s:
#             print i, c, ord(c), big[max(0, i-10):min(N, i+10)]
#             s.add(c)
#     print s
#     print [ord(c) for c in s]