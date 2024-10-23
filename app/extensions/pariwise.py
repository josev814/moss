### create kmeans process here
import os
import re
from py_classes.assignment_collector import AssignmentCollector
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ASSIGNMENTS_DIR = os.path.join(os.path.sep, 'assignments')
DEFITION_MATCH = re.compile('^([\s]+)?def\s')

"""
    Task 1:
    Implement a clustering algorithm to group similar code submissions using an ML method like k-means.
    This will help identify clusters of highly similar code for further investigation.
"""
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

        cosine_similarities = cosine_similarity(X)
        threshold = .75

        # Step 3: Clustering
        plagiarism_pairs = np.argwhere(cosine_similarities > threshold)

        print(f'Assignment: {files_to_compare[0].split("/")[-2]}')
        for i, j in plagiarism_pairs:
            if i != j and i < j:  # Avoid self-comparison and prevent i = j and j = i from being displayed twice
                print(f"{files_to_compare[i].split('/')[-1]} is similar to {files_to_compare[j].split('/')[-1]} with similarity {cosine_similarities[i, j] * 100:.2f}%")
        print("\n\n")
