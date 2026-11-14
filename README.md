# AiJobs

AiJobs is a Python application that recommends suitable job roles based on a user's interests, programming language, experience level, and city.

The project uses a machine learning model to make recommendations and can also search for matching job listings online and in a SQL Server database.

## Technologies

- Python
- Pandas
- Scikit-learn
- Joblib
- Microsoft SQL Server
- Rich

## How to run

1. Install the required Python packages:

```bash
pip install pandas scikit-learn joblib pyodbc rich googlesearch-python
```

2. Configure the SQL Server connection in `db.py`.
3. Make sure the database contains the required `UserProfiles` and `Jobs` tables.
4. If needed, train the model:

```bash
python train_model.py
```

5. Start the career assistant:

```bash
python AiJobs.py
```

The application asks a few questions, predicts a suitable job role, saves the profile, and displays matching job opportunities.