#include <iostream>
#include <cmath>
#include <vector>
using namespace std;
using namespace std::chrono;

const long N = pow(10, 4);
const long K = 10;
// const long N = 100;
// const long K = 10;

// const long N = 10;
// const long K = 2;

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

vector<long> getRBarArray(vector<long> rCount, vector<vector<long>> choose)
{
    vector<long> rBar = vector<long>(N + 1, 0);
    rBar[1] = 1;
    for (int n = 2; n <= N; n++)
    {
        rBar[n] += rCount[n];
        for (int i = 1; i < n; i++)
        {
            rBar[n] -= (choose[n][i] * rBar[i]) % MOD;
            rBar[n] = posMod(rBar[n]);
            rBar[n] %= MOD;
        }
    }
    return rBar;
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

    // create rBar and cBar arrays
    cout << "Getting rBar, cbar arrays..." << endl;
    vector<long> rBar = getRBarArray(rCount, choose);
    vector<vector<long>> cBar(N + 1, vector<long>(N + 1, 0));
    cout << "done" << endl;

    cout << "Filling the cBar array..." << endl;
    // n is the number of labels we're computing on
    for (long n = 1; n <= N; n++)
    {
        if (!(n % 100))
        {
            cout << "n=" << n << endl;
        }
        // k is the number of connected components we're computing on
        for (long k = 2; k <= K; k++)
        {
            // if n and k are equal, there is only one possible graph,
            // and that's when each label is its
            // own connected component
            if (n == k)
            {
                // c[n][k] = 1;
                cBar[n][k] = 1;
                if (!(n % 100))
                {
                    cout << "n=" << n << ", k=" << k << ", breaking..." << endl;
                }
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
            }
            cBar[n][k] = posMod(cBar[n][k]);
        }

        // handle cBar[n][1] separately
        cBar[n][1] = rBar[n];
        // subtract counts of graphs with exactly n labels AND > 1 connected components
        for (int i = 0; i < n; i++)
        {
            long term1 = (choose[n - 1][i] * cBar[i + 1][1]) % MOD;
            cBar[n][1] -= (term1 * rBar[n - i - 1]) % MOD;
            cBar[n][1] = posMod(cBar[n][1]);
        }
    }
    cout << "done" << endl;
    // pprint2d(cBar);
    // pprint1d(rBar);
    // pprint1d(rCount);

    // long solution = c[N][K];
    long solution = 0;
    for (int i = 1; i <= N; i++)
    {
        long term1 = (choose[N][i] * cBar[i][K]) % MOD;
        solution += term1;
        solution %= MOD;
    }
    if (solution < 0)
    {
        solution += MOD;
    }

    cout << "Solution is: " << solution << endl;

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << duration.count() << endl;

    return 0;
}
