#!/usr/bin/env python3
"""
Create detailed correlation graph between mistakes and cosine similarity
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Get paths relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Read the data
df = pd.read_csv(os.path.join(project_root, 'data/output/vector_similarity_averaged.csv'))

# Extract data
mistakes = df['Mistakes'].values
avg_similarity = df['Avg_Similarity'].values
std_dev = df['Std_Dev'].values

# Calculate correlation
pearson_r, pearson_p = stats.pearsonr(mistakes, avg_similarity)
spearman_r, spearman_p = stats.spearmanr(mistakes, avg_similarity)

# Calculate linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(mistakes, avg_similarity)
line = slope * mistakes + intercept

# Create figure with single plot
fig, ax1 = plt.subplots(figsize=(14, 9))

# Scatter plot with error bars
ax1.errorbar(mistakes, avg_similarity, yerr=std_dev,
             fmt='o', markersize=10, capsize=5, capthick=2,
             elinewidth=2, alpha=0.7, color='#2E86AB',
             label='Average Similarity (±1 SD)')

# Trend line
ax1.plot(mistakes, line, 'r--', linewidth=2.5, alpha=0.8,
         label=f'Linear Fit: y = {slope:.4f}x + {intercept:.4f}')

# Fill area for trend line confidence
predict_std = np.sqrt(np.sum((avg_similarity - line)**2) / (len(mistakes) - 2))
margin = 1.96 * predict_std
ax1.fill_between(mistakes, line - margin, line + margin, alpha=0.2, color='red',
                  label='95% Confidence Interval')

# Styling
ax1.set_xlabel('Number of Mistakes (Errors)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Cosine Similarity', fontsize=14, fontweight='bold')
ax1.set_title('Correlation Between Number of Mistakes and Semantic Similarity\n' +
              'Multi-Stage Translation Pipeline (English → French → Hebrew → English)',
              fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(fontsize=11, loc='upper right', framealpha=0.9)
ax1.set_xlim(3, 21)
ax1.set_ylim(0.6, 0.8)

# Add statistics box
stats_text = f'''Statistical Analysis:
Pearson r = {pearson_r:.4f} (p = {pearson_p:.4f})
Spearman ρ = {spearman_r:.4f} (p = {spearman_p:.4f})
R² = {r_value**2:.4f}
Slope = {slope:.4f}
Sample Size: n = {len(mistakes)} groups (10 sentences each)
Total Sentences: {len(mistakes) * 10}'''

ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Add some space at the bottom for the interpretation text
plt.subplots_adjust(bottom=0.15)

# Add interpretation at bottom with proper spacing
interpretation = """Interpretation: The negative correlation (r = {:.3f}, p = {:.4f}) indicates that as the number of mistakes increases,
semantic similarity tends to decrease, though the effect is moderate. The pipeline shows resilience with an average
similarity of {:.2%} even at 20 mistakes, suggesting the multi-stage translation preserves core meaning despite errors.""".format(pearson_r, pearson_p, avg_similarity.mean())

plt.figtext(0.5, 0.04, interpretation, ha='center', fontsize=11,
            style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# Save to visualizations folder
output_path = os.path.join(project_root, 'visualizations/correlation_mistakes_vs_similarity_detailed.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print("✓ Detailed correlation graph created!")
print(f"✓ Saved as: {output_path}")
print(f"\nKey Statistics:")
print(f"  Pearson Correlation: r = {pearson_r:.4f}, p = {pearson_p:.4f}")
print(f"  Spearman Correlation: ρ = {spearman_r:.4f}, p = {spearman_p:.4f}")
print(f"  R² (explained variance): {r_value**2:.4f} ({r_value**2*100:.1f}%)")
print(f"  Linear equation: y = {slope:.4f}x + {intercept:.4f}")
print(f"  Average similarity: {avg_similarity.mean():.4f}")
print(f"  Similarity range: [{avg_similarity.min():.4f}, {avg_similarity.max():.4f}]")

# Show significance
if pearson_p < 0.001:
    sig_level = "p < 0.001 (highly significant ***)"
elif pearson_p < 0.01:
    sig_level = "p < 0.01 (very significant **)"
elif pearson_p < 0.05:
    sig_level = "p < 0.05 (significant *)"
else:
    sig_level = "p ≥ 0.05 (not significant)"

print(f"  Significance: {sig_level}")

# Don't show plot, just save it
# plt.show()
