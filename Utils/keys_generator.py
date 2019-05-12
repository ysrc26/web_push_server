from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1, default_backend())
    # public_key = private_key.public_key()
    private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    # public_key = public_key.public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PublicFormat.SubjectPublicKeyInfo
    # )

    # return private_key, public_key
    return private_key

# priv, pub, = generate_keys()
# print "private: {0}\npublic: {1}".format(priv, pub)
