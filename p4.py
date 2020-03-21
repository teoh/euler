import optparse
import time

parser = optparse.OptionParser()
parser.add_option('-N', '--number')

def is_palindrome(k):
    return str(k) == str(k)[::-1]

def solution(N):
    print("Doing for N={}".format(N))
    print("Number of digits to look: {}".format(N))
    N_digit_numbers = range(10**(N-1), 10**N)
    highest = -1
    factors = None
    for lower in N_digit_numbers:
        print(lower)
        for upper in range(lower, N_digit_numbers[-1]):
            prod = lower * upper
            if is_palindrome(prod) and prod > highest:
                highest = prod
                factors = lower, upper
    print(factors)
    return highest

def main(N):
    start = time.time()
    print(solution(N))
    end = time.time()
    print("Elapsed: {}".format(end - start))

if __name__ == "__main__":
    options, args = parser.parse_args()

    N = int(options.number)
    assert N is not None, "N needs to be a number"
    main(N)
