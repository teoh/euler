import optparse
import math


parser = optparse.OptionParser()
parser.add_option('-N', '--number')

FILE_PATH = "base_exp.txt"
def solution(N):
    print("Doing for N={}".format(N))
    with open(FILE_PATH) as f:
        lines = f.readlines()
    best_val = float("-inf")
    best_line = None
    for i, l in enumerate(lines):
        b, e = l.strip().split(',')
        b, e = int(b), int(e)
        log_val = e * math.log(b)
        if log_val > best_val:
            best_val = log_val
            best_line = i+1
    return best_line

def main(N):
    print(solution(N))

if __name__ == "__main__":
    options, args = parser.parse_args()

    N = int(options.number)
    assert N is not None, "N needs to be a number"
    main(options.number)
