def solution(N):
    fibs = [1, 2]
    def generate_fib():
        while fibs[-1] < N:
            fibs.append(fibs[-1] + fibs[-2])

    generate_fib()
    print(fibs)
    return sum(list(filter(lambda n: n % 2 == 0, fibs[:-1])))

def main():
    print(solution(4 * 10**6))
    # print(solution(101))

if __name__ == "__main__":
    main()
