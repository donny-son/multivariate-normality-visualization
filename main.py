import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
import termplotlib as tpl

class ChiQQ:
    """Object for creating Chisquare QQ plots.

    params
    ------
    src: input matrix of shape (n:int, p:int) where n is the sample size and p is the number of dependent variables
        np.ndarray

    methods
    -------
    _get_mean_vector: gets the mean vector along the features
        np.array

    _get_cov_mat: gets the covariance matrix in (p by p).
        np.array

    generalized_distance_squared: gets list of squared distance by dimension n.
        list

    _get_qq_tuples: gets the list of tuples of the qq pair for the chisquare distribution with df=p
        list

    draw: draws the plot by using matplotlib
    """
    def __init__(self, src) -> None:
        assert isinstance(src, np.ndarray)
        self.src = src
        self.n, self.p = self.src.shape
        self.mean_vector = self._get_mean_vector()
        self.cov_matrix = self._get_cov_mat()

    def _get_mean_vector(self) -> np.array:
        return (np.mean(self.src, axis=0))

    def _get_cov_mat(self) -> np.array:
        result = np.cov(self.src.transpose())
        assert result.shape == (self.p, self.p)
        return result

    def generalized_distance_squared(self) -> list:
        result = []
        inv_cov = np.linalg.inv(self.cov_matrix)
        for row in self.src:
            diff = row - self.mean_vector
            result.append(np.matmul(np.matmul(diff, inv_cov), diff))
        assert len(result) == self.n
        return result

    def _get_qq_tuples(self) -> list:
        result = []
        sorted_general_distance = sorted(self.generalized_distance_squared())
        for i, x in enumerate(sorted_general_distance):
            x_probability_value = (i+1 - 0.5) / self.n
            q_value = chi2.ppf(x_probability_value, self.p)
            result.append(
                (q_value, x)
            )
        return result

    def draw(self, terminal=False):
        qq_tuples = self._get_qq_tuples()
        x = [x for x, _ in qq_tuples]
        y = [y for _, y in qq_tuples]
        if terminal:
            fig = tpl.figure()
            fig.plot(x, y, width=60, height=20)
            fig.show()
        else:
            plt.scatter(x, y)


if __name__=="__main__":
    a = list(np.random.uniform(-1, 1, 100))
    b = list(np.random.normal(-1, 4, 100))
    c = list(np.random.chisquare(10, 100))
    data = np.array([a, b, c]).transpose()
    cq = ChiQQ(data)
    cq.draw(terminal=True)
