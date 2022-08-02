# nextcast: Long-term forecasts for pathogen populations

## Usage

Download seasonal influenza A/H3N2 data for model fitting.

``` bash
curl "https://github.com/blab/flu-forecasting/raw/master/results/builds/natural/natural_sample_1_with_90_vpm_sliding/tip_attributes_with_weighted_distances.tsv" > tip_attributes_with_weighted_distances.tsv
```


Fit a model using default 6 year training windows and 12-month forecasts.

``` bash
    nextcast fit \
      --tip-attributes tip_attributes_with_weighted_distances.tsv \
      --output lbi_model.json \
      --predictors lbi
```
