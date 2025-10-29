from flask import Flask, render_template_string, request, send_file
import os
import csv

try:
	import pandas as pd
except Exception:
	pd = None

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
			  <li><a href="/table">View table (default: last 200 rows)</a></li>
			  <li><a href="/table?limit=50">View last 50 rows</a></li>
			  <li><a href="/download">Download raw CSV</a></li>
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
		except Exception:
			# fallback to simple read if parsing fails
			df = pd.read_csv(path)

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


if __name__ == '__main__':
	# Development server. On Windows run: python app/data.py
	app.run(debug=True, host='0.0.0.0', port=5000)

