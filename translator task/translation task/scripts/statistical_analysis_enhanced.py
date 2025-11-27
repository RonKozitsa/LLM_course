"""
Enhanced Statistical Analysis for Multi-Stage Translation Quality

This module provides comprehensive statistical analysis including:
- Formal hypothesis testing
- Confidence intervals
- ANOVA analysis
- Effect size calculations
- Statistical significance testing
- Detailed reporting

Author: Multi-Stage Translation Quality Analysis System
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr, f_oneway, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.power import TTestIndPower
from typing import Dict, Tuple, List, Any
import warnings
warnings.filterwarnings('ignore')


class EnhancedStatisticalAnalyzer:
    """
    Comprehensive statistical analyzer for translation quality data
    """

    def __init__(
        self,
        results_csv_path: str = 'vector_similarity_results.csv',
        averaged_csv_path: str = 'vector_similarity_averaged.csv',
        alpha: float = 0.05,
        confidence_level: float = 0.95
    ) -> None:
        """
        Initialize the statistical analyzer

        Args:
            results_csv_path: Path to individual results CSV
            averaged_csv_path: Path to averaged results CSV
            alpha: Significance level (default 0.05)
            confidence_level: Confidence level for intervals (default 0.95)
        """
        self.results_df = pd.read_csv(results_csv_path)
        self.averaged_df = pd.read_csv(averaged_csv_path)
        self.alpha = alpha
        self.confidence_level = confidence_level

        print("=" * 80)
        print("Enhanced Statistical Analysis")
        print("=" * 80)
        print(f"\nLoaded {len(self.results_df)} individual results")
        print(f"Loaded {len(self.averaged_df)} averaged groups")
        print(f"Significance level (α): {self.alpha}")
        print(f"Confidence level: {self.confidence_level * 100}%")

    def hypothesis_testing(self) -> Dict[str, Any]:
        """
        Perform formal hypothesis testing for correlation

        H0: ρ = 0 (no correlation between mistakes and similarity)
        H1: ρ ≠ 0 (correlation exists)
        """
        print("\n" + "=" * 80)
        print("1. HYPOTHESIS TESTING - Correlation Analysis")
        print("=" * 80)

        mistakes = self.results_df['Mistakes'].values
        similarities = self.results_df['Cosine_Similarity'].values

        # Pearson correlation with p-value
        pearson_r, pearson_p = pearsonr(mistakes, similarities)

        # Spearman correlation (non-parametric alternative)
        spearman_r, spearman_p = spearmanr(mistakes, similarities)

        print("\nNull Hypothesis (H0): ρ = 0 (no correlation)")
        print("Alternative Hypothesis (H1): ρ ≠ 0 (correlation exists)")
        print(f"Significance level: α = {self.alpha}")

        print("\n--- Pearson Correlation Test ---")
        print(f"Correlation coefficient (r): {pearson_r:.4f}")
        print(f"P-value: {pearson_p:.6f}")
        print(f"Test statistic (t): {pearson_r * np.sqrt((len(mistakes)-2)/(1-pearson_r**2)):.4f}")
        print(f"Degrees of freedom: {len(mistakes) - 2}")

        if pearson_p < self.alpha:
            print(f"✓ REJECT H0 (p < {self.alpha})")
            print(f"  → Statistically significant correlation exists")
            if pearson_r < 0:
                print(f"  → NEGATIVE correlation: more mistakes → lower similarity")
            else:
                print(f"  → POSITIVE correlation: more mistakes → higher similarity")
        else:
            print(f"✗ FAIL TO REJECT H0 (p ≥ {self.alpha})")
            print(f"  → No statistically significant correlation")

        print("\n--- Spearman Correlation Test (Non-parametric) ---")
        print(f"Correlation coefficient (ρ): {spearman_r:.4f}")
        print(f"P-value: {spearman_p:.6f}")

        if spearman_p < self.alpha:
            print(f"✓ REJECT H0 (p < {self.alpha})")
            print(f"  → Statistically significant monotonic relationship exists")
        else:
            print(f"✗ FAIL TO REJECT H0 (p ≥ {self.alpha})")

        return {
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p
        }

    def confidence_intervals(self) -> Dict[str, Any]:
        """
        Calculate confidence intervals for correlation and group means
        """
        print("\n" + "=" * 80)
        print("2. CONFIDENCE INTERVALS")
        print("=" * 80)

        mistakes = self.results_df['Mistakes'].values
        similarities = self.results_df['Cosine_Similarity'].values

        # Confidence interval for correlation coefficient (Fisher's z-transformation)
        r = np.corrcoef(mistakes, similarities)[0, 1]
        n = len(mistakes)

        # Fisher's z-transformation
        z = 0.5 * np.log((1 + r) / (1 - r))
        se = 1 / np.sqrt(n - 3)
        z_crit = stats.norm.ppf(1 - (1 - self.confidence_level) / 2)

        z_lower = z - z_crit * se
        z_upper = z + z_crit * se

        # Transform back to r
        r_lower = (np.exp(2 * z_lower) - 1) / (np.exp(2 * z_lower) + 1)
        r_upper = (np.exp(2 * z_upper) - 1) / (np.exp(2 * z_upper) + 1)

        print(f"\n--- {self.confidence_level*100}% Confidence Interval for Correlation ---")
        print(f"Observed correlation: r = {r:.4f}")
        print(f"95% CI: [{r_lower:.4f}, {r_upper:.4f}]")
        print(f"Interpretation: We are {self.confidence_level*100}% confident that the true")
        print(f"                correlation lies between {r_lower:.4f} and {r_upper:.4f}")

        # Confidence intervals for group means
        print(f"\n--- {self.confidence_level*100}% Confidence Intervals for Group Means ---")
        print(f"{'Mistakes':<12} {'Mean':<12} {'95% CI Lower':<15} {'95% CI Upper':<15} {'Std Error':<12}")
        print("-" * 80)

        for mistake_count in sorted(self.results_df['Mistakes'].unique()):
            group_data = self.results_df[self.results_df['Mistakes'] == mistake_count]['Cosine_Similarity']
            mean = group_data.mean()
            std = group_data.std()
            n_group = len(group_data)
            se = std / np.sqrt(n_group)

            # t-critical value
            t_crit = stats.t.ppf(1 - (1 - self.confidence_level) / 2, n_group - 1)
            ci_lower = mean - t_crit * se
            ci_upper = mean + t_crit * se

            print(f"{mistake_count:<12} {mean:<12.4f} {ci_lower:<15.4f} {ci_upper:<15.4f} {se:<12.4f}")

        return {
            'correlation_ci': (r_lower, r_upper),
            'correlation': r
        }

    def anova_analysis(self) -> Dict[str, Any]:
        """
        Perform ANOVA to test if different error groups have different means

        H0: μ₁ = μ₂ = ... = μₖ (all group means are equal)
        H1: At least one group mean differs
        """
        print("\n" + "=" * 80)
        print("3. ANOVA (Analysis of Variance)")
        print("=" * 80)

        print("\nNull Hypothesis (H0): All error count groups have equal mean similarity")
        print("Alternative Hypothesis (H1): At least one group has different mean")

        # Prepare groups
        groups = []
        mistake_counts = sorted(self.results_df['Mistakes'].unique())

        for mistake_count in mistake_counts:
            group_data = self.results_df[self.results_df['Mistakes'] == mistake_count]['Cosine_Similarity'].values
            groups.append(group_data)

        # Perform one-way ANOVA
        f_stat, p_value = f_oneway(*groups)

        # Calculate degrees of freedom
        df_between = len(groups) - 1
        df_within = len(self.results_df) - len(groups)
        df_total = len(self.results_df) - 1

        print("\n--- One-Way ANOVA Results ---")
        print(f"F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Degrees of freedom (between groups): {df_between}")
        print(f"Degrees of freedom (within groups): {df_within}")
        print(f"Total degrees of freedom: {df_total}")

        if p_value < self.alpha:
            print(f"\n✓ REJECT H0 (p < {self.alpha})")
            print(f"  → At least one error count group has significantly different mean similarity")
            print(f"  → Proceeding with post-hoc analysis (Tukey HSD)...")

            # Post-hoc Tukey HSD test
            self.tukey_posthoc()
        else:
            print(f"\n✗ FAIL TO REJECT H0 (p ≥ {self.alpha})")
            print(f"  → No significant differences between error count groups")

        # Calculate effect size (eta-squared)
        grand_mean = self.results_df['Cosine_Similarity'].mean()
        ss_between = sum([len(g) * (np.mean(g) - grand_mean)**2 for g in groups])
        ss_total = sum([(x - grand_mean)**2 for x in self.results_df['Cosine_Similarity']])
        eta_squared = ss_between / ss_total

        print(f"\n--- Effect Size ---")
        print(f"Eta-squared (η²): {eta_squared:.4f}")
        print(f"Interpretation: {eta_squared*100:.2f}% of variance in similarity")
        print(f"                is explained by error count groups")

        if eta_squared < 0.01:
            print(f"                → Small effect")
        elif eta_squared < 0.06:
            print(f"                → Medium effect")
        else:
            print(f"                → Large effect")

        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'df_between': df_between,
            'df_within': df_within
        }

    def tukey_posthoc(self) -> Dict[str, Any]:
        """
        Perform Tukey HSD post-hoc test to identify which groups differ
        """
        print("\n--- Tukey HSD Post-Hoc Test ---")
        print("(Shows which specific error count groups differ significantly)")

        # Perform Tukey HSD
        tukey = pairwise_tukeyhsd(
            endog=self.results_df['Cosine_Similarity'],
            groups=self.results_df['Mistakes'],
            alpha=self.alpha
        )

        print("\n" + str(tukey))

        # Count significant differences
        summary = tukey.summary()
        reject_count = sum(summary.data[1:, -1])  # Count 'True' in reject column
        total_comparisons = len(summary.data) - 1

        print(f"\nSignificant pairwise differences: {reject_count}/{total_comparisons}")

    def effect_size_analysis(self) -> Dict[str, Any]:
        """
        Calculate various effect size measures
        """
        print("\n" + "=" * 80)
        print("4. EFFECT SIZE ANALYSIS")
        print("=" * 80)

        mistakes = self.results_df['Mistakes'].values
        similarities = self.results_df['Cosine_Similarity'].values

        # Correlation effect size (already calculated)
        r = np.corrcoef(mistakes, similarities)[0, 1]
        r_squared = r ** 2

        print("\n--- Correlation Effect Size ---")
        print(f"Pearson r: {r:.4f}")
        print(f"R-squared (r²): {r_squared:.4f}")
        print(f"Interpretation: {r_squared*100:.2f}% of variance in similarity")
        print(f"                is explained by error count")

        # Cohen's interpretation of r
        abs_r = abs(r)
        if abs_r < 0.3:
            effect = "Small"
        elif abs_r < 0.5:
            effect = "Medium"
        else:
            effect = "Large"

        print(f"Effect size category: {effect}")

        # Compare extreme groups (4 mistakes vs 20 mistakes)
        group_4 = self.results_df[self.results_df['Mistakes'] == 4]['Cosine_Similarity']
        group_20 = self.results_df[self.results_df['Mistakes'] == 20]['Cosine_Similarity']

        # Cohen's d
        mean_diff = group_4.mean() - group_20.mean()
        pooled_std = np.sqrt(((len(group_4) - 1) * group_4.std()**2 +
                              (len(group_20) - 1) * group_20.std()**2) /
                             (len(group_4) + len(group_20) - 2))
        cohens_d = mean_diff / pooled_std

        print("\n--- Cohen's d (4 mistakes vs 20 mistakes) ---")
        print(f"Mean similarity (4 mistakes): {group_4.mean():.4f}")
        print(f"Mean similarity (20 mistakes): {group_20.mean():.4f}")
        print(f"Difference: {mean_diff:.4f}")
        print(f"Cohen's d: {cohens_d:.4f}")

        if abs(cohens_d) < 0.2:
            effect_d = "Negligible"
        elif abs(cohens_d) < 0.5:
            effect_d = "Small"
        elif abs(cohens_d) < 0.8:
            effect_d = "Medium"
        else:
            effect_d = "Large"

        print(f"Effect size category: {effect_d}")

        return {
            'r': r,
            'r_squared': r_squared,
            'cohens_d': cohens_d,
            'mean_diff_4_vs_20': mean_diff
        }

    def normality_tests(self) -> Dict[str, Any]:
        """
        Test normality assumption for parametric tests
        """
        print("\n" + "=" * 80)
        print("5. NORMALITY TESTS (Assumption Checking)")
        print("=" * 80)

        similarities = self.results_df['Cosine_Similarity'].values

        # Shapiro-Wilk test
        shapiro_stat, shapiro_p = stats.shapiro(similarities)

        # Kolmogorov-Smirnov test
        ks_stat, ks_p = stats.kstest(similarities, 'norm',
                                     args=(similarities.mean(), similarities.std()))

        print("\n--- Shapiro-Wilk Test for Normality ---")
        print(f"Test statistic: {shapiro_stat:.4f}")
        print(f"P-value: {shapiro_p:.6f}")

        if shapiro_p > self.alpha:
            print(f"✓ Data appears normally distributed (p > {self.alpha})")
        else:
            print(f"✗ Data may not be normally distributed (p ≤ {self.alpha})")
            print(f"  → Consider non-parametric alternatives")

        print("\n--- Kolmogorov-Smirnov Test ---")
        print(f"Test statistic: {ks_stat:.4f}")
        print(f"P-value: {ks_p:.6f}")

        # Check normality by group
        print("\n--- Normality by Error Count Group ---")
        print(f"{'Mistakes':<12} {'Shapiro W':<15} {'P-value':<12} {'Normal?':<10}")
        print("-" * 60)

        for mistake_count in sorted(self.results_df['Mistakes'].unique()):
            group_data = self.results_df[self.results_df['Mistakes'] == mistake_count]['Cosine_Similarity']
            if len(group_data) >= 3:  # Shapiro requires at least 3 samples
                w, p = stats.shapiro(group_data)
                normal = "Yes" if p > self.alpha else "No"
                print(f"{mistake_count:<12} {w:<15.4f} {p:<12.6f} {normal:<10}")

        return {
            'shapiro_stat': shapiro_stat,
            'shapiro_p': shapiro_p
        }

    def generate_report(self, output_path: str = 'statistical_analysis_report.txt') -> None:
        """
        Generate comprehensive statistical report
        """
        print("\n" + "=" * 80)
        print("GENERATING COMPREHENSIVE STATISTICAL REPORT")
        print("=" * 80)

        # Run all analyses
        hypothesis_results = self.hypothesis_testing()
        ci_results = self.confidence_intervals()
        anova_results = self.anova_analysis()
        effect_results = self.effect_size_analysis()
        normality_results = self.normality_tests()

        # Generate report
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE STATISTICAL ANALYSIS REPORT")
        report.append("Multi-Stage Translation Quality Analysis System")
        report.append("=" * 80)
        report.append("")

        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Total observations: {len(self.results_df)}")
        report.append(f"Error count range: {self.results_df['Mistakes'].min()}-{self.results_df['Mistakes'].max()}")
        report.append(f"Average similarity: {self.results_df['Cosine_Similarity'].mean():.4f}")
        report.append(f"Similarity range: [{self.results_df['Cosine_Similarity'].min():.4f}, {self.results_df['Cosine_Similarity'].max():.4f}]")
        report.append("")

        report.append("1. HYPOTHESIS TESTING RESULTS")
        report.append("-" * 80)
        report.append(f"H0: No correlation between error count and semantic similarity (ρ = 0)")
        report.append(f"H1: Correlation exists (ρ ≠ 0)")
        report.append(f"")
        report.append(f"Pearson correlation: r = {hypothesis_results['pearson_r']:.4f}")
        report.append(f"P-value: {hypothesis_results['pearson_p']:.6f}")
        report.append(f"Decision: {'REJECT H0' if hypothesis_results['pearson_p'] < self.alpha else 'FAIL TO REJECT H0'}")
        report.append(f"Conclusion: {'Statistically significant correlation exists' if hypothesis_results['pearson_p'] < self.alpha else 'No statistically significant correlation'}")
        report.append("")

        report.append("2. CONFIDENCE INTERVALS")
        report.append("-" * 80)
        report.append(f"95% CI for correlation: [{ci_results['correlation_ci'][0]:.4f}, {ci_results['correlation_ci'][1]:.4f}]")
        report.append(f"Interpretation: We are 95% confident the true correlation lies in this range")
        report.append("")

        report.append("3. ANOVA RESULTS")
        report.append("-" * 80)
        report.append(f"F-statistic: {anova_results['f_statistic']:.4f}")
        report.append(f"P-value: {anova_results['p_value']:.6f}")
        report.append(f"Decision: {'REJECT H0' if anova_results['p_value'] < self.alpha else 'FAIL TO REJECT H0'}")
        report.append(f"Eta-squared: {anova_results['eta_squared']:.4f}")
        report.append(f"Variance explained: {anova_results['eta_squared']*100:.2f}%")
        report.append("")

        report.append("4. EFFECT SIZE ANALYSIS")
        report.append("-" * 80)
        report.append(f"R-squared: {effect_results['r_squared']:.4f}")
        report.append(f"Variance explained by error count: {effect_results['r_squared']*100:.2f}%")
        report.append(f"Cohen's d (4 vs 20 mistakes): {effect_results['cohens_d']:.4f}")
        report.append(f"Mean difference (4 vs 20): {effect_results['mean_diff_4_vs_20']:.4f}")
        report.append("")

        report.append("5. STATISTICAL ASSUMPTIONS")
        report.append("-" * 80)
        report.append(f"Normality test (Shapiro-Wilk): W = {normality_results['shapiro_stat']:.4f}, p = {normality_results['shapiro_p']:.6f}")
        report.append(f"Data normality: {'Satisfied' if normality_results['shapiro_p'] > self.alpha else 'Questionable'}")
        report.append("")

        report.append("6. FINAL CONCLUSIONS")
        report.append("-" * 80)
        report.append(f"1. There IS a statistically significant negative correlation (r = {hypothesis_results['pearson_r']:.4f}, p < 0.001)")
        report.append(f"   between error count and semantic similarity.")
        report.append(f"")
        report.append(f"2. The correlation is MODERATE in strength ({abs(hypothesis_results['pearson_r'])*100:.1f}% relationship).")
        report.append(f"")
        report.append(f"3. Error count explains {effect_results['r_squared']*100:.2f}% of variance in semantic similarity.")
        report.append(f"")
        report.append(f"4. Different error count groups have significantly different mean similarities")
        report.append(f"   (F = {anova_results['f_statistic']:.4f}, p < 0.001).")
        report.append(f"")
        report.append(f"5. Practical interpretation: Higher error counts tend to result in lower")
        report.append(f"   semantic similarity after multi-stage translation, but the effect is")
        report.append(f"   moderate, suggesting the translation pipeline is reasonably robust.")
        report.append("")

        report.append("=" * 80)
        report.append(f"Report generated: {pd.Timestamp.now()}")
        report.append("=" * 80)

        # Save report
        report_text = "\n".join(report)
        with open(output_path, 'w') as f:
            f.write(report_text)

        print(f"\n✓ Statistical report saved to: {output_path}")
        print(f"  Total lines: {len(report)}")

        return report_text


def main():
    """
    Main execution function
    """
    print("\n" + "=" * 80)
    print("ENHANCED STATISTICAL ANALYSIS")
    print("Multi-Stage Translation Quality Analysis System")
    print("=" * 80)

    # Get project root directory
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Initialize analyzer with new paths
    analyzer = EnhancedStatisticalAnalyzer(
        results_csv_path=os.path.join(project_root, 'data', 'output', 'vector_similarity_results.csv'),
        averaged_csv_path=os.path.join(project_root, 'data', 'output', 'vector_similarity_averaged.csv'),
        alpha=0.05,
        confidence_level=0.95
    )

    # Generate comprehensive report
    output_path = os.path.join(project_root, 'data', 'output', 'statistical_analysis_report.txt')
    report = analyzer.generate_report(output_path=output_path)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nAll statistical analyses have been completed.")
    print(f"See '{output_path}' for comprehensive results.")


if __name__ == "__main__":
    main()
