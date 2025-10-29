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

### 4th Commit

### 5th Commit