"""
run_pipeline.py
Run the full pipeline end to end.
Usage: python run_pipeline.py
"""
import subprocess, sys

scripts = [
    "scripts/fetch_trends.py",
    "scripts/clean_data.py",
    "scripts/analyze_trends.py",
    "scripts/export_for_powerbi.py",
]

for script in scripts:
    print(f"\n{'='*50}")
    print(f"Running: {script}")
    print('='*50)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\n✗ Pipeline stopped at {script}")
        sys.exit(1)

print("\n Full pipeline complete. Check outputs/")