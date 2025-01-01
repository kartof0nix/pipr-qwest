TRANSPARENT = None

class item:
    foreground = ''
    def resize(s, offset_x, offset_y, x, y):
        s.x = x
        s.y = y
        s.off_x = offset_x
        s.off_y = offset_y
    def __init__(s, offset_x, offset_y, x, y):
        s.resize(offset_x, offset_y, x, y)


    def sketch(s):
        grid = [[None for i in range(s.y)] for j in range(s.x)]
        clr = [[s.foreground for i in range(s.y)] for j in range(s.x)]
        return (grid, clr)
    
    def draw(s, char, style):
        a = s.sketch()
        for i in range (s.x):
            for j in range (s.y):

                if(a[0][i][j] != TRANSPARENT):
                    char[i + s.off_x][j + s.off_y] = a[0][i][j]
                style[i + s.off_x][j + s.off_y] += a[1][i][j]
