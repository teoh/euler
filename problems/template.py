import optparse

parser = optparse.OptionParser()
parser.add_option('-N', '--number')

def solution(N):
    print("Doing for N={}".format(N))
    pass

def main(N):
    print(solution(N))

if __name__ == "__main__":
    options, args = parser.parse_args()

    N = int(options.number)
    assert N is not None, "N needs to be a number"
    main(options.number)
