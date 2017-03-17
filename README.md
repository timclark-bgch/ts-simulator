# Time Series Simulator

This project generates large volumes of time series data for testing time series storage and retrieval.

## Data Format

Data is generated as comma separated records with a newline (\n) between each record.

A record looks like this:

```text
DEVICE_ID, TIMESTAMP, VALUE
```

For example:

```text
DEVICE_1,12340,-10.12
DEVICE_2,11057,234.53
DEVICE_2,10057,4.76
DEVICE_1,12498,-12.12
DEVICE_2,21056,87.6
```

This data file contains two records for DEVICE_1 and three records for DEVICE_2. Note that the records do not
occur in timestamp order.
