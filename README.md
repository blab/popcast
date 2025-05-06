# popcast: Long-term forecasts for pathogen populations

See the methods of [Huddleston et al. 2020](https://doi.org/10.7554/eLife.60067) for more details or to cite this tool.

## Install

For a full installation with the OpenCV package that's required for model fitting, specify the "full" package dependencies.

``` bash
python -m pip install 'popcast[full]'
```

For a smaller installation that only supports forecasting with an existing model, omit the optional package dependency.

``` bash
python -m pip install popcast
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
python -m pip install '.[full,test]'
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
python -m pip install --upgrade build twine
```

Build the distribution packages.

``` bash
python -m build
```

Upload the distribution packages.

``` bash
python -m twine upload dist/*
```
