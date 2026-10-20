"""Everything that touches Media/score.csv lives here."""
import csv
import os
import warnings
from datetime import date

import numpy as np

SCORE_FILE = os.path.join("Media", "score.csv")
HEADER = ["date", "wpm", "seconds"]


def load_scores(path=SCORE_FILE):
    """Return (scores, times) as 1-D arrays.

    Works with a missing file, a header-only file and a single-row file.
    If there is no data yet, a single 0 is returned so callers never see an
    empty array.
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = np.loadtxt(path, skiprows=1, usecols=(1, 2),
                              delimiter=";", ndmin=2)
    except (OSError, ValueError):
        data = np.empty((0, 2))
    if data.size == 0:
        return np.zeros(1), np.zeros(1)
    return data[:, 0], data[:, 1]


def get_high_score():
    scores, _ = load_scores()
    return int(np.max(scores))


def format_total_time(seconds):
    if seconds > 3600:
        return "You have spent " + str(round(seconds / 3600, 2)) + " hours on the game."
    if seconds > 60:
        return "You have spent " + str(round(seconds / 60, 2)) + " minutes on the game."
    return "You have spent " + str(round(seconds)) + " seconds on the game."


def save_score(wpm, seconds):
    """Append one game to the CSV (writing the header if the file is new)."""
    wpm = int(wpm)
    if wpm == 0:
        return
    new_file = not os.path.exists(SCORE_FILE) or os.path.getsize(SCORE_FILE) == 0
    with open(SCORE_FILE, "a", newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        if new_file:
            writer.writerow(HEADER)
        writer.writerow([date.today().isoformat(), wpm, int(seconds)])
