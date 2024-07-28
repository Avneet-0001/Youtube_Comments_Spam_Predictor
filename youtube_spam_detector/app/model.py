import pickle

# Assuming `clf` is your trained model and `count_vect` is your vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(random_forest_best, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(count_vect, f)
