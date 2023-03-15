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

        # init r-bar
        rbar = [0 for i in range(N+1)]

        # for ever n, number of labels
        for n in range(1, N+1):
            row_total = 0
            # for every k, number of connected components
            for k in range(2, N+1):
                # base cases:
                if n == k:
                    cbar[n][k] = 1
                    c[n][k] = 1
                    print(f"n={n}, k={k}, breaking...")
                elif k > n:
                    break
                else:
                    # get cbar(n, k)
                    for j in range(n-k+1):
                        term1 = (i_choose_j[n-1][j] * cbar[j+1][1]) % MOD
                        cbar[n][k] += (term1 * cbar[n-j-1][k-1]) % MOD

                    # c(n, k) = sum_i(1->n) n_choose_i * cbar(i, k)
                    for i in range(1, n+1):
                        term1 = (i_choose_j[n][i] * cbar[i][k]) % MOD
                        c[n][k] = (c[n][k] + term1) % MOD

                cbar[n][k] %= MOD
                c[n][k] %= MOD
                row_total = (row_total + cbar[n][k]) % MOD
                # print(f"n={n}, k={k}, cbar[{n}][{k}]={cbar[n][k]}, c[{n}][{k}]={c[n][k]}")
            # handle cbar(n, 1) separately
            num_graphs_below_n_labels = sum([(i_choose_j[n][i] * rbar[i]) % MOD for i in range(n)])
            expected_rbar = (r_count[n] - num_graphs_below_n_labels) % MOD
            cbar[n][1] = expected_rbar - row_total
            cbar[n][1] %= MOD
            rbar[n] = expected_rbar

            # handle c(n, 1) separately
            for i in range(1, n+1):
                term1 = (i_choose_j[n][i] * cbar[i][1]) % MOD
                c[n][1] = (c[n][1] + term1) % MOD

            # print(f"n={n}, k={1}, cbar[{n}][{1}]={cbar[n][1]}, c[{n}][{1}]={c[n][1]}")
            # print(f"cbar[{n}][*]={cbar[n]}, c[{n}][*]={c[n]}, rbar[{n}]={rbar[n]}\n")

    # pprint.pprint(c, width=200)
    pprint.pprint(cbar, width=200)
    pprint.pprint(rbar, width=50)
    pprint.pprint([sum(row) % MOD for row in cbar])
    pprint.pprint(r_count, width=50)
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
