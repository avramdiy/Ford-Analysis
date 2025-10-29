# TRG Week 47

## $F (Ford Motor Company)

- A century-old American automaker based in Dearborn, Michigan, that designs, manufactures and sells cars, trucks, SUVs and commercial vehicles globally; historically dominant in combustion-engine vehicles and now investing heavily in electric vehicles and commercial mobility solutions while maintaining strong scale in pickup trucks (F-150) and commercial vans.

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

- Added a Flask web application (`app/data.py`) that serves the stock data as an HTML table:
  - Routes: Index (`/`), Table view (`/table`), and CSV download (`/download`)
  - Supports pagination via `limit` parameter (e.g., `/table?limit=50`)
  - Uses pandas for efficient data handling (with CSV fallback)
  - Includes Bootstrap styling for better presentation
  - Run locally with: `python app/data.py` (requires Flask; pandas optional)

### 2nd Commit

- Enhanced data analysis by splitting Ford's stock data into three distinct periods for better historical analysis:
  - Period 1 (1977-1992): Early data covering Ford's recovery from the 70s oil crisis through the late 80s boom
  - Period 2 (1993-2008): The SUV/truck boom years through the 2008 financial crisis
  - Period 3 (2009-2025): Post-crisis recovery and transition to EVs
- Technical changes:
  - Dropped 'OpenInt' (Open Interest) column as it contained no meaningful data (all zeros)
  - Added period selection via `?period=1|2|3` query parameter
  - Updated UI to show clear period navigation
  - Maintained existing pagination and download features

### 3rd Commit

- Added a visualization and API endpoint to compare average monthly trading volume across the three historical periods.
  - New Flask route: `/volume-chart` (in `app/data.py`) that computes average monthly volume for each period and returns an embedded PNG bar chart.
  - Implementation notes:
    - Requires `pandas` and `matplotlib` to run the chart (the app will return a friendly message if those packages are missing).
    - For each period, monthly totals are computed (sum of `Volume` per calendar month); the average of those monthly totals is plotted as a single bar per period.
    - Chart is annotated with formatted numbers for quick reading and styled simply with Bootstrap for the surrounding page.
  - Reasoning: comparing average monthly volumes by era highlights changes in market activity (liquidity) across Ford's long history and gives a concise, visual summary useful for both exploratory analysis and reporting.

### 4th Commit

### 5th Commit