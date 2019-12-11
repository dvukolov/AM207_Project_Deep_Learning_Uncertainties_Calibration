import numpy as np


def calibration_error(predicted_quantiles, levels=10):
    """Compute the calibration error

    The result is sensitive to binning.
    Will use the supplied number of equally spaced quantiles.

    Args:
        predicted_quantiles: the values of the quantiles for each Y in the dataset.
            Equivalent to H(x_t)(y_t) in the paper's notation. A 1-dimensional array
            of the shape (T,), where T is the number of observations in the dataset.
        levels: the number of quantiles in the 0-1 range (default: {10})

    Returns:
        cal_error: the calibration error
    """

    # Assume equally spaced quantiles
    expected_quantiles = np.linspace(0, 1, num=levels + 1)

    # Compute the probabilities of predicted quantiles at the discrete quantile levels
    T = predicted_quantiles.shape[0]
    empirical_quantiles = (
        predicted_quantiles.reshape(1, -1) <= expected_quantiles.reshape(-1, 1)
    ).sum(axis=1) / T

    # Compute the calibration error
    cal_error = np.sum((empirical_quantiles - expected_quantiles) ** 2)

    return cal_error


def picp(predicted_quantiles, interval=0.95):
    """Calculate the Prediction Interval Coverage Probability (PICP)
    for the given interval.

    Args:
        predicted_quantiles: the values of the quantiles for each Y in the dataset.
            Equivalent to H(x_t)(y_t) in the paper's notation. A 1-dimensional array
            of the shape (T,), where T is the number of observations in the dataset.
        interval: the width of the predictive interval (default: {0.95})

    Returns:
        picp_value: the value of the Prediction Interval Coverage Probability
            for the requested interval
    """
    q_alpha = (1 - interval) / 2
    low, high = 1 - interval - q_alpha, interval + q_alpha
    picp_value = np.mean((predicted_quantiles >= low) & (predicted_quantiles <= high))
    return picp_value