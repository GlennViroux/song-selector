"""Solver for the Subset-Sum-Problem"""

import random
import time
from pathlib import Path
from typing import List

from common.decorators import log_exec_time
from common.logger import StuBruLogger
from core import SongInfo


class SubSumSetSolver:
    """
    Class responsible for solving the subset-sum problem (SSP) following the fast approximation algorithm proposed in:

    Bartosz Przydatek,
    A Fast Approximation Algorithm for the Subset-Sum Problem,
    International Transactions in Operational Research,
    July 2002, Pages 437-459
    """

    Threshold = 2
    MaxNumberOfIterations = 5
    Logger = StuBruLogger()

    def __init__(self, sum_time_seconds: float, available_songs: List[SongInfo]):
        self.sum_time_seconds = sum_time_seconds
        self.available_songs = available_songs
        self.current_solution_vector = []  # type: List[SongInfo]
        self.best_solution = []  # type: List[SongInfo]
        self.worst_solution = []  # type: List[SongInfo]
        self.Logger.info(f"Initialized SubSetSumSolver with {sum_time_seconds:.2f}sec and {len(available_songs)} songs")

    def _check_possible_song(self, new_song: SongInfo) -> bool:
        """
        Check if a new song can be added to the current solution vector, without exceeding the total sum constraint.
        """
        return sum([song.duration for song in self.current_solution_vector]) + new_song.duration < self.sum_time_seconds

    def _random_greedy_phase(self):
        """
        Random greedy phase, initializing a solution vector by randomly creating a maximal and permissible
        solution vector.
        """

        unordered_songs = self.available_songs.copy()
        random.shuffle(unordered_songs)

        for new_song in unordered_songs:
            if self._check_possible_song(new_song):
                self.current_solution_vector.append(new_song)

    def _local_improvement_phase(self):
        """Local improvement phase, trying to improve the solution by looking to replace individual elements."""

        for index, current_song in enumerate(self.current_solution_vector):

            if self._solution_error(self.current_solution_vector) < self.Threshold:
                self.Logger.info(f"Breaking improvement phase as threshold is reached")
                break

            local_improvement = None  # type: SongInfo | None
            for possible_replacement in self.available_songs:
                if possible_replacement in self.current_solution_vector:
                    continue

                if not self._check_possible_song(possible_replacement):
                    continue

                if local_improvement is None or possible_replacement.duration > local_improvement.duration:
                    local_improvement = possible_replacement

            if local_improvement:
                self.current_solution_vector[index] = local_improvement

    def _solution_error(self, solution: List[SongInfo]):
        """Calculate the error of a specific solution set"""
        return abs(self.sum_time_seconds - sum([song.duration for song in solution]))

    def _update_solutions(self) -> None:
        """Update the best and worst solution of the solving process."""

        if not self.best_solution or not self.worst_solution:
            if not self.best_solution:
                self.best_solution = self.current_solution_vector

            if not self.worst_solution:
                self.worst_solution = self.current_solution_vector

            return None

        current_error = self._solution_error(self.current_solution_vector)
        if current_error < self._solution_error(self.best_solution):
            self.best_solution = self.current_solution_vector

        if current_error > self._solution_error(self.worst_solution):
            self.worst_solution = self.current_solution_vector

        return None

    def _check_threshold(self) -> bool:
        if self._solution_error(self.current_solution_vector) <= self.Threshold:
            return True

        return False

    def _write_stats(self, duration: float, best_error: float, worst_error: float, iterations: int):
        with Path("subset_sum_stats.csv").open("a") as fp:
            fp.write(f"{best_error:.2f},{worst_error:.2f},{duration:.2f},{iterations},{self.sum_time_seconds}\n")

    @log_exec_time("Solving SubSetProblem took ")
    def solve(self) -> List[SongInfo]:
        start = time.perf_counter()
        iteration = 0
        for i in range(self.MaxNumberOfIterations):
            iteration = i
            self.Logger.debug(f"Starting iteration {i}")
            self.current_solution_vector = []
            self._random_greedy_phase()
            self._local_improvement_phase()
            self._update_solutions()

            if self._check_threshold():
                self.Logger.info(f"Threshold reached in iteration {i}")
                break

        duration = time.perf_counter() - start
        best_error = self._solution_error(self.best_solution)
        worst_error = self._solution_error(self.worst_solution)
        self._write_stats(duration, best_error, worst_error, iteration)
        self.Logger.info(f"Approximate optimal solution found with offset {best_error:.2f}sec")
        return self.best_solution
