from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random
from typing import Any, DefaultDict, Protocol
import math

import numpy as np
import plotly.express as px  # type: ignore
from plotly.offline import plot  # type: ignore
import pandas as pd


class DistanceStrategy(Protocol):
    def calculate(self, a: tuple[float, float], b: tuple[float, float]) -> float: ...


class EuclideanStrategy(DistanceStrategy):
    def calculate(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        distance = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        return distance


class ManhattanStrategy(DistanceStrategy):
    def calculate(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        distance = abs(a[0] - b[0]) + abs(a[1] - b[1])

        return distance


@dataclass
class KMeans:
    k: int
    distance_strategy: DistanceStrategy = EuclideanStrategy()

    def calculate_centroid(self, cluster: list[tuple[float, float]]) -> tuple[float, float]:
        x_sum = 0.0
        y_sum = 0.0

        for point in cluster:
            x_sum += point[0]
            y_sum += point[1]

        x_mean = x_sum / len(cluster)
        y_mean = y_sum / len(cluster)
        centroid = (x_mean, y_mean)

        return centroid

    def fit(self, points: list[tuple[float, float]]) -> dict[int, list]:
        centroids = [(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(self.k)]
        converged = False

        while not converged:
            clusters: DefaultDict[int, list[tuple[float, float]]] = defaultdict(list, {i: [] for i in range(self.k)})

            for point in points:
                centroid_distances = [self.distance_strategy.calculate(point, centroid) for centroid in centroids]
                cluster_assignment = centroid_distances.index(min(centroid_distances))
                clusters[cluster_assignment].append(point)

            new_centroids = [self.calculate_centroid(cluster) for cluster in clusters.values() if len(cluster) != 0]
            converged = new_centroids == centroids
            centroids = new_centroids

            if converged:
                break
        return clusters


def plot_clusters(clusters, filename: str):
    data: dict[str, list[Any]] = {"x": [], "y": [], "label": []}

    for label, points in clusters.items():
        for point in points:
            data["x"].append(point[0])
            data["y"].append(point[1])
            data["label"].append(label)

    df = pd.DataFrame(data)
    custom_colors = px.colors.qualitative.Plotly
    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="label",
        title="Cluster Visualization",
        labels={"label": "Cluster"},
        color_discrete_sequence=custom_colors,
    )

    plot(fig, filename=filename, auto_open=False)
    print(f"Plot saved as {filename}. Open it in your browser.")


def main():
    points1 = np.random.multivariate_normal([0, 0], np.eye(2), 33)
    points2 = np.random.multivariate_normal([1, 1], np.eye(2), 33)
    points3 = np.random.multivariate_normal([-1, -1], np.eye(2), 33)
    points = points1.tolist() + points2.tolist() + points3.tolist()

    k = 3
    model = KMeans(k, distance_strategy=EuclideanStrategy())
    euclidean_clusters = model.fit(points)

    filename = "cluster_plot_euclidean.html"
    plot_clusters(euclidean_clusters, filename)

    model = KMeans(k, distance_strategy=ManhattanStrategy())
    manhattan_clusters = model.fit(points)

    filename = "cluster_plot_manhattan.html"
    plot_clusters(manhattan_clusters, filename)


if __name__ == "__main__":
    main()
