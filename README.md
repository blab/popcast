# popcast: Long-term forecasts for pathogen populations

## Install

``` bash
python3 -m pip install popcast
```

## Usage

Download seasonal influenza A/H3N2 data for model fitting.

``` bash
curl -LO "https://github.com/blab/flu-forecasting/raw/master/results/builds/natural/natural_sample_1_with_90_vpm_sliding/tip_attributes_with_weighted_distances.tsv"
```

Fit a model using default 6 year training windows and 12-month forecasts.

``` bash
popcast fit \
  --tip-attributes tip_attributes_with_weighted_distances.tsv \
  --output lbi_model.json \
  --predictors lbi
```

## Development

### Install locally

``` bash
python3 -m pip install .[test]
```

### Lint and run tests

Lint code.

``` bash
flake8 . --count --show-source --statistics
```

Run tests.

``` bash
cram --shell=/bin/bash tests/
```

### Publish

Install or upgrade publishing tools.

``` bash
python3 -m pip install --upgrade build twine
```

Build the distribution packages.

``` bash
python3 -m build
```

Upload the distribution packages.

``` bash
python3 -m twine upload dist/*
```
