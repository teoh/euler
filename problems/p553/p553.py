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


def generate_choose(N):
    choose = [[0 for j in range(N+1)] for i in range(N+1)]
    for i in range(N+1):
        for j in range(i+1):
            if not j:
                choose[i][j] = 1
            else:
                choose[i][j] = (choose[i-1][j-1] + choose[i-1][j]) % MOD
    return choose


def generate_r_count(N):
    r_count = [0 for i in range(N+1)]
    for i in range(1, N+1):
        term1 = (2 * r_count[i-1]) % MOD
        term2 = (r_count[i-1] + 2) % MOD
        term3 = (term1 * term2) % MOD
        r_count[i] = (term3 + 1) % MOD
    return r_count


def generate_rbar(N, r_count, choose):
    rbar = [0 for i in range(N+1)]
    rbar[1] = 1
    for n in range(2, N+1):
        rbar[n] += r_count[n]
        for i in range(1, n):
            rbar[n] -= (choose[n][i] * rbar[i]) % MOD
            rbar[n] %= MOD
    return rbar


def solution(N, K):
    print("Doing for N={}, K={}".format(N, K))

    with catchtime("choose") as t:
        choose = generate_choose(N)

    with catchtime("r_count") as t:
        r_count = generate_r_count(N)
    # print(r_count)

    with catchtime("rbar") as t:
        rbar = generate_rbar(N, r_count, choose)
    # print(rbar)

    with catchtime("cbar") as t:
        # init c-bar
        cbar = [[0 for j in range(K+1)] for i in range(N+1)]

        # for every n, number of labels
        for n in range(1, N+1):
            print(f"doing n={n}")
            # for every k, number of connected components
            for k in range(2, K+1):
                # base cases:
                if n == k:
                    cbar[n][k] = 1
                    print(f"n={n}, k={k}, breaking...")
                    break
                else:
                    # get cbar(n, k)
                    for j in range(n-k+1):
                        term1 = (choose[n-1][j] * cbar[j+1][1]) % MOD
                        cbar[n][k] += (term1 * cbar[n-j-1][k-1]) % MOD
                        cbar[n][k] %= MOD

                # print(f"n={n}, k={k}, cbar[{n}][{k}]={cbar[n][k]}, c[{n}][{k}]={c[n][k]}")
            # handle cbar(n, 1) separately
            # initialize cbar[n][1] to be # graphs with exactly n labels
            # if n == 3:
            #     import pdb; pdb.set_trace()
            cbar[n][1] = rbar[n]
            # subtract counts of graphs with exactly n labels AND > 1 connected components
            for i in range(n-1):
                term1 = (choose[n-1][i] * cbar[i+1][1]) % MOD
                cbar[n][1] -= (term1 * rbar[n-i-1]) % MOD
                cbar[n][1] %= MOD
            # if n == 3:
            #     import pdb; pdb.set_trace()

    # pprint.pprint(cbar, width=200)
    # pprint.pprint(rbar, width=50)
    # pprint.pprint(r_count, width=50)

    solution = 0
    for i in range(1, N+1):
        solution += (choose[n][i] * cbar[i][K]) % MOD
        solution %= MOD
    return solution


def main(N, K):
    print(solution(N, K))


if __name__ == "__main__":
    options, args = parser.parse_args()

    N = int(options.number)
    K = int(options.knumber)
    assert N is not None, "N needs to be a number"
    assert K is not None, "K needs to be a number"
    main(N, K)
