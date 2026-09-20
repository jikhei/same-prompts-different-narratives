PYTHON ?= python3

.PHONY: verify reproduce analysis

verify:
	$(PYTHON) scripts/verify_release.py

reproduce: verify
	$(PYTHON) scripts/reproduce.py

analysis: reproduce
	mkdir -p outputs
	jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb --output analysis-executed.ipynb --output-dir outputs --ExecutePreprocessor.timeout=1800
