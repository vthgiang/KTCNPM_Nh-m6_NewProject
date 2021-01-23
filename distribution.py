from constant import *
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Distribution:
    # make sure that sum of pdf's elements is 1
    def __init__(self, pdf):
        self.pdf = pdf.copy()
        self.pdf /= np.sum(self.pdf)
        self.mu = np.sum(pdf * np.arange(len(pdf)))
        self.sigma = np.sqrt(np.sum((pdf * (np.arange(len(pdf)) - self.mu) ** 2)))

    # use for initiation only
    @staticmethod
    def eval(mu, sigma, x):
        return 1.0 / (sigma * np.sqrt(2.0 * np.pi)) * np.exp(-(x - mu)**2 / (2.0 * sigma**2))

    @classmethod
    def from_mu_sigma(cls, mu, sigma, sz=DISTRIBUTION_MAX_SIZE):
        pdf = np.zeros(sz)
        for i in range(sz):
            pdf[i] = cls.eval(mu, sigma, i)
        pdf /= np.sum(pdf)
        return cls(pdf)

    def add(self, other):
        pdf = np.convolve(self.pdf, other.pdf)
        return Distribution(pdf)

    def max(self, other):
        cdf1 = self.pdf.copy()
        cdf2 = other.pdf.copy()
        sz = max(len(cdf1), len(cdf2))
        cdf1.resize(sz)
        cdf2.resize(sz)
        for i in range(1, sz):
            cdf1[i] += cdf1[i - 1]
            cdf2[i] += cdf2[i - 1]
        pdf = cdf1 * cdf2
        for i in range(sz - 1, 0, -1):
            pdf[i] -= pdf[i - 1]
        return Distribution(pdf)

    def div(self, k):
        pdf = [0.0] * ((len(self.pdf) + k - 1) // k)
        for u in range(len(self.pdf)):
            pdf[u // k] += self.pdf[u]
        return Distribution(pdf)

# a = Distribution.from_mu_sigma(10, 5)
# # d = a.div(2)
# b = Distribution.from_mu_sigma(10, 2)
# c = Distribution.add(a, b)
# plt.plot(c.pdf, label = "c")
# plt.plot(a.pdf, label = "a")
# # plt.plot(d.pdf, label = "d")
# plt.plot(b.pdf, label = "b")
# plt.legend()
# plt.show()