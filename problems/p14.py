
collatz_lens = {1: 1}

def collatz(k):
    if k % 2:
        return 3 * k + 1
    else:
        return k / 2

def get_collatz_seq_length(n):
    if n in collatz_lens:
        return collatz_lens[n]
    else:
        res = 1 + get_collatz_seq_length(collatz(n))
        # print("collatz length for n={}: {}".format(n, res))
        collatz_lens[n] = res
        return res

def solution(N):
    res = -1
    starting_num = None
    for i in range(1, N):
        print("doing i = {}".format(i))
        seq_len = get_collatz_seq_length(i)
        if seq_len > res:
            res = seq_len
            starting_num = i
    return starting_num

def main():
    print(solution(N=10**6))

if __name__ == "__main__":
    main()
