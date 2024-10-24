import os
import re
from py_classes.assignment_collector import AssignmentCollector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt

ASSIGNMENTS_DIR = os.path.join(os.path.sep, 'assignments')
DEFITION_MATCH = re.compile('^([\s]+)?def\s')

ac = AssignmentCollector(ASSIGNMENTS_DIR)
if __name__ == '__main__':
    
    file_paths, save_paths = ac.collect_assignments()

    for i in range(len(file_paths)):
        files_to_compare = file_paths[i]
        f_count = len(files_to_compare)
        
        # Step 2: Pull the data for the assignment
        code_snippets = ac.read_files(files_to_compare)

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(code_snippets)

        pwd = pairwise_distances(X, X, metric='euclidean')

        plt.figure(figsize=(8, 6))
        for idx, (x, y) in enumerate(zip(pwd[:, 0], pwd[:, 1])):
            plt.scatter(x, y, label=os.path.basename(files_to_compare[idx].split('-')[-1]), alpha=0.5)
        plt.title('Scatter Plot with Pairwise Distances')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), fontsize='small', title="Files")        

        plt.show()

        plt.savefig(
            os.path.join('/assignments/python/', f'{i}.png'),
            dpi=300,
            bbox_inches='tight'
        )

        # Close the plot
        plt.close()
