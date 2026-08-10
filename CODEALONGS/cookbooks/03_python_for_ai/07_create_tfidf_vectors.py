# Create TF-IDF vectors
from sklearn.feature_extraction.text import TfidfVectorizer

sentences = ["Keep minimum cash.", "Limit concentration.", "Require human confirmation."]
vectors = TfidfVectorizer().fit_transform(sentences)
print(vectors.shape)

