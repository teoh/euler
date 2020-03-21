def make_grid(N):
    return [[None for i in range(N)] for j in range(N)]

def solution(L):
    grid = make_grid(L+1)
    grid[0][0] = 1
    def dp(row, col):
        print("Checking row {} and col {}".format(row, col))
        if grid[row][col] is not None:
            print("Returning {} for row col {} {}".format(grid[row][col], row, col))
            return grid[row][col]
        else:
            from_left = 0 if col == 0 else dp(row, col-1)
            from_up = 0 if row == 0 else dp(row-1, col)
            grid[row][col] = from_left + from_up
            return grid[row][col]
    return dp(L, L)

def main():
    print(solution(20))

if __name__ == "__main__":
    main()
