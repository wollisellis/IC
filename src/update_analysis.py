import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr, shapiro, kruskal
import statsmodels.api as sm
from statsmodels.stats.power import TTestIndPower

# Load processed data with encoded variables and recalculated caffeine
df_proc = pd.read_csv("IC_Dados_Processados.csv", encoding='utf-8-sig')
# Recalculated caffeine values
df_recalc = pd.read_csv("IC_Dados_Curados_Cafeina_Recalculada_v3.csv", encoding='utf-8-sig')[['MG_CAFEINA_TOTAL_DIA_RECALCULADA']]
# Merge on row index
df = pd.concat([df_proc.reset_index(drop=True), df_recalc.reset_index(drop=True)], axis=1)

# Column with caffeine values
col_cafe = "MG_CAFEINA_TOTAL_DIA_RECALCULADA"

# Map hours category to numeric for correlation (H2)
HOURS_MAP = {
    "Menos de 1 hora": 0.5,
    "1-2 horas": 1.5,
    "2-4 horas": 3.0,
    "4-6 horas": 5.0,
    "Mais de 6 horas": 7.0
}
col_hours = "Quantas horas por dia, em média, você joga e-sports?"
df_hours_cat = df[col_hours].astype(str).str.strip()
df_hours_num = df_hours_cat.map(HOURS_MAP)

# H1 updated: Amador/Jogador casual vs Semi-Profissional (exclude Profissionais devido a N muito baixo)
col_level = "Em qual nível você se classifica como jogador de esportes eletrônicos?"
mask_exp = df[col_level].isin(["Amador/Jogador casual", "Semi-Profissional"])
sub_exp = df[mask_exp]
am_values = sub_exp[sub_exp[col_level] == "Amador/Jogador casual"][col_cafe].dropna()
sp_values = sub_exp[sub_exp[col_level] == "Semi-Profissional"][col_cafe].dropna()
U_H1, p_H1 = mannwhitneyu(am_values, sp_values, alternative='two-sided')

# H1 alternative: combine Semi-Profissional and Profissional into one 'higher level' group
mask_high = df[col_level].isin(["Semi-Profissional", "Profissional"])
high_values = df[mask_high][col_cafe].dropna()
U_H1_alt, p_H1_alt = mannwhitneyu(am_values, high_values, alternative='two-sided')

# Global Kruskal-Wallis test for H1 across all three experience levels
prof_values = df[df[col_level] == "Profissional"][col_cafe].dropna()
H_H1_global, p_H1_global = kruskal(am_values, sp_values, prof_values)

# H6 updated: Masculino vs Feminino (excluir outros gênero/missing devido a N pequeno)
col_gender = "Gênero"
mask_gender = df[col_gender].isin(["Masculino", "Feminino"])
sub_gender = df[mask_gender]
male_values = sub_gender[sub_gender[col_gender] == "Masculino"][col_cafe].dropna()
fem_values = sub_gender[sub_gender[col_gender] == "Feminino"][col_cafe].dropna()
U_H6, p_H6 = mannwhitneyu(male_values, fem_values, alternative='two-sided')

# H2: Spearman correlation between caffeine and hours played
mask_h2 = df_hours_num.notnull() & df[col_cafe].notnull()
rho_H2, p_H2 = spearmanr(df[col_cafe][mask_h2], df_hours_num[mask_h2])
rho_H2_log, p_H2_log = spearmanr(np.log1p(df[col_cafe][mask_h2]), df_hours_num[mask_h2])

# Normality tests for caffeine distribution and log-transformed
df_cafe_nonan = df[col_cafe].dropna()
w_orig, p_shapiro_orig = shapiro(df_cafe_nonan)
w_log, p_shapiro_log = shapiro(np.log1p(df_cafe_nonan))

# Effect size for Mann-Whitney (r) calculation
import math

def mannwhitney_r(U, n1, n2):
    """Calculate effect size r from Mann-Whitney U."""
    mean_U = n1 * n2 / 2
    std_U = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (U - mean_U) / std_U
    return z / math.sqrt(n1 + n2)

r_H1 = mannwhitney_r(U_H1, len(am_values), len(sp_values))
r_H1_alt = mannwhitney_r(U_H1_alt, len(am_values), len(high_values))
r_H6 = mannwhitney_r(U_H6, len(male_values), len(fem_values))

# Output updated results
print("H1 (Mann-Whitney) Amador vs Semi-Profissional:")
print(f"U = {U_H1:.2f}, p = {p_H1:.4f}, N_am = {len(am_values)}, N_sp = {len(sp_values)}")

# Global Kruskal-Wallis test output for H1
print()
print("H1 global (Kruskal-Wallis) entre Amador, Semi-Profissional e Profissional:")
print(f"H = {H_H1_global:.2f}, p = {p_H1_global:.4f}")

print()
print("H1 alternative (Mann-Whitney) Amador vs (Semi-Profissional + Profissional):")
print(f"U = {U_H1_alt:.2f}, p = {p_H1_alt:.4f}, N_high = {len(high_values)}")
print()
print("H6 (Mann-Whitney) Masculino vs Feminino:")
print(f"U = {U_H6:.2f}, p = {p_H6:.4f}, N_male = {len(male_values)}, N_fem = {len(fem_values)}")

# Output additional statistics
print()
print("Effect sizes:")
print(f"H1 r = {r_H1:.4f}")
print(f"H1 alt r = {r_H1_alt:.4f}")
print(f"H6 r = {r_H6:.4f}")
print()
print("Normality tests (Shapiro-Wilk):")
print(f"Caffeine original: W = {w_orig:.4f}, p = {p_shapiro_orig:.4f}")
print(f"Caffeine log1p: W = {w_log:.4f}, p = {p_shapiro_log:.4f}")
print()
print("Spearman correlation (Caffeine vs Hours Played):")
print(f"rho = {rho_H2:.4f}, p = {p_H2:.4f}, N = {mask_h2.sum()} (hours_map applied)")
print(f"rho log1p = {rho_H2_log:.4f}, p_log = {p_H2_log:.4f}")

# -- Power Analysis for H1 --
# Convert Mann-Whitney r to Cohen's d approximation: d = 2r / sqrt(1 - r^2)
d_H1 = 2 * r_H1 / np.sqrt(1 - r_H1**2) if abs(r_H1) < 1 else np.nan
power_calc = TTestIndPower().power(effect_size=d_H1, nobs1=len(am_values), ratio=len(sp_values)/len(am_values), alpha=0.05)
print()
print(f"Power analysis H1: Cohen's d = {d_H1:.4f}, power = {power_calc:.4f}")

# -- Multiple Linear Regression on log-transformed caffeine intake --
print()
Y = np.log1p(df[col_cafe])
# Prepare predictors: experience level, gender, performance intention, hours played
X = pd.DataFrame({
    'Horas_Jogo': df_hours_num,
    'Perf_Intencao': df['MELHORAR_PERFORMANCE_MOTIVO_BIN'],
    'Nivel_Semi': (df[col_level] == 'Semi-Profissional').astype(int),
    'Nivel_Prof': (df[col_level] == 'Profissional').astype(int),
    'Genero_Fem': (df[col_gender] == 'Feminino').astype(int)
})
X = sm.add_constant(X)
model = sm.OLS(Y, X, missing='drop').fit()
print("Multiple linear regression on log(caffeine intake):")
print(model.summary()) 