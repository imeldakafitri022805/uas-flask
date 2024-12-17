from flask import Flask, jsonify, make_response
from flask import request
from model import Data

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello():
    data = [{
        'nama': 'Galih',
        'pekerjaan': 'Web Engineer',
        'pesan': 'Hello World'
    }]
    return make_response(jsonify({'data': data}), 200)


@app.route('/karyawan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def karyawan():
    try:

        dt = Data()
        values = ()
        
        # Jika Method GET
        if request.method == 'GET':
           id_ = request.args.get('id')
           if id_:
               query = "SELECT * FROM data_karyawan where id = %s "
               values = (id_,)
           else:
               query = "SELECT * FROM data_karyawan"
           data = dt.get_data(query, values)    

        # Jika Method POST
        elif request.method == 'POST':
            datainput = request.json
            nama = datainput['nama']
            pekerjaan = datainput['pekerjaan']
            usia = datainput['usia']

            query = "INSERT INTO data_karyawan (nama, pekerjaan, usia) values (%s, %s, %s) "
            values = (nama, pekerjaan, usia)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil menambah data'
            }] 

        #Jika Method PUT
        elif request.method == 'PUT':
            query = "UPDATE data_karyawan SET id = %s "
            datainput = request.json
            id_ = datainput['id']
            values += (id_,)

            if 'nama' in datainput:
                nama = datainput['nama']
                values += (nama, )
                query += ", nama = %s"
            if 'pekerjaan' in datainput:
                pekerjaan = datainput['pekerjaan']
                values += (pekerjaan, )
                query += ", pekerjaan = %s"
            if 'usia' in datainput:
                usia = datainput['usia']
                values += (usia, )
                query += ", usia = %s"

            query += "where id = %s "
            values += (id_,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil mengubah data'
            }]
        # selain itu ada DELETE, Bila ada method selain keempat ini maka akan langsung error karenamethod tidak assign 
        else :
            query = "DELETE FROM data_karyawan where id = %s "
            id_ = request.args.get("id")
            values = (id_,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil menghapus data'
            }]
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)
    return make_response(jsonify({'data': data}), 200)

app.run()