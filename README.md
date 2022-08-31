# popcast: Long-term forecasts for pathogen populations

## Install

Install [Flit](https://flit.pypa.io/en/latest/index.html).

``` bash
python3 -m pip install flit
```

Install popcast with the current environment's Python 3.

``` bash
flit install --python `which python3`
```

## Usage

Download seasonal influenza A/H3N2 data for model fitting.

``` bash
curl "https://github.com/blab/flu-forecasting/raw/master/results/builds/natural/natural_sample_1_with_90_vpm_sliding/tip_attributes_with_weighted_distances.tsv" > tip_attributes_with_weighted_distances.tsv
```

Fit a model using default 6 year training windows and 12-month forecasts.

``` bash
popcast fit \
  --tip-attributes tip_attributes_with_weighted_distances.tsv \
  --output lbi_model.json \
  --predictors lbi
```
