import math
import time

def check_prime(i, primes):
    for j in primes:
        if j > math.sqrt(i):
            break
        if j > 2 and i % j == 0:
            return False
    return True

def get_primes_up_to(N):
    primes = [0, 2]
    if N > 2:
        for i in range(3, N, 2):
            if check_prime(i, primes):
                primes.append(i)
    return primes

def get_c_sum(primes):
    c_sum = []
    for i, p in enumerate(primes):
        if i > 0:
            c_sum.append(c_sum[-1] + p)
        else:
            c_sum.append(p)
    return c_sum

def update(best_prime, largest_size, best_idxs, this_sum, l_idx, r_idx, prime_set):
    this_size = r_idx - l_idx
    if this_sum in prime_set and this_size > largest_size:
        best_prime, largest_size, best_idxs = this_sum, this_size, (l_idx, r_idx)
    return best_prime, largest_size, best_idxs

def main():
    print("hi")
    N = 1000000
    # N = 1000
    # N = 100
    start = time.time()
    primes = get_primes_up_to(N)
    prime_set = set(primes[1:])
    elapsed = time.time() - start
    print(f"N={N}; elapsed: {elapsed}")
    print(f"len(primes)={len(primes)}")

    start = time.time()
    r_idx = 1

    largest_size = -1
    best_prime = -1
    best_idxs = (0, 0)

    c_sum = get_c_sum(primes)
    for l_idx in range(0, len(c_sum)):
        if l_idx > r_idx:
            break
        # start with some sum
        test_sum = c_sum[r_idx] - c_sum[l_idx]

        # if test_sum is less than N, go up, check primes, and stop on ce you exceed N
        if test_sum < N:
            while c_sum[r_idx] - c_sum[l_idx] < N:
                # run update
                best_prime, largest_size, best_idxs = update(best_prime,
                                                             largest_size,
                                                             best_idxs,
                                                             c_sum[r_idx] - c_sum[l_idx],
                                                             l_idx,
                                                             r_idx,
                                                             prime_set)
                # increment
                r_idx += 1
        else:
            # if test_sum is >= N, go down and stop at the first prime you see
            found_prime = False
            while not found_prime:
                if c_sum[r_idx] - c_sum[l_idx] < N:
                    best_prime, largest_size, best_idxs = update(best_prime,
                                                                 largest_size,
                                                                 best_idxs,
                                                                 c_sum[r_idx] - c_sum[l_idx],
                                                                 l_idx,
                                                                 r_idx,
                                                                 prime_set)
                    found_prime = (c_sum[r_idx] - c_sum[l_idx]) in prime_set
                # increment
                r_idx -= 1

    elapsed = time.time() - start
    print(f"elapsed: {elapsed}")
    print(f"best_prime={best_prime}")
    print(f"largest_size={largest_size}")
    # print(f"primes={primes}")
    # print(f"c_sum={c_sum}")
    print(f"best_idxs={best_idxs}")

if __name__ == "__main__":
    main()
