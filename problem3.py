import math

def is_prime(k):
    lim = int(math.sqrt(k)) + 1
    if k == 2: return True
    for i in range(2, lim+1):
        if k % i == 0:
            return False
    return True

def solution(N):
    limit = int(math.sqrt(N)) + 1
    print(limit)
    largest = -1
    for factor in range(1, limit+1):
        if is_prime(factor) and N % factor == 0:
            print("Prime factor: {}".format(factor))
            largest = factor
    return largest

def main():
    print(solution(600851475143))

if __name__ == "__main__":
    main()
