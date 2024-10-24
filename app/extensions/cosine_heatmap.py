import os
import re
from py_classes.assignment_collector import AssignmentCollector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sb
import matplotlib.pyplot as plt

ASSIGNMENTS_DIR = os.path.join(os.path.sep, 'assignments')
DEFITION_MATCH = re.compile('^([\s]+)?def\s')

ac = AssignmentCollector(ASSIGNMENTS_DIR, 'cosine_heatmap')
if __name__ == '__main__':
    
    file_paths, save_paths = ac.collect_assignments()

    for i in range(len(file_paths)):
        files_to_compare = file_paths[i]
        save_path = save_paths[i]
        f_count = len(files_to_compare)
        
        # Step 2: Pull the data for the assignment
        code_snippets = ac.read_files(files_to_compare)

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(code_snippets)

        cosine_similarities = cosine_similarity(X)

        print(f'Assignment: {files_to_compare[0].split("/")[-2]}')
        plt.figure(figsize=(8, 6))
        sb.heatmap(cosine_similarities, annot=False, fmt=".2f", cmap='jet', 
            xticklabels=[f'{files_to_compare[idx].split("-")[-1]}' for idx in range(len(files_to_compare))],
            yticklabels=[f'{files_to_compare[idx].split("-")[-1]}' for idx in range(len(files_to_compare))]
        )

        plt.title('Similarity Heatmap')
        plt.show()

        plt.savefig(
            os.path.join(save_path, f'assignment_{i}_heatmap.png'),
            dpi=300,
            bbox_inches='tight'
        )

        # Close the plot
        plt.close()