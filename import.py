def import_from_csv(filename):
    f = open(filename)
    parsed = []
    for s in f:
        parsed.append(s.split(','))
    objects = [{'category': p[0], 'name': p[1], 'slug': p[2], 'sizes': p[3:-1], 'price': p[-1]} for p in parsed[3:]]

    i = 0
    sizes = []
    for p in parsed[1][2:-1]:
        sizes.append((p, parsed[1][3+i], parsed[0][3+i]))
        i += 1

    print sizes

