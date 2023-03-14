import optparse
import pprint
from time import perf_counter
from contextlib import contextmanager

parser = optparse.OptionParser()
parser.add_option('-N', '--number')
parser.add_option('-K', '--knumber')

pp = pprint.PrettyPrinter(indent=4)

@contextmanager
def catchtime(fn) -> float:
    print(f"{fn}: start")
    start = perf_counter()
    yield lambda: perf_counter() - start
    print(f"{fn}: finished in {perf_counter() - start:.3f} seconds")

MOD = 1_000_000_007

def generate_i_choose_j(N):
    res = [[0 for j in range(N+1)] for i in range(N+1)]
    for i in range(N+1):
        for j in range(i+1):
            if not j:
                res[i][j] = 1
            else:
                res[i][j] = (res[i-1][j-1] + res[i-1][j]) % MOD
    return res

def generate_r_count(N):
    res = [0 for i in range(N+1)]
    for i in range(1, N+1):
        term1 = (2 * res[i-1]) % MOD
        term2 = (res[i-1] + 2) % MOD
        term3 = (term1 * term2) % MOD
        res[i] = (term3 + 1) % MOD
    return res

def solution(N, K):
    print("Doing for N={}, K={}".format(N, K))

    with catchtime("i_choose_j") as t:
        i_choose_j = generate_i_choose_j(N)
    # pp.pprint(i_choose_j)
    # print(i_choose_j[6][4])

    print("Generating r_count...")
    with catchtime("r_count") as t:
        r_count = generate_r_count(N)
    print(r_count)
    print(MOD)

    print("Initializing c and cbar arrays...")
    with catchtime("c, cbar") as t:
        # init c array
        c = [[0 for j in range(N+1)] for i in range(N+1)]

        # init c-bar
        cbar = [[0 for j in range(N+1)] for i in range(N+1)]

        for n in range(1, N+1):
            row_total = 0
            for k in range(2, N+1):
                # base cases:
                if n == k:
                    cbar[n][k] = 1
                    c[n][k] = 1
                    row_total += 1
                elif n < k:
                    cbar[n][k] = 0
                    c[n][k] = 0
                    print(f"n={n}, k={k}, breaking...")
                    break
                else:
                    # get cbar(n, k)
                    for j in range(n-k+1):
                        term1 = (i_choose_j[n-1][j] * cbar[j+1][1]) % MOD
                        cbar[n][k] += (term1 * cbar[n-j-1][k-1]) % MOD

                    # update final c(n, k) = cbar(n, k) + n*c(n-1, k)
                    term1 = (n * c[n-1][k]) % MOD
                    c[n][k] = (cbar[n][k] + term1) % MOD

                    row_total += cbar[n][k]
                print(f"n={n}, k={k}, cbar[{n}][{k}]={cbar[n][k]}, c[{n}][{k}]={c[n][k]}")
            # handle cbar(n, 1) separately. needs sum_j(2->n) cbar(n, j)
            # print(f"n={n}, k={1}")
            print(f"n={n}, k={1}, r_count[{n}]={r_count[n]}, r_count[n-1]={r_count[n-1]}, row_total={row_total}")
            cbar[n][1] = r_count[n] - n * r_count[n-1] - row_total

            # handle c(n, 1) separately
            term1 = (n * c[n-1][1]) % MOD
            c[n][1] = (cbar[n][1] + term1) % MOD
            print(f"n={n}, k={1}, cbar[{n}][{1}]={cbar[n][1]}, c[{n}][{1}]={c[n][1]}")
            print(f"cbar[{n}][*]={cbar[n]}, c[{n}][*]={c[n]}\n")

    pp.pprint(c)
    pp.pprint(cbar)
    return c[N][K]


def main(N, K):
    print(solution(N, K))

if __name__ == "__main__":
    options, args = parser.parse_args()

    N = int(options.number)
    K = int(options.knumber)
    assert N is not None, "N needs to be a number"
    assert K is not None, "K needs to be a number"
    main(N, K)
