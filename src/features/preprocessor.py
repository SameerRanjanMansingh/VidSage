from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


column_transformer = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['views', 'likes', 'dislikes', 'comment_count']),
        ('cat', OneHotEncoder(), ['channel_title', 'comments_disabled', 'ratings_disabled']),
        ('text', TfidfVectorizer(), 'title')
    ],
    remainder='drop'  # Drop the columns that are not specified
)
