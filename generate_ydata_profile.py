from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

data_path = Path(__file__).parent / "Data_set_prep_assignment_1.csv"
df = pd.read_csv(data_path, low_memory=False)
df = df.drop_duplicates().reset_index(drop=True)

group_means = df.groupby("ReproductionStatus")["Avgmilkflow"].transform("mean")
group_stds = df.groupby("ReproductionStatus")["Avgmilkflow"].transform("std")
outlier_mask = (
    df["ReproductionStatus"].notna()
    & (((df["Avgmilkflow"] - group_means) / group_stds).abs() > 3)
)
df = df.loc[~outlier_mask].copy()

profile_sample = df.sample(n=min(100_000, len(df)), random_state=42)
profile_path = data_path.parent / "project_1_ydata_profile.html"
profile_report = ProfileReport(
    profile_sample,
    title="Project 1 ANSC 4040 Data Profile",
    minimal=True,
)
profile_report.to_file(profile_path)

print(f"Profiled rows: {len(profile_sample):,}")
print(f"Saved: {profile_path}")