from flask import Flask, json, request
import waitress
import sqlite3

high_score_list = [{"id": 1, "name": "mike", "score": 69}, {"id": 2, "name": "donut", "score": 420}, {"id": 3, "name": "john", "score": 88}]

api = Flask(__name__)

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

@api.route('/get_scores', methods=['GET'])
def get_scores():

    con = sqlite3.connect("scoresdb.db")
    con.row_factory = dict_factory
    db = con.cursor()

    data = db.execute("SELECT * FROM Scores ORDER BY score DESC")

    allrows = data.fetchall()

    print(allrows)

    return json.dumps(allrows)


@api.route('/get_highscore', methods=['GET'])
def get_highscore():

    con = sqlite3.connect("scoresdb.db")
    con.row_factory = dict_factory
    db = con.cursor()

    data = db.execute("SELECT name, MAX(score) FROM Scores")


    #return json.dumps(data.fetchall()) # works, but let's just return one row instead of array
    return json.dumps(data.fetchone())


@api.route('/put_score', methods=['PUT'])
def put_score():

    con = sqlite3.connect("scoresdb.db")
    con.row_factory = dict_factory
    db = con.cursor()

    #print(request.mimetype)

    #print(request.get_data())

    data = request.get_json()

    print(data)

    #high_score_list.append(data)

    #print(high_score_list)

    print(list(data.values()))

    db.execute("INSERT INTO Scores (name, score) VALUES (?, ?)", list(data.values()))
    #db.execute("INSERT INTO Scores VALUES (?, ?, ?)", list(data.values())) # the question is whether or not this actually
    # keeps the keys / values ordered properly when transmitted. I would much rather know that my data is being mapped
    # correctly. Perhaps make a function that takes the metadata of the table, and then with the dictionary outputs just
    # a list of the VALUES of that dictionary in the order of the metadata to be safe.

    con.commit()

    return json.dumps(db.execute("SELECT * FROM Scores").fetchall())



if __name__ == '__main__':
    #api.run('10.0.0.8', '8000')
    waitress.serve(api, host="0.0.0.0", port=8080)