from flask import Flask, render_template_string, request, send_file
import os
import csv
import base64
from io import BytesIO

try:
	import pandas as pd
except Exception:
	pd = None

try:
	import matplotlib.pyplot as plt
except Exception:
	plt = None

app = Flask(__name__)


def data_file_path():
	# f.us.txt is stored in the workspace root (parent of this app/ folder)
	base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	return os.path.join(base_dir, 'f.us.txt')


@app.route('/')
def index():
	return render_template_string(
		'''
		<!doctype html>
		<html>
		<head>
		  <meta charset="utf-8">
		  <title>Data viewer</title>
		  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
		</head>
		<body class="p-4">
		  <div class="container">
			<h1>CSV Data Viewer</h1>
			<p>This small app serves <code>f.us.txt</code> as an HTML table.</p>
			<ul>
			  <li><strong>Time Periods:</strong></li>
			  <li><a href="/table?period=1">Period 1: 1977-1992</a></li>
			  <li><a href="/table?period=2">Period 2: 1993-2008</a></li>
			  <li><a href="/table?period=3">Period 3: 2009-2025</a> (default)</li>
			  <li><strong>View Options:</strong></li>
			  <li><a href="/table">View table (default: last 200 rows)</a></li>
			  <li><a href="/table?limit=50">View last 50 rows</a></li>
			  <li><a href="/download">Download raw CSV</a></li>
			  <li><a href="/volume-chart">Average monthly volume chart</a></li>
			</ul>
		  </div>
		</body>
		</html>
		'''
	)


@app.route('/table')
def table():
	"""Return the CSV as an HTML table. Optional query param `limit` (int) returns only the last N rows."""
	path = data_file_path()
	if not os.path.exists(path):
		return f"Data file not found at {path}", 404

	limit = request.args.get('limit', default=None, type=int)

	if pd is not None:
		# Use pandas when available for convenience and speed
		try:
			df = pd.read_csv(path, parse_dates=['Date'], infer_datetime_format=True)
			# Drop OpenInt column as it's not needed
			df = df.drop('OpenInt', axis=1)
			
			# Split into three periods
			period1 = df[df['Date'] < '1993-01-01'].copy()
			period2 = df[(df['Date'] >= '1993-01-01') & (df['Date'] < '2009-01-01')].copy()
			period3 = df[df['Date'] >= '2009-01-01'].copy()
			
			# Get requested period from query param (default to latest)
			period = request.args.get('period', default='3', type=str)
			if period == '1':
				df = period1
			elif period == '2':
				df = period2
			else:
				df = period3
		except Exception:
			# fallback to simple read if parsing fails
			df = pd.read_csv(path)
			df = df.drop('OpenInt', axis=1)

		if limit:
			df = df.tail(limit)
		else:
			# default to showing last 200 rows to avoid huge pages
			df = df.tail(200)

		table_html = df.to_html(classes="table table-striped table-sm", index=False, justify='center', border=0)
	else:
		# Lightweight fallback that does not require pandas
		with open(path, newline='', encoding='utf-8') as f:
			reader = csv.reader(f)
			rows = list(reader)

		if not rows:
			return "Empty data file", 204

		header = rows[0]
		body = rows[1:]
		if limit:
			body = body[-limit:]
		else:
			body = body[-200:]

		# build simple HTML table
		parts = ["<table class='table table-striped table-sm'>"]
		parts.append('<thead><tr>')
		for col in header:
			parts.append(f"<th>{col}</th>")
		parts.append('</tr></thead>')
		parts.append('<tbody>')
		for r in body:
			parts.append('<tr>')
			for c in r:
				parts.append(f"<td>{c}</td>")
			parts.append('</tr>')
		parts.append('</tbody></table>')
		table_html = '\n'.join(parts)

	# Render inside a small page with Bootstrap
	return render_template_string(
		'''
		<!doctype html>
		<html>
		<head>
		  <meta charset="utf-8">
		  <title>CSV Table</title>
		  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
		</head>
		<body class="p-4">
		  <div class="container">
			<h1>f.us.txt — Table view</h1>
			<p>Showing last {{shown_rows}} rows. <a href="/download">Download CSV</a></p>
			<div class="table-responsive">{{table|safe}}</div>
			<p class="mt-3"><a href="/">Back</a></p>
		  </div>
		</body>
		</html>
		''',
		table=table_html,
		shown_rows=(limit or 200)
	)


@app.route('/download')
def download():
	path = data_file_path()
	if not os.path.exists(path):
		return f"Data file not found at {path}", 404
	return send_file(path, as_attachment=True)


@app.route('/volume-chart')
def volume_chart():
	"""Compute average monthly volume for each of the three periods and return a PNG bar chart embedded in HTML.
	Requires pandas and matplotlib to be installed.
	Query params:
	 - period: optional, if set to 1/2/3 will show only that period's monthly series and value (not used here)
	"""
	path = data_file_path()
	if not os.path.exists(path):
		return f"Data file not found at {path}", 404

	if pd is None:
		return (
			"This visualization requires pandas. Install it with: pip install pandas",
			400,
		)

	if plt is None:
		return (
			"This visualization requires matplotlib. Install it with: pip install matplotlib",
			400,
		)

	# load data
	df = pd.read_csv(path, parse_dates=['Date'], infer_datetime_format=True)
	# drop OpenInt if present
	df = df.drop('OpenInt', axis=1, errors='ignore')
	# ensure Date is datetime
	df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
	df = df.dropna(subset=['Date'])

	# define periods
	period1 = df[df['Date'] < '1993-01-01']
	period2 = df[(df['Date'] >= '1993-01-01') & (df['Date'] < '2009-01-01')]
	period3 = df[df['Date'] >= '2009-01-01']

	def avg_monthly_volume(period_df):
		if period_df.empty:
			return 0
		# sum volume per month then average those monthly totals
		monthly = period_df.set_index('Date').resample('M')['Volume'].sum()
		return float(monthly.mean())

	vals = [
		avg_monthly_volume(period1),
		avg_monthly_volume(period2),
		avg_monthly_volume(period3),
	]
	labels = ['1977-1992', '1993-2008', '2009-2025']

	# build chart
	fig, ax = plt.subplots(figsize=(8, 4))
	colors = ['#4c72b0', '#55a868', '#c44e52']
	ax.bar(labels, vals, color=colors)
	ax.set_ylabel('Average Monthly Volume')
	ax.set_title('Average Monthly Volume by Period')
	# annotate values
	for i, v in enumerate(vals):
		ax.text(i, v, f"{int(round(v)):,}", ha='center', va='bottom')

	buf = BytesIO()
	plt.tight_layout()
	fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
	plt.close(fig)
	buf.seek(0)
	img_b64 = base64.b64encode(buf.getvalue()).decode('ascii')

	# render simple html with embedded image
	return render_template_string(
		'''
		<!doctype html>
		<html>
		<head>
		  <meta charset="utf-8">
		  <title>Average Monthly Volume Chart</title>
		  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
		</head>
		<body class="p-4">
		  <div class="container">
			<h1>Average Monthly Volume by Period</h1>
			<p>Bar chart shows average total monthly volume for each historical period.</p>
			<img src="data:image/png;base64,{{img}}" alt="volume chart" class="img-fluid" />
			<p class="mt-3"><a href="/">Back</a></p>
		  </div>
		</body>
		</html>
		''',
		img=img_b64,
	)


if __name__ == '__main__':
	# Development server. On Windows run: python app/data.py
	app.run(debug=True, host='0.0.0.0', port=5000)

