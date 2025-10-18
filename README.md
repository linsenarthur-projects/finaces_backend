📊 Finances Analysis

A personal finance analysis app that helps me track and visualize my expenses and income over time.
The app uses PostgreSQL as a database, processes transaction data exported from my bank, and provides dashboards and automation to simplify analysis.

pip install -r requirements.txt


⚠️ Currently built for KBC Bank Belgium (Flanders) CSV exports. Other banks may have different formats that require adjustments.

Step 1 - Data & Database <a id='fase_1'></a> (testing voor future wanneer grotere readme)
- [x] CSV extraction from banking app (set to montly CSV creation of all accounts)
- [x] PostgreSQL database setup
- [x] Data transformation & cleaning (jupter notebook)
- [x] Create script for schema & insertions

Step 2 - Backend & First Frontend
- [x] Refactor ETL scripts into backend logic (3 layer structure)
- [ ] CRUD for database changes                                                 -- NEXT STEP: want anders geen grafieken en tabellen
- [ ] Build a basic frontend for initial dashboards, analysis and backend logic
- [ ] Build graphs and tables of the data
- [ ] Dockerize first version (backend + DB + frontend)

Step 3 - Dashboard & Features
- [ ] improved front-end Quaser
- [ ] improved visualisation: charts.js 'https://www.chartjs.org/' | Echarts | Power BI dashboard implementation

- [ ] Enhance data exploration features
- [ ] Export analysis to PDF/Excel (csv) reports
- [ ] Dockerize second version

Step 4 - Automation & Deployment
- [ ] Automate monthly CSV processing (AI agent)
- [ ] Run as a service on Raspberry Pi 5
- [ ] Host dashboard on local network

Step 5 - ...
- [ ] ...

TODO
- [x] fix issue with date NaT in transaction
- [x] dubble check data in transactions if it actually is right:
        - zaken zoals automatic saving wordt er nog niet uitgehaald
- [ ] look into free & standard format for possible description of transaction table
- [ ] install fail save als aantal transacties inkomend niet overkomt met verwerkt dat deze bepaalde lijnen getoond/gelogd worden
- [x] alle inkomende transacties (desbetreffende accounts) checken of accounts al bestaan anders nieuwe aanmaken