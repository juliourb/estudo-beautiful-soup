.PHONY: install test test-unit test-cli run-sample

install:
	python -m pip install -e .

test: test-unit test-cli

test-unit:
	python -m pytest -q

test-cli:
	python -m src.main --help

run-sample:
	python -m src.main \
		--city "São Paulo - SP" \
		--min-rent 1200 \
		--max-rent 4000 \
		--max-pages-per-site 1 \
		--max-records 30 \
		--output-csv output/imoveis_sample.csv \
		--checkpoint output/checkpoint_sample.json
