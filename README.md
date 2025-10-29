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

### 3rd Commit

### 4th Commit

### 5th Commit