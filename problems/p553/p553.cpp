#include <iostream>
#include <cmath>
#include <vector>
using namespace std;
using namespace std::chrono;

// const long N = pow(10, 4);
// const long K = 10;

const long N = 100;
const long K = 10;

const long MOD = 1000000007;

long posMod(long raw)
{
    long res = raw % MOD;
    if (res < 0)
    {
        return res + MOD;
    }
    else
    {
        return res;
    }
}

void pprint2d(vector<vector<long>> arr)
{
    for (vector<long> row : arr)
    {
        cout << "[";
        for (long val : row)
        {
            cout << val << " ";
        }
        cout << "]" << endl;
    }
    cout << endl;
}

void pprint1d(vector<long> arr)
{
    for (long val : arr)
    {
        cout << val << " ";
    }
    cout << endl
         << endl;
}

vector<vector<long>> getChooseArray()
{
    vector<vector<long>> choose(N + 1, vector<long>(N + 1, 0));
    for (long i = 0; i < choose.size(); i++)
    {
        for (long j = 0; j <= i; j++)
        {
            if (!j)
            {
                choose[i][j] = 1;
            }
            else
            {
                choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD;
            }
        }
    }
    return choose;
}

vector<long> getRCountArray()
{
    vector<long> rCount = vector<long>(N + 1, 0);
    for (long i = 1; i < rCount.size(); i++)
    {
        // R(n+1) = 2R(n)*(R(n) + 2) + 1
        long prev = rCount[i - 1];
        long term1 = (2 * prev) % MOD;
        long term2 = (prev + 2) % MOD;
        long term3 = (term1 * term2) % MOD;
        rCount[i] = (term3 + 1) % MOD;
    }

    return rCount;
}

int main()
{
    auto start = high_resolution_clock::now();

    // choose[n][k] gives n choose k
    cout << "Getting choose array..." << endl;
    vector<vector<long>> choose = getChooseArray();
    cout << "done" << endl;
    // pprint2d(choose);

    // generate rCount array:
    cout << "Getting rCount array..." << endl;
    vector<long> rCount = getRCountArray();
    cout << "done" << endl;
    // pprint1d(rCount);

    cout << "Getting rBar, c, cbar arrays..." << endl;
    // create rBar array
    vector<long> rBar = vector<long>(N + 1, 0);
    // create c and cBar arrays
    vector<vector<long>> c(N + 1, vector<long>(N + 1, 0));
    vector<vector<long>> cBar(N + 1, vector<long>(N + 1, 0));
    cout << "done" << endl;

    cout << "Filling the c and cBar arrays..." << endl;
    // n is the number of labels we're computing on
    for (long n = 1; n <= N; n++)
    {
        long rowTotal = 0;
        // k is the number of connected components we're computing on
        for (long k = 2; k <= N; k++)
        {
            // if n and k are equal, there is only one possible graph,
            // and that's when each label is its
            // own connected component
            if (n == k)
            {
                c[n][k] = 1;
                cBar[n][k] = 1;
                cout << "n=" << n << ", k=" << k << ", breaking..." << endl;
            }
            else if (k > n)
            {
                break;
            }
            else
            {
                // get cBar[n][k]
                for (long j = 0; j <= n - k; j++)
                {
                    long term1 = (choose[n - 1][j] * cBar[j + 1][1]) % MOD;
                    cBar[n][k] += (term1 * cBar[n - j - 1][k - 1]) % MOD;
                    cBar[n][k] %= MOD;
                }
                // get c[n][k]
                for (long i = 1; i <= n; i++)
                {
                    long term1 = (choose[n][i] * cBar[i][k]) % MOD;
                    c[n][k] += term1;
                    c[n][k] %= MOD;
                }
            }
            cBar[n][k] = posMod(cBar[n][k]);
            c[n][k] = posMod(c[n][k]);
            rowTotal += cBar[n][k];
            rowTotal %= MOD;
        }

        // handle cBar[n][1] separately
        long numGraphsBelowNLabels = 0;
        for (long i = 0; i < n; i++)
        {
            numGraphsBelowNLabels += (choose[n][i] * rBar[i]) % MOD;
            numGraphsBelowNLabels %= MOD;
        }
        long expectedRBar = posMod(rCount[n] - numGraphsBelowNLabels);
        cBar[n][1] = posMod(expectedRBar - rowTotal);
        rBar[n] = expectedRBar;

        // handle c[n][1] separately
        for (long i = 1; i <= n; i++)
        {
            long term1 = (choose[n][i] * cBar[i][1]) % MOD;
            c[n][1] += term1;
            c[n][1] %= MOD;
        }
    }

    cout << "done" << endl;
    // pprint2d(c);
    // pprint2d(cBar);
    // pprint1d(rBar);
    // pprint1d(rCount);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << duration.count() << endl;

    long solution = c[N][K];
    if (solution < 0)
    {
        solution += MOD;
    }

    cout << "Solution is: " << solution << endl;

    return 0;
}
