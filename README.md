## West Java Occupation Data Model

This project is a [dbt (data build tool)](https://www.getdbt.com/) implementation designed to model and analyze population occupation data in West Java, Indonesia.

### Project Overview

- **Project Name**: West Java Occupation Data Model  
- **Tool**: dbt (Data Build Tool)  
- **Language**: Python (for data extraction)

### Data Source

The data is sourced from the official West Java open data portal:

> [Population by Occupation Group and Gender in West Java](https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-kelompok-pekerjaan-dan-jenis-kelamin-di-jawa-barat)

### Workflow

1. **Extract & Load**  
   Use `get_data.py` to download and load the raw data into the database.

2. **Transform (with dbt)**  
   Several models have been created within the dbt project to:
   - Create data marts
   - Perform validations with data tests
   - Monitor freshness
   - Generate rich documentation
  
3. Build model
   - Use `dbt source freshness && dbt build` to check data freshness and build data model. 
