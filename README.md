# 📆 End-of-Life Product Tracker (`end_of_life.py`)

This Python script automates the retrieval of end-of-life (EOL) data for various popular software products using the public API from [endoflife.date](https://endoflife.date). It produces a structured CSV file with enriched information like human-readable dates and time calculations relative to the EOL.

## 🚀 What Does It Do?

- Queries release and EOL data for products like `apache`, `mysql`, `python`, `gitlab`, and more.
- Collects:
  - Released versions and their launch dates
  - End-of-life dates (if available)
  - Latest version info and release date
  - Human-readable time difference (e.g., “Ends in 2 years, 3 months” or “Ended Yesterday”)
- Exports all records to a `end_of_life.csv` file

## ⚙️ Requirements

- Python 3.x
- Dependencies:

```bash
pip install requests
```
(datetime and csv are part of Python’s standard library.)

## ▶️ How to Use

1. Clone the repository or copy the script into your project:

2. Run the script:

```bash
python3 end_of_life.py
```

A file named `end_of_life.csv` will be generated in your project directory with structured data, including versions, release dates, EOL information, and time calculations.


## 🔍 Products Checked

The following products are queried via the API:

```python
eol_products = [
  'apache', 'tomcat', 'docker-engine', 'elasticsearch',
  'gitlab', 'grafana', 'jenkins', 'mssqlserver', 'mongodb',
  'mysql', 'nginx', 'openssl', 'oracle-database', 'php',
  'postgresql', 'python', 'sonar'
]
```
You can customize this list by editing the `eol_products` array in the script.

## 🧾 Example Output

| mw     | version | released      | end_of_life                             | latest_version        |
|--------|---------|---------------|-----------------------------------------|------------------------|
| apache | 2.4     | (21 Feb 2012) | Ends in 1 year, 6 months (31 Dec 2026) | 2.4.59 (14 May 2024)  |
| python | 3.7     | (27 Jun 2018) | Ended 7 months ago (27 Sep 2023)       | 3.12 (02 Apr 2024)    |

## 📡 Data Source

This project uses data from the [endoflife.date API](https://endoflife.date/docs/api), a community-maintained resource tracking software lifecycles and support timelines.

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and distribute it.

