from flask import Flask, render_template, request
import numpy as np
import pickle

chunk_files = ['book_0.pkl','book_1.pkl','book_2.pkl','book_3.pkl']

# List to store all loaded chunks
all_chunks = []
# Load each chunk and append its data to `all_chunks`
for chunk_file in chunk_files:
    with open(chunk_file, 'rb') as file:
        chunk_data = pickle.load(file)
        all_chunks.extend(chunk_data)  # Extend by chunk data

books = all_chunks


#books = pickle.load(open('book.pkl', 'rb'))
popular = pickle.load(open('popular1.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
pivot = pickle.load(open('pivot_table.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')


def index():

    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_ratings'].values),
                           rating=list(popular['avg_ratings'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pivot.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

