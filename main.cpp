#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <fstream>
#include <cassert>
#include <algorithm>
#include <iomanip>
#include <numeric>

const double INF = 1e18;
const int GROUP_LIMIT = 3;
const int NUM_TEAM = 4;
const int DIST_SIZE = 30;

template<class T> bool minimize(T &a, const T &b) {
    if (b < a) {
        a = b;
        return true;
    }
    return false;
}


using Vector = std::vector<double>;
class Distribution : public Vector {
    using Vector::Vector;

  public:
    double expectation = -1;

    double mean() {
        if (expectation < 0) {
            expectation = 0;
            for (int i = 0; i < this->size(); ++i) {
                expectation += this->at(i) * i; 
            }
        } 
        return expectation;
    }
};

Distribution normal(double mean, double sigma, int size) {
    static const double PI = acos(-1);
    static const double FACTOR = 1.0 / sqrt(PI * 2);

    Distribution result(size);
    double sum = 0;
    for (int i = 0; i < size; ++i) {
        double nv = (i - mean) / sigma;
        result[i] = exp(-0.5 * nv * nv) * FACTOR / sigma;
        sum += result[i];
    }
    for (int i = 0; i < size; ++i) {
        result[i] /= sum;
    }

    return result;
}

Vector cdf(const Distribution &f) {
    Vector p = f;
    for (int i = 1; i < p.size(); ++i) {
        p[i] += p[i - 1];
    } 
    return p;
}

Distribution operator + (const Distribution &a, const Distribution &b) {
    Distribution result(a.size() + b.size() - 1, 0);
    for (int i = 0; i < a.size(); ++i) {
        for (int j = 0; j < b.size(); ++j) {
            result[i + j] += a[i] * b[j];
        }
    }
    return result;
}

Distribution operator ^ (const Distribution &a, const Distribution &b) {
    Distribution result(std::max(a.size(), b.size()));
    Vector pa = cdf(a); 
    Vector pb = cdf(b); 
    for (int i = pa.size(); i < result.size(); ++i) {
        pa.push_back(pa.back());
    }
    for (int i = pb.size(); i < result.size(); ++i) {
        pb.push_back(pb.back());
    }
    for (int i = 0; i < result.size(); ++i) {
        // std::cerr << i << ' ' << pa[i] << ' ' << pb[i] << ' ' << result[i] << std::endl;
        result[i] = pa[i] * pb[i];
    }
    for (int i = (int) result.size() - 1; i > 0; --i) {
        result[i] -= result[i - 1];
    }
    return result;
}

Distribution operator / (const Distribution &a, double k) {
    Distribution result(a.size() / k + 1, 0);
    for (int i = 0; i < a.size(); ++i) {
        assert(i / k < result.size());
        result[std::max(1, int(i/ k))] += a[i];
    }
    return result;
}

struct Edge {
    int v;
    int w;

    Edge(int v, int w): v(v), w(w) {}
};

std::vector< std::vector<Edge> > to, into;
std::vector< Distribution > node_dist;
int n;

void read_dist(const char* prefix) {
    node_dist.resize(n);
    for (int i = 1; i <= n; ++i) {
        std::string distfile = std::string(prefix) + "dist" + std::to_string(i) + ".txt";
        std::cerr << "read_dist " << distfile << std::endl;
        std::ifstream fin(distfile);
        int x; double f;
        Distribution &dist = node_dist[i - 1];
        while (fin >> x >> f) {
            while (dist.size() <= x) dist.push_back(0);
            dist[x] = f;
        } 
    }
    std::cerr << "done read_dist" << std::endl;
}

void read_relations(const char* inputfile) {
    std::ifstream fin(inputfile);
    int u, v, w;
    while (fin >> u >> v >> w) {
        --u; --v; // zero indexed
        while (to.size() <= u) to.push_back(std::vector<Edge>());        
        while (into.size() <= u) into.push_back(std::vector<Edge>());        
        while (to.size() <= v) to.push_back(std::vector<Edge>());        
        while (into.size() <= v) into.push_back(std::vector<Edge>());        
        to[u].push_back(Edge(v, w));
        into[v].push_back(Edge(u, w));
    }
    n = to.size();
    std::cerr << "done read_relations " << n << std::endl;
}

std::vector< std::pair< std::vector<int>, Distribution> >  solve() {
    std::vector<Distribution> dp(1 << n, {1});
    std::vector<int> trace(1 << n);
    std::vector<Distribution> group_dist(1 << n);
/*
    std::vector<Distribution> group_cost(1 << n, normal(0, 0, 1));

    for (int mask = 0; mask < (1 << n); ++mask) {
        for (int u = 0; u < n; ++u) if (mask >> u & 1) {
            for (auto &e : to[u]) {
                int v = e.v;
                if (mask >> v & 1) {
                    group_cost[mask] = group_cost[mask] ^ normal(e.w, 0.1, e.w * 2);
                }
            }
        }
    } 
*/

    dp[0].expectation = 0;
    for (int mask = 1; mask < (1 << n); ++mask) {
        dp[mask].expectation = INF;
        for (int group_mask = mask; group_mask > 0; group_mask = (group_mask - 1) & mask) {
            if (__builtin_popcount(group_mask) > GROUP_LIMIT) {
                continue;
            }
            Distribution cost = {1};
            for (int u = 0; u < n; ++u) if (group_mask >> u & 1) {
                double intra_cost = 0;
                for (auto e : into[u]) {
                    int v = e.v;
                    if (!((mask ^ group_mask) >> v & 1)) {
                        intra_cost += e.w;
                    }
                }
                Distribution cur = node_dist[u] + normal(intra_cost, 0.1, DIST_SIZE);
                cost = cost ^ cur;
//                if (mask == 8)
//                  std::cerr << "intra_cost " << intra_cost << ' ' << node_dist[u].mean() << ' ' << cur.mean() << ' ' << cost.mean() << std::endl; 
            }
            cost = cost / NUM_TEAM;
            Distribution cand = dp[mask ^ group_mask] + cost; 
//            if (mask == 8)
//                std::cerr << "cand " << cand.mean() << ' ' << dp[mask].mean() << std::endl;
            if (cand.mean() < dp[mask].mean()) {
                dp[mask] = cand;
//                 std::cerr << "minimized " << dp[mask].mean() << std::endl;
                group_dist[mask] = cost;
                trace[mask] = group_mask;
            }
        }
//        if (mask == 8) {
//            std::cerr << "dp " << mask << ' ' << dp[mask].mean() << std::endl;                     
//        }
    }
    std::cerr << "done DP\n";

    std::vector< std::pair<std::vector<int>, Distribution> > result;
    for (int mask = (1 << n) - 1; mask > 0; mask ^= trace[mask]) {
//        std::cerr << mask << ' ' << trace[mask] << std::endl;
        assert(trace[mask] != 0);
        std::vector<int> group;
        for (int i = 0; i < n; ++i) {
            if (trace[mask] >> i & 1) {
                group.push_back(i + 1);
            }
        }
        result.push_back({group, group_dist[mask]});
    }

    std::reverse(result.begin(), result.end());
    return result;
}

int main(int argc, char* argv[]) {
    read_relations(argv[1]); 
    read_dist("out/");
    std::vector< std::pair< std::vector<int>, Distribution> > result = solve();

    Distribution disttill = {1};
    for (const auto &g : result) {
        for (int v : g.first) {
            std::cout << v << ' ';
        }
        std::cout << std::endl;
        for (double v : g.second) {
            std::cout << std::setprecision(6) << std::fixed << v << ' ';
        }
        std::cout << std::endl;
        disttill = disttill + g.second;
        for (double v : disttill) {
            std::cout << std::setprecision(6) << std::fixed << v << ' ';
        }

        std::cout << std::endl;
        std::cerr << std::accumulate(g.second.begin(), g.second.end(), 0.0) << std::endl;
    }
    std::cerr << "Mean = " << disttill.mean() << std::endl;
    return 0;
}

