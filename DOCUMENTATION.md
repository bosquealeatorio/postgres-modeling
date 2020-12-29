# Documentation 

## Dependencies

- Python 3+ distribution
- Conda package manager
- Postgres SQL Installation

## Usage

Clone the repository and locate on the root folder  
```
git clone https://github.com/manuel-montoya-gamio/postgres-modeling.git  
cd postgres-modeling
```

Create a virtual environment with the `environment.yml` file
```
conda env create -f environment.yml  
conda activate postgres-modeling
```   

Start Postgres with the following command 
```
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

Execute the scripts from the root folder postgres-modeling
```
python create_tables.py  
python etl.py
``` 

For the bulk inserts with copy-from execute the v2 files
```
python create_tables_v2.py  
python etl_v2.py
``` 

Validate the inserts using the notebooks `test.ipynb` and `test-validation.ipynb`
