import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from typing import Tuple, List
import os

def compare_sentence_vectors(
    file1_path: str,
    file2_path: str,
    output_plot: str = 'vector_similarity_vs_mistakes.png'
) -> Tuple[pd.DataFrame, float]:
    """
    Compare sentences from two CSV files using cosine similarity.
    Calculates average similarity for each mistake count group (10 sentences per group).

    Args:
        file1_path: Path to first CSV file (English.csv - original with mistakes)
        file2_path: Path to second CSV file (English_final.csv - after translation cycle)
        output_plot: Path to save the output plot showing averaged similarities
    """
    print("=" * 80)
    print("Sentence Vector Comparison")
    print("=" * 80)

    # Load CSV files
    print(f"\nLoading {file1_path}...")
    df1 = pd.read_csv(file1_path)

    print(f"Loading {file2_path}...")
    df2 = pd.read_csv(file2_path)

    # Sort by Index to ensure proper alignment
    df1 = df1.sort_values(by='Index').reset_index(drop=True)
    df2 = df2.sort_values(by='Index').reset_index(drop=True)

    # Remove empty rows
    df1 = df1[df1['text'].notna() & (df1['text'].str.strip() != '')]
    df2 = df2[df2['text'].notna() & (df2['text'].str.strip() != '')]

    print(f"File 1: {len(df1)} sentences")
    print(f"File 2: {len(df2)} sentences")

    if len(df1) != len(df2):
        print(f"Warning: Files have different number of sentences!")

    # Extract data
    sentences1 = df1['text'].tolist()
    sentences2 = df2['text'].tolist()
    mistakes = df1['mistakes'].tolist()
    indices = df1['Index'].tolist()

    # Load sentence transformer model and convert to vectors
    print("\nLoading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Converting sentences to vectors...")
    print("  Processing file 1...")
    vectors1 = model.encode(sentences1, show_progress_bar=True)

    print("  Processing file 2...")
    vectors2 = model.encode(sentences2, show_progress_bar=True)

    print(f"\nVector dimensions: {vectors1.shape[1]}")

    # Calculate cosine similarity between corresponding vectors
    print("\nCalculating cosine similarities...")
    similarities = []
    for i in range(len(vectors1)):
        # Calculate cosine similarity directly
        sim = cosine_similarity([vectors1[i]], [vectors2[i]])[0][0]
        similarities.append(sim)

    # Display results
    print("\n" + "=" * 80)
    print("Results")
    print("=" * 80)
    print(f"\n{'Index':<8} {'Mistakes':<12} {'Similarity':<12}")
    print("-" * 80)
    for idx, m, s in zip(indices, mistakes, similarities):
        print(f"{idx:<8} {m:<12} {s:<12.4f}")

    print(f"\nSimilarity Statistics:")
    print(f"  Average similarity: {np.mean(similarities):.4f}")
    print(f"  Minimum similarity: {np.min(similarities):.4f} (Index {indices[np.argmin(similarities)]}, {mistakes[np.argmin(similarities)]} mistakes)")
    print(f"  Maximum similarity: {np.max(similarities):.4f} (Index {indices[np.argmax(similarities)]}, {mistakes[np.argmax(similarities)]} mistakes)")

    # Save results to CSV
    results_df = pd.DataFrame({
        'Index': indices,
        'Mistakes': mistakes,
        'Cosine_Similarity': similarities,
        'Original_Sentence': sentences1,
        'Final_Sentence': sentences2
    })
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in globals() else os.getcwd()
    csv_output = os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv')
    results_df.to_csv(csv_output, index=False)
    print(f"\nResults saved to: {csv_output}")

    # Calculate average similarities per mistake count
    print("\n" + "=" * 80)
    print("Average Similarities by Mistake Count")
    print("=" * 80)

    # Group by mistake count and calculate averages
    avg_similarities_by_mistakes = results_df.groupby('Mistakes')['Cosine_Similarity'].agg(['mean', 'std', 'count']).reset_index()
    avg_similarities_by_mistakes.columns = ['Mistakes', 'Avg_Similarity', 'Std_Dev', 'Count']

    print(f"\n{'Mistakes':<12} {'Avg Similarity':<18} {'Std Dev':<15} {'Count':<10}")
    print("-" * 80)
    for _, row in avg_similarities_by_mistakes.iterrows():
        print(f"{int(row['Mistakes']):<12} {row['Avg_Similarity']:<18.4f} {row['Std_Dev']:<15.4f} {int(row['Count']):<10}")

    # Save averaged results to CSV
    avg_csv_output = os.path.join(project_root, 'data', 'output', 'vector_similarity_averaged.csv')
    avg_similarities_by_mistakes.to_csv(avg_csv_output, index=False)
    print(f"\nAveraged results saved to: {avg_csv_output}")

    # Create visualization
    print("\n" + "=" * 80)
    print("Creating Graph")
    print("=" * 80)

    plt.figure(figsize=(14, 9))

    # Extract averaged data for plotting
    avg_mistakes = avg_similarities_by_mistakes['Mistakes'].values
    avg_sims = avg_similarities_by_mistakes['Avg_Similarity'].values
    std_devs = avg_similarities_by_mistakes['Std_Dev'].values

    # Scatter plot using averaged similarity - single color with error bars
    scatter = plt.scatter(avg_mistakes, avg_sims,
                         c='steelblue',
                         s=200, alpha=0.7, edgecolors='black', linewidth=1.5,
                         label='Average Similarity per Mistake Count')

    # Add error bars for standard deviation
    plt.errorbar(avg_mistakes, avg_sims, yerr=std_devs, fmt='none',
                ecolor='gray', alpha=0.5, capsize=5, capthick=2)

    # Calculate correlation using averaged data
    correlation = np.corrcoef(avg_mistakes, avg_sims)[0, 1]

    # Add trend line using averaged data
    z = np.polyfit(avg_mistakes, avg_sims, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(avg_mistakes), max(avg_mistakes), 100)
    plt.plot(x_trend, p(x_trend), "r--", linewidth=2.5, alpha=0.8,
             label=f'Trend: y = {z[0]:.5f}x + {z[1]:.4f}')

    # Labels and title
    plt.xlabel('Number of Mistakes in Original Sentence', fontsize=15, fontweight='bold')
    plt.ylabel('Average Cosine Similarity', fontsize=15, fontweight='bold')
    plt.title('Average Semantic Similarity After Translation Cycle (English → French → Hebrew → English)\n' +
              f'Correlation: {correlation:.3f}',
              fontsize=17, fontweight='bold', pad=20)

    # Grid
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Legend for trend line
    plt.legend(fontsize=12, loc='best')

    # Set x-axis to start from minimum mistakes value, not 0
    plt.xlim([min(avg_mistakes) - 0.5, max(avg_mistakes) + 0.5])

    # Set x-axis ticks to only show values that actually exist in the data
    min_mistake = int(min(avg_mistakes))
    max_mistake = int(max(avg_mistakes))
    # Create ticks at reasonable intervals
    tick_interval = max(1, (max_mistake - min_mistake) // 10)
    x_ticks = range(min_mistake, max_mistake + 1, tick_interval)
    plt.xticks(x_ticks)

    # Add text box with statistics
    stats_text = f'Overall Avg Similarity: {np.mean(similarities):.4f}\n'
    stats_text += f'Min Avg Similarity: {np.min(avg_sims):.4f}\n'
    stats_text += f'Max Avg Similarity: {np.max(avg_sims):.4f}\n'
    stats_text += f'Groups: {len(avg_mistakes)}'

    plt.text(0.02, 0.98, stats_text,
             transform=plt.gca().transAxes,
             fontsize=11,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    print(f"\nGraph saved to: {output_plot}")
    plt.close()

    print("\n" + "=" * 80)
    print("Analysis Summary")
    print("=" * 80)
    print(f"Correlation between mistakes and average cosine similarity: {correlation:.3f}")

    if abs(correlation) < 0.3:
        print("Interpretation: Weak correlation - number of mistakes has little impact on semantic similarity")
    elif abs(correlation) < 0.7:
        print("Interpretation: Moderate correlation - number of mistakes somewhat affects semantic similarity")
    else:
        print("Interpretation: Strong correlation - number of mistakes significantly affects semantic similarity")

    print("\nComparison complete!")

    return avg_similarities_by_mistakes, correlation

if __name__ == "__main__":
    import sys
    import os

    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Default files with new folder structure
    file1 = os.path.join(project_root, "data", "input", "English.csv")
    file2 = os.path.join(project_root, "data", "output", "English_final.csv")
    output = os.path.join(project_root, "visualizations", "vector_similarity_vs_mistakes.png")

    # Accept command line arguments
    if len(sys.argv) >= 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    if len(sys.argv) >= 4:
        output = sys.argv[3]

    try:
        compare_sentence_vectors(file1, file2, output)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
