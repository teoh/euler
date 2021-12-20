
def is_mult_of_3_or_5(n):
    return not (n % 3 and n % 5)

def solution(n):
    res = 0
    for i in range(1, n):
        if is_mult_of_3_or_5(i):
            res += i
    return res

def main():
    print(solution(1000))

if __name__ == "__main__":
    main()
