# Yify Movies DB

So, I wanted to search for a nice movie with my own criteria, and I wanted to
use Yify as it is not just rates, but downloads as well.

I got a scraping script online ( can't remember from where ). Modified it, and
thought of keeping the data in github.

This data is Free to be used by any one

### Querying the data

I like to use Miller to manipulate CSV files quickly.


ex.

```
mlr --c2p cut -x -f '',Synopsis,Url then filter '$Downloads > 1000000' then sort -nr Rating then head -n 40 data_*.csv

```
