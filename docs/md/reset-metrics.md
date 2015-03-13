How to clear the metrics to start from a clean copy. Typically, before the application goes live.

### Reset the metrics table
go to [the-app-domain-url]/delete/metrics
You’ll then be prompted to sign in as an administrator for the deletion to occur.

### Amend the starting month for the metrics page
In metrics-sparql.js amend the date at the top of the file to the date for which you would like the metrics to start displaying data: (format should stay consistent: ‘YYYY-MM’)
```python
var START_DATE = "2014-11";
```
