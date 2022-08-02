from collections import defaultdict
import jellyfish
import numpy as np
import pandas as pd


def hamming_distance(sequence_a, sequence_b):
    """Light-weight wrapper around a fast Hamming distance calculation."""
    return jellyfish.hamming_distance(
        sequence_a,
        sequence_b
    )


def float_to_datestring(time):
    """Convert a floating point date to a date string
    """
    year = int(time)
    month = int(((time - year) * 12) + 1)
    day = 1
    return "-".join(map(str, (year, month, day)))


def timestamp_to_float(time):
    """Convert a pandas timestamp to a floating point date.
    """
    return time.year + ((time.month - 1) / 12.0)


def process_predictor_args(predictors, params=None, sds=None):
    """Returns a predictor data structure for the given lists of predictors, params,
    and standard deviations.

    When no parameters or deviations are provided, the predictors are a simple
    list. When parameters and deviations are provided, the predictor are a
    dictionary indexed by predictor name with values corresponding to each
    predictor's param and global standard deviation.

    >>> process_predictor_args(None, None, None)
    >>> process_predictor_args(['ep'])
    ['ep']
    >>> process_predictor_args(['ep'], None, None)
    ['ep']
    >>> process_predictor_args(['ep'], [1], [5])
    {'ep': [1, 5]}
    """
    if predictors is None:
        processed_predictors = None
    elif params is None or sds is None:
        processed_predictors = predictors
    else:
        merged_params = map(list, zip(params, sds))
        processed_predictors = dict(zip(predictors, merged_params))

    return processed_predictors


def make_pivots(start, stop, pivots_per_year=12, precision=2):
    """Makes an array of pivots (i.e., timepoints) between the given start and stop
    by the given pivots per year. The generated pivots are floating point values
    that are then rounded to the requested decimal precision.

    >>> list(make_pivots(2000.0, 2001.0, 5))
    [2000.0, 2000.25, 2000.5, 2000.75, 2001.0]
    """
    # Calculate number of pivots (i.e., months) in the requested interval.
    number_of_pivots = np.ceil((stop - start) * pivots_per_year)

    # Build an evenly-spaced closed interval (including the start and stop
    # points) based on the calculated number of pivots.
    return np.around(
        np.linspace(start, stop, number_of_pivots),
        precision
    )


def matthews_correlation_coefficient(tp, tn, fp, fn):
    """Return Matthews correlation coefficient for values from a confusion matrix.
    Implementation is based on the definition from wikipedia:

    https://en.wikipedia.org/wiki/Matthews_correlation_coefficient
    """
    numerator = (tp * tn) - (fp * fn)
    denominator = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denominator == 0:
        denominator = 1

    return float(numerator) / denominator


def get_matthews_correlation_coefficient_for_data_frame(freq_df, return_confusion_matrix=False):
    """Calculate Matthew's correlation coefficient from a given pandas data frame
    with columns for initial, observed, and predicted frequencies.
    """
    observed_growth = (freq_df["observed_freq"] > freq_df["initial_freq"])
    predicted_growth = (freq_df["predicted_freq"] > freq_df["initial_freq"])
    true_positives = ((observed_growth) & (predicted_growth)).sum()
    false_positives = ((~observed_growth) & (predicted_growth)).sum()

    observed_decline = (freq_df["observed_freq"] <= freq_df["initial_freq"])
    predicted_decline = (freq_df["predicted_freq"] <= freq_df["initial_freq"])
    true_negatives = ((observed_decline) & (predicted_decline)).sum()
    false_negatives = ((~observed_decline) & (predicted_decline)).sum()

    mcc = matthews_correlation_coefficient(
        true_positives,
        true_negatives,
        false_positives,
        false_negatives
    )

    if return_confusion_matrix:
        confusion_matrix = {
            "tp": true_positives,
            "tn": true_negatives,
            "fp": false_positives,
            "fn": false_negatives
        }

        return mcc, confusion_matrix
    else:
        return mcc


def sum_of_squared_errors(observed_freq, predicted_freq):
    """
    Calculates the sum of squared errors for observed and predicted frequencies.

    Args:
        observed_freq (numpy.ndarray): observed frequencies
        predicted_freq (numpy.ndarray): predicted frequencies

    Returns:
        float: sum of squared errors between observed and predicted frequencies
    """
    return np.sum((observed_freq - predicted_freq) ** 2)


def mean_absolute_error(observed_freq, predicted_freq):
    """
    Calculates the mean absolute error between observed and predicted frequencies.

    Args:
        observed_freq (numpy.ndarray): observed frequencies
        predicted_freq (numpy.ndarray): predicted frequencies

    Returns:
        float: mean absolute error between observed and predicted frequencies
    """
    return np.mean(np.abs(observed_freq - predicted_freq))


def project_clade_frequencies_by_delta_from_time(tree, model, time, delta, delta_steps_per_year=12):
    """
    Project clade frequencies from a given time to the future by a given delta.
    """
    # Calculate the steps between the projection date and delta time into the
    # future. First, find the frequency pivot that is closest to the requested
    # projection date.
    max_date = model.timepoints[np.searchsorted(model.timepoints, time)]
    future_date = max_date + delta

    # Then, calculate a fixed number of steps between that pivot and delta time
    # into the future.
    projected_pivots = np.linspace(max_date, future_date, int(delta_steps_per_year * delta))
    deltas = projected_pivots - max_date

    # Identify tip predictors and frequencies at the current time point.
    all_pred = model.predictor_arrays[max_date]
    all_freqs = model.freq_arrays[max_date]

    # For each requested delta, project current tip frequencies using the model
    # and calculate the corresponding projected clade frequencies.
    projected_clade_frequencies = defaultdict(list)

    for delta in deltas:
        # Project all tip frequencies.
        pred_freq = model.projection(model.model_params, all_pred, all_freqs, delta)

        # Normalize projected frequencies.
        pred_freq = pred_freq / pred_freq.sum()

        # Store projected frequencies by clade id.
        for i, tip in enumerate(model.tips):
            projected_clade_frequencies[tip.name].append(pred_freq[i])

        # Calculate projected frequencies for internal nodes and store by clade it.
        for node in tree.find_clades(order="postorder"):
            if not node.is_terminal():
                projected_clade_frequencies[node.name].append(pred_freq[node.tips].sum())

    projected_frequencies = {
        "params": {
            "max_date": max_date
        },
        "data": {
            "pivots": projected_pivots.tolist(),
            "frequencies": projected_clade_frequencies
        }
    }

    return projected_frequencies


def get_train_validate_timepoints(timepoints, delta_time, training_window):
    """Return all possible train-validate timepoints from the given complete list of
    timepoints, a delta time to project forward by, and the required number of
    timepoints to include in each training window.

    Parameters
    ----------
    timepoints : list
        Date/time strings to use for model training and validation

    delta_time : int
        Number of months into the future that the model will project

    training_window : int
        Number of years to include in each training window

    Returns
    -------
    list
        List of dictionaries containing all possible train-validate timepoints indexed by "train" and "validate" keys
    """
    # Convert list of date/time strings into pandas datetimes.
    timepoints = pd.to_datetime(timepoints)

    # Convert delta time and training window to pandas offsets.
    delta_time = pd.DateOffset(months=delta_time)
    training_window = pd.DateOffset(years=training_window)

    # Filter timepoints to those with enough future years to train and project
    # from. This means timepoints must not extend beyond the last training
    # timepoint plus its delta time in the future and the delta time in the
    # future for the validation interval.
    #
    # If the timepoints range from October 2005 to October 2015, the training
    # window is 4 years, and the delta time is 1 year, then the last validation
    # timepoint is October 2014 and the last training timepoint is October
    # 2013. This allows the model to train from October 2013 to October 2014 and
    # then validate from October 2014 to 2015. Assuming there is enough data in
    # the tree up to October 2005, the earliest point we can project from is
    # then October 2008 such that the previous 4 years are included in that
    # projection.
    is_valid_projection_timepoint = (timepoints + training_window + delta_time + delta_time) <= timepoints[-1]
    projection_timepoints = timepoints[is_valid_projection_timepoint].copy()

    # Split valid timepoint index values into all possible train/test sets.
    train_validate_timepoints = []
    for start_timepoint in projection_timepoints:
        end_timepoint = start_timepoint + training_window
        train_timepoints = timepoints[
            (timepoints >= start_timepoint) &
            (timepoints <= end_timepoint)
        ]
        validate_timepoint = train_timepoints[-1] + delta_time

        # Store train/validate timepoints as datetime strings to enable
        # downstream use by other tools.
        train_validate_timepoints.append({
            "train": train_timepoints.strftime("%Y-%m-%d").tolist(),
            "validate": validate_timepoint.strftime("%Y-%m-%d")
        })

    return train_validate_timepoints


def cross_immunity_cost(d_ep, d_init):
    """Return the cross-immunity cost corresponding to the given epitope distance
    between two amino acid sequences and a predetermined scaling parameter that
    controls the time period across which cross-immunity decays.
    """
    return np.exp(-d_ep / float(d_init))
