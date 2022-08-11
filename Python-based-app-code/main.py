import os
from flask import Flask
from pymongo import MongoClient
from flask_restplus import Api, fields, Resource
## for password cryptography encryption
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def create_cipher_engine():
    """
    Methods to support the encryption and decryption of data.
    Create the cipher details to use.
    :param self:
    :param unencrypted:
    :return:
    """
    key = b'\xef|x\x9e\xf7#\xda\x84^d\xb0\x86:G\x0e\x9e\x7f<\x97\x13~\xc7Z\xcd7\x17\x10\x8c\x05Z\xa9\x80'
    iv = b'\x98\x02^_\x88H\x80\x81\xf3N\x0f\xbf Z<\xd7'
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Take the plain text string and return the encrypted version as a hex string value.
    # As we are using 128-bit encryption the plain text given is padded out to a multiple
    # of 16 bytes before being encrypted.


def encrypt(unencrypted):
    """
    Take the plain text string and return the encrypted version as a hex string value.
    As we are using 128-bit encryption the plain text given is padded out to a multiple
    of 16 bytes before being encrypted.
    :param self:
    :param unencrypted:
    :return:
    """
    if unencrypted and len(unencrypted) > 0:
        engine = cipher_engine.encryptor()
        padding = PKCS7(128).padder()
        padded = padding.update(unencrypted.encode()) + padding.finalize()
        return (engine.update(padded) + engine.finalize()).hex()

    return unencrypted


def decrypt(encrypted):
    """
    Decode the encrypted hex string string and return the results with the previous encryption
    padding removed.
    :param self:
    :param unencrypted:
    :return:
    """
    if encrypted and len(encrypted) > 0:
        engine = cipher_engine.decryptor()
        padded = engine.update(bytearray.fromhex(encrypted)) + engine.finalize()
        padding = PKCS7(128).unpadder()
        un_padded = padding.update(padded) + padding.finalize()
        return un_padded.decode()

    return encrypted


cipher_engine = create_cipher_engine()
# cryptography entries end here

# mongodb connector and cred details
mongo_client = MongoClient("mongodb://{LB IP of the mongodb svc}:{27017}/".format("mongo_host", 27017))
db_connector = mongo_client.get_database("mongo_database")
db_connector.authenticate(os.environ["mongo_user"], decrypt(os.environ["mongo_password"]))

app = Flask(__flask-app__)
api = Api(app)
population_model = api.model('City Population', {'Population': fields.String('City Poplulation')})

# health check end point
@api.route('/health', methods=['GET'])
class Health(Resource):
    def get(self):
        return "OK"

# get, query, update API calls end point listening from front end application
@api.route('/population/<key>', methods=['GET', 'POST', 'PUT'])
class Population(Resource):
    @api.expect(population_model)
    def post(self, key):
        db_connector["Population"].update({"name": key}, {"$set": api.payload}, upsert=True)
        # print(api.payload)
        return True

    def get(self, key):
        return db_connector["Population"].find({"name": key})[0]
        # print(key)
        # return 20

    @api.expect(population_model)
    def put(self, key):
        db_connector["Population"].update({"name": key}, {"$set": api.payload}, upsert=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
