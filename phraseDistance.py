
def ph_distance(base_phrase, input_phrase):
    a_string = str(base_phrase).lower()
    b_string = str(input_phrase).lower()

    n = len(a_string)+1
    m = len(b_string)+1

    d = [[0]*m for i in range(n)]

    for i in range(n):
        d[i][0] = i

    for j in range(m):
        d[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            c = 0 if a_string[i-1] == b_string[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+c)
    return d[n-1][m-1]
