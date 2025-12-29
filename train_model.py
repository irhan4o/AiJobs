from db import get_connection
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib


def load_data_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT MainInterest, Lang, ExpLevel, City, RecommendedRole
        FROM UserProfiles
        WHERE RecommendedRole IS NOT NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame.from_records(rows, columns=columns)
    conn.close()
    return df


def train_and_save_model():
    df = load_data_from_db()
    print(f"Заредени {len(df)} записа от UserProfiles")
    
    if df.empty:
        print("Няма данни за обучение. Попълни повече профили!")
        return

    X = df[["MainInterest", "Lang", "ExpLevel", "City"]]
    y = df["RecommendedRole"]

    print("Примерни данни:")
    print(X.head())
    print("\nЦели (роли):")
    print(y.value_counts())

    categorical_features = ["MainInterest", "Lang", "ExpLevel", "City"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ]
    )

    clf = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=1000)),  # ← без multi_class
    ]
)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf.fit(X_train, y_train)

    train_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)
    
    print(f"\nТочност на обучението: {train_accuracy:.2f}")
    print(f"Точност на теста: {test_accuracy:.2f}")

    joblib.dump(clf, "role_model.joblib")
    print("✅ Моделът е записан в role_model.joblib")


if __name__ == "__main__":
    train_and_save_model()
