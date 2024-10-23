### create kmeans process here
import os
import re
from py_classes.assignment_collector import AssignmentCollector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

ASSIGNMENTS_DIR = os.path.join(os.path.sep, 'assignments')
DEFITION_MATCH = re.compile('^([\s]+)?def\s')

ac = AssignmentCollector(ASSIGNMENTS_DIR, 'kmeans_clustering')

def plot_cluster(clusters: int, x_reduced: PCA, save_path:str, label_points=True) -> None:
    """
    Task 5:
        If we were to create a graph that shows each submitted code
        as a point with clusters plotted in the XY plane,
        what are your thoughts and ideas on how we should approach this visualization?
        Any suggestions on useful metrics or dimensions to represent?

    :param clusters: The number of clusters we're using
    :type clusters: int
    :param x_reduced: the pca object
    :type x_reduced: PCA
    :param save_path: Where we're saving the file
    :type save_path: str
    :param label_points: if we're labeling the files on the plot, defaults to True
    :type label_points: bool, optional
    """
    # Step 5: Plotting the clusters
    plt.figure(figsize=(8, 6))
    for i in range(clusters):
        plt.scatter(
            x_reduced[kmeans.labels_ == i, 0],
            x_reduced[kmeans.labels_ == i, 1],
            label=f'Cluster {i}'
        )

    if label_points:
        # Annotate points with file names
        for idx, (x, y) in enumerate(X_reduced):
            plt.annotate(
                files_to_compare[idx].split('/')[-1].split('-')[-1],
                (x, y),
                fontsize=9
            )

    plt.title('KMeans Clustering of Code Snippets')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    plt.show()

    # Save the plot to a file
    plt.savefig(
        os.path.join(save_path, f'{clusters}.png'),
        dpi=300,
        bbox_inches='tight'
    )

    # Close the plot
    plt.close()


"""
    Task 1:
    Implement a clustering algorithm to group similar code submissions using an ML method like k-means.
    This will help identify clusters of highly similar code for further investigation.
"""

if __name__ == '__main__':
    file_paths, save_paths = ac.collect_assignments()

    for i in range(len(file_paths)):
        files_to_compare = file_paths[i]
        save_path = save_paths[i]
        f_count = len(files_to_compare)
        clusters = 4 if f_count > 4 else 2
        if (os.path.isfile(os.path.join(save_path, f'{clusters}.png'))):
            # don't run kmeans if we've already done so against the assignment
            continue

        # Step 2: Pull the data for the assignment
        code_snippets = ac.read_files(files_to_compare)

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(code_snippets)

        # Step 3: Clustering
        kmeans = KMeans(
            n_clusters = clusters,
            max_iter = 100,
            n_init = 5
        )
        kmeans.fit(X)

        # Step 4: Dimensionality Reduction for Visualization
        pca = PCA(n_components=2) # was 2
        X_reduced = pca.fit_transform(X.toarray())

        plot_cluster(clusters, X_reduced, save_path, label_points=True)
