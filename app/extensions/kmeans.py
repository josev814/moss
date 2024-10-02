### create kmeans process here
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

ASSIGNMENTS_DIR = os.path.join(os.path.sep, 'assignments')
DEFITION_MATCH = re.compile('^([\s]+)?def\s')

# Step 1: Read files and preprocess code
def read_files(file_paths:list) -> list:
    """
    Reads the contents of the files and returns them in a list

    :param file_paths: The files we're reading
    :type file_paths: list
    :return: list of strings where the strings are the contents of each file
    :rtype: list
    """
    code_snippets = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            code = file.read()
            # Preprocess code (remove comments, normalize, etc.)
            code_snippets.append(preprocess_code(code))
    return code_snippets

def preprocess_code(code: str) -> str:
    """
    Simple preprocessing to remove comments and normalize whitespace
    This should be improved on

    :param code: The raw contents of the file
    :type code: str
    :return: We return the string as a single line with no comments
    :rtype: str
    """
    clean_lines = []
    comment_block = False
    for line in code.splitlines():
        strip_line = line.strip()
        if len(strip_line) == 0:
            continue
        if strip_line[0] in ['#']:
            continue
        if strip_line.startswith('"""'):
            comment_block = '"""'
            if strip_line.endswith(comment_block):
                # single line comment
                comment_block = False
            continue
        if comment_block:
            # Currently in a comment block
            if (strip_line.startswith(comment_block) or strip_line.endswith(comment_block)):
                # End of comment block
                comment_block = False
            continue
        clean_lines.append(strip_line)
    return ' '.join(clean_lines)

def collect_assignments() -> list[list[str], str]:
    """
    Collects all assignment files

    :return: Returns a list of the assignments broken down by the assignment dir along with a list of strings of where to save the results to
    :rtype: list[list[str], str]
    """
    file_paths = []
    save_paths = []
    for language_dir in os.scandir(ASSIGNMENTS_DIR):
        if not language_dir.is_dir():
            continue
        for assignment_dir in os.scandir(language_dir.path):
            if not assignment_dir.is_dir():
                continue
            result_path = os.path.join(assignment_dir.path, 'kmeans_clustering')
            if not os.path.isdir(result_path):
                os.mkdir(result_path)
            files_to_compare = []
            for entry in os.scandir(assignment_dir.path):
                if entry.is_file() and entry.name.endswith('.py'):
                    files_to_compare.append(entry.path)
            if len(files_to_compare) > 0:
                file_paths.append(
                    files_to_compare
                )
                save_paths.append(
                    result_path
                )
    return file_paths, save_paths

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
    file_paths, save_paths = collect_assignments()

    for i in range(len(file_paths)):
        files_to_compare = file_paths[i]
        save_path = save_paths[i]
        f_count = len(files_to_compare)
        clusters = 4 if f_count > 4 else 2
        if (os.path.isfile(save_path, f'{clusters}.png')):
            # don't run kmeans if we've already done so against the assignment
            continue

        # Step 2: Pull the data for the assignment
        code_snippets = read_files(files_to_compare)

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

        plot_cluster(clusters, X_reduced, save_path, label_points=False)
