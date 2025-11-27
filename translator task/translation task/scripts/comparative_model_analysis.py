"""
Comparative Model Analysis for Translation Quality

This script compares multiple sentence embedding models to evaluate
translation quality and establish baselines.

Models tested:
1. all-MiniLM-L6-v2 (current model)
2. all-mpnet-base-v2 (larger, more accurate)
3. paraphrase-multilingual-MiniLM-L12-v2 (multilingual)
4. all-distilroberta-v1 (alternative architecture)

Also includes baseline comparison: English.csv vs itself (identity)

Author: Multi-Stage Translation Quality Analysis System
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')
import time


class ComparativeModelAnalyzer:
    """
    Compare multiple sentence embedding models for translation quality analysis
    """

    def __init__(self, english_csv='English.csv', english_final_csv='English_final.csv'):
        """
        Initialize the comparative analyzer

        Args:
            english_csv: Path to original English CSV
            english_final_csv: Path to final translated English CSV
        """
        self.english_df = pd.read_csv(english_csv)
        self.english_final_df = pd.read_csv(english_final_csv)

        # Models to compare
        self.models = {
            'all-MiniLM-L6-v2': 'sentence-transformers/all-MiniLM-L6-v2',
            'all-mpnet-base-v2': 'sentence-transformers/all-mpnet-base-v2',
            'paraphrase-multilingual': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
            'all-distilroberta-v1': 'sentence-transformers/all-distilroberta-v1'
        }

        self.results = {}

        print("=" * 80)
        print("COMPARATIVE MODEL ANALYSIS")
        print("=" * 80)
        print(f"\nLoaded {len(self.english_df)} original sentences")
        print(f"Loaded {len(self.english_final_df)} translated sentences")
        print(f"\nModels to test: {len(self.models)}")
        for name in self.models.keys():
            print(f"  - {name}")

    def calculate_baseline(self):
        """
        Calculate baseline similarity (English.csv vs itself)
        This shows perfect translation would have similarity ~1.0
        """
        print("\n" + "=" * 80)
        print("BASELINE ANALYSIS (Identity Comparison)")
        print("=" * 80)
        print("\nComparing English.csv with itself (perfect identity)")
        print("This establishes the upper bound for similarity scores")

        # Use current model for baseline
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        sentences = self.english_df['text'].tolist()
        vectors = model.encode(sentences, show_progress_bar=True)

        # Calculate similarity with itself
        similarities = []
        for i in range(len(vectors)):
            sim = cosine_similarity([vectors[i]], [vectors[i]])[0][0]
            similarities.append(sim)

        baseline = {
            'mean_similarity': np.mean(similarities),
            'min_similarity': np.min(similarities),
            'max_similarity': np.max(similarities),
            'std_similarity': np.std(similarities)
        }

        print(f"\nBaseline Results (Identity):")
        print(f"  Mean similarity: {baseline['mean_similarity']:.6f}")
        print(f"  Min similarity: {baseline['min_similarity']:.6f}")
        print(f"  Max similarity: {baseline['max_similarity']:.6f}")
        print(f"  Std deviation: {baseline['std_similarity']:.6f}")
        print(f"\nInterpretation: Perfect similarity should be 1.000000")
        print(f"                Actual: {baseline['mean_similarity']:.6f} (numerical precision)")

        self.results['baseline'] = baseline
        return baseline

    def analyze_model(self, model_name, model_path):
        """
        Analyze translation quality using a specific model

        Args:
            model_name: Display name of the model
            model_path: Hugging Face model path

        Returns:
            dict: Analysis results
        """
        print(f"\n" + "-" * 80)
        print(f"Testing: {model_name}")
        print("-" * 80)

        start_time = time.time()

        # Load model
        print(f"Loading model...")
        model = SentenceTransformer(model_path)

        # Encode sentences
        print(f"Encoding original sentences...")
        original_vectors = model.encode(self.english_df['text'].tolist(),
                                       show_progress_bar=True, batch_size=32)

        print(f"Encoding translated sentences...")
        final_vectors = model.encode(self.english_final_df['text'].tolist(),
                                     show_progress_bar=True, batch_size=32)

        # Calculate similarities
        print(f"Calculating similarities...")
        similarities = []
        for i in range(len(original_vectors)):
            sim = cosine_similarity([original_vectors[i]], [final_vectors[i]])[0][0]
            similarities.append(sim)

        # Calculate correlation with mistakes
        mistakes = self.english_df['mistakes'].values
        correlation, p_value = pearsonr(mistakes, similarities)

        # Group by mistake count
        results_df = pd.DataFrame({
            'Mistakes': mistakes,
            'Similarity': similarities
        })
        grouped = results_df.groupby('Mistakes')['Similarity'].agg(['mean', 'std'])

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Compile results
        model_results = {
            'model_name': model_name,
            'model_path': model_path,
            'mean_similarity': np.mean(similarities),
            'std_similarity': np.std(similarities),
            'min_similarity': np.min(similarities),
            'max_similarity': np.max(similarities),
            'correlation': correlation,
            'p_value': p_value,
            'grouped_means': grouped['mean'].to_dict(),
            'vector_dimensions': original_vectors.shape[1],
            'processing_time': elapsed_time,
            'similarities': similarities
        }

        print(f"\nResults for {model_name}:")
        print(f"  Vector dimensions: {model_results['vector_dimensions']}")
        print(f"  Mean similarity: {model_results['mean_similarity']:.4f}")
        print(f"  Std deviation: {model_results['std_similarity']:.4f}")
        print(f"  Similarity range: [{model_results['min_similarity']:.4f}, {model_results['max_similarity']:.4f}]")
        print(f"  Correlation with mistakes: r = {model_results['correlation']:.4f} (p = {model_results['p_value']:.6f})")
        print(f"  Processing time: {model_results['processing_time']:.2f} seconds")

        self.results[model_name] = model_results
        return model_results

    def run_all_comparisons(self):
        """
        Run analysis for all models
        """
        print("\n" + "=" * 80)
        print("RUNNING COMPARATIVE ANALYSIS")
        print("=" * 80)

        # Calculate baseline first
        self.calculate_baseline()

        # Test each model
        for model_name, model_path in self.models.items():
            try:
                self.analyze_model(model_name, model_path)
            except Exception as e:
                print(f"\n✗ Error with {model_name}: {e}")
                print(f"  Skipping this model...")

        print("\n" + "=" * 80)
        print("ALL MODELS TESTED")
        print("=" * 80)

    def generate_comparison_report(self, output_path='comparative_analysis_report.txt'):
        """
        Generate comprehensive comparison report
        """
        print("\n" + "=" * 80)
        print("GENERATING COMPARISON REPORT")
        print("=" * 80)

        report = []
        report.append("=" * 80)
        report.append("COMPARATIVE MODEL ANALYSIS REPORT")
        report.append("Multi-Stage Translation Quality Analysis System")
        report.append("=" * 80)
        report.append("")

        # Baseline
        if 'baseline' in self.results:
            report.append("BASELINE (Identity Comparison)")
            report.append("-" * 80)
            baseline = self.results['baseline']
            report.append(f"Mean similarity (English.csv vs itself): {baseline['mean_similarity']:.6f}")
            report.append(f"This represents perfect translation (no degradation)")
            report.append("")

        # Model comparison table
        report.append("MODEL PERFORMANCE COMPARISON")
        report.append("-" * 80)
        report.append(f"{'Model':<30} {'Dims':<8} {'Mean Sim':<12} {'Correlation':<15} {'P-value':<12} {'Time (s)':<10}")
        report.append("-" * 80)

        models_to_report = [k for k in self.results.keys() if k != 'baseline']
        for model_name in models_to_report:
            r = self.results[model_name]
            report.append(f"{model_name:<30} {r['vector_dimensions']:<8} "
                         f"{r['mean_similarity']:<12.4f} {r['correlation']:<15.4f} "
                         f"{r['p_value']:<12.6f} {r['processing_time']:<10.2f}")

        report.append("")

        # Detailed analysis
        report.append("DETAILED ANALYSIS BY MODEL")
        report.append("=" * 80)

        for model_name in models_to_report:
            r = self.results[model_name]
            report.append(f"\n{model_name}")
            report.append("-" * 80)
            report.append(f"Vector dimensions: {r['vector_dimensions']}")
            report.append(f"Mean similarity: {r['mean_similarity']:.4f} ± {r['std_similarity']:.4f}")
            report.append(f"Similarity range: [{r['min_similarity']:.4f}, {r['max_similarity']:.4f}]")
            report.append(f"Correlation with error count: r = {r['correlation']:.4f}")
            report.append(f"Statistical significance: p = {r['p_value']:.6f} ({'Significant' if r['p_value'] < 0.05 else 'Not significant'})")
            report.append(f"Processing time: {r['processing_time']:.2f} seconds")
            report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("=" * 80)

        # Find best model by mean similarity
        best_by_similarity = max(models_to_report, key=lambda x: self.results[x]['mean_similarity'])
        # Find best by correlation strength
        best_by_correlation = max(models_to_report, key=lambda x: abs(self.results[x]['correlation']))
        # Find fastest
        fastest = min(models_to_report, key=lambda x: self.results[x]['processing_time'])

        report.append(f"Best average similarity: {best_by_similarity}")
        report.append(f"  Mean similarity: {self.results[best_by_similarity]['mean_similarity']:.4f}")
        report.append("")
        report.append(f"Strongest correlation with errors: {best_by_correlation}")
        report.append(f"  Correlation: {self.results[best_by_correlation]['correlation']:.4f}")
        report.append("")
        report.append(f"Fastest processing: {fastest}")
        report.append(f"  Processing time: {self.results[fastest]['processing_time']:.2f} seconds")
        report.append("")

        # Overall recommendation
        report.append("OVERALL RECOMMENDATION:")
        report.append(f"For this translation quality analysis task, {best_by_similarity} provides")
        report.append(f"the best balance of similarity detection with semantic degradation after")
        report.append(f"multi-stage translation (mean similarity: {self.results[best_by_similarity]['mean_similarity']:.4f}).")
        report.append("")

        report.append("=" * 80)
        report.append(f"Report generated: {pd.Timestamp.now()}")
        report.append("=" * 80)

        # Save report
        report_text = "\n".join(report)
        with open(output_path, 'w') as f:
            f.write(report_text)

        print(f"\n✓ Comparison report saved to: {output_path}")

        return report_text

    def visualize_comparison(self, output_path='model_comparison_visualization.png'):
        """
        Create comparison visualizations
        """
        print("\n" + "=" * 80)
        print("CREATING COMPARISON VISUALIZATIONS")
        print("=" * 80)

        models_to_plot = [k for k in self.results.keys() if k != 'baseline']

        if len(models_to_plot) == 0:
            print("No models to visualize")
            return

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Mean similarity comparison
        means = [self.results[m]['mean_similarity'] for m in models_to_plot]
        stds = [self.results[m]['std_similarity'] for m in models_to_plot]

        axes[0, 0].bar(range(len(models_to_plot)), means, yerr=stds, capsize=5,
                       color='steelblue', edgecolor='black', alpha=0.7)
        axes[0, 0].set_xticks(range(len(models_to_plot)))
        axes[0, 0].set_xticklabels(models_to_plot, rotation=15, ha='right')
        axes[0, 0].set_ylabel('Mean Cosine Similarity', fontsize=12, fontweight='bold')
        axes[0, 0].set_title('Average Similarity by Model', fontsize=13, fontweight='bold')
        axes[0, 0].grid(alpha=0.3, axis='y')

        # 2. Correlation comparison
        correlations = [self.results[m]['correlation'] for m in models_to_plot]
        colors = ['red' if c < 0 else 'green' for c in correlations]

        axes[0, 1].bar(range(len(models_to_plot)), correlations,
                       color=colors, edgecolor='black', alpha=0.7)
        axes[0, 1].axhline(0, color='black', linestyle='--', linewidth=1)
        axes[0, 1].set_xticks(range(len(models_to_plot)))
        axes[0, 1].set_xticklabels(models_to_plot, rotation=15, ha='right')
        axes[0, 1].set_ylabel('Correlation Coefficient', fontsize=12, fontweight='bold')
        axes[0, 1].set_title('Correlation with Error Count', fontsize=13, fontweight='bold')
        axes[0, 1].grid(alpha=0.3, axis='y')

        # 3. Processing time comparison
        times = [self.results[m]['processing_time'] for m in models_to_plot]

        axes[1, 0].bar(range(len(models_to_plot)), times,
                       color='orange', edgecolor='black', alpha=0.7)
        axes[1, 0].set_xticks(range(len(models_to_plot)))
        axes[1, 0].set_xticklabels(models_to_plot, rotation=15, ha='right')
        axes[1, 0].set_ylabel('Processing Time (seconds)', fontsize=12, fontweight='bold')
        axes[1, 0].set_title('Computational Efficiency', fontsize=13, fontweight='bold')
        axes[1, 0].grid(alpha=0.3, axis='y')

        # 4. Similarity distribution comparison (box plot)
        similarity_data = [self.results[m]['similarities'] for m in models_to_plot]

        bp = axes[1, 1].boxplot(similarity_data, labels=models_to_plot, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)
        axes[1, 1].set_xticklabels(models_to_plot, rotation=15, ha='right')
        axes[1, 1].set_ylabel('Cosine Similarity', fontsize=12, fontweight='bold')
        axes[1, 1].set_title('Similarity Distribution Comparison', fontsize=13, fontweight='bold')
        axes[1, 1].grid(alpha=0.3, axis='y')

        plt.suptitle('Comparative Model Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_path}")
        plt.close()

    def save_results_csv(self, output_path='comparative_analysis_results.csv'):
        """
        Save detailed results to CSV
        """
        rows = []
        for model_name, results in self.results.items():
            if model_name == 'baseline':
                continue

            rows.append({
                'Model': model_name,
                'Vector_Dimensions': results['vector_dimensions'],
                'Mean_Similarity': results['mean_similarity'],
                'Std_Similarity': results['std_similarity'],
                'Min_Similarity': results['min_similarity'],
                'Max_Similarity': results['max_similarity'],
                'Correlation': results['correlation'],
                'P_Value': results['p_value'],
                'Processing_Time_Seconds': results['processing_time']
            })

        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        print(f"\n✓ Results saved to CSV: {output_path}")


def main():
    """
    Main execution function
    """
    import os

    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("\n" + "=" * 80)
    print("COMPARATIVE MODEL ANALYSIS")
    print("Multi-Stage Translation Quality Analysis System")
    print("=" * 80)

    # Initialize analyzer with new paths
    analyzer = ComparativeModelAnalyzer(
        english_csv=os.path.join(project_root, 'data', 'input', 'English.csv'),
        english_final_csv=os.path.join(project_root, 'data', 'output', 'English_final.csv')
    )

    # Run all comparisons
    analyzer.run_all_comparisons()

    # Generate reports and visualizations
    report_path = os.path.join(project_root, 'data', 'output', 'comparative_analysis_report.txt')
    viz_path = os.path.join(project_root, 'visualizations', 'model_comparison_visualization.png')
    csv_path = os.path.join(project_root, 'data', 'output', 'comparative_analysis_results.csv')

    analyzer.generate_comparison_report(output_path=report_path)
    analyzer.visualize_comparison(output_path=viz_path)
    analyzer.save_results_csv(output_path=csv_path)

    print("\n" + "=" * 80)
    print("COMPARATIVE ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print(f"  - {report_path}")
    print(f"  - {viz_path}")
    print(f"  - {csv_path}")


if __name__ == "__main__":
    main()
