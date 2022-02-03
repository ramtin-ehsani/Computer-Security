from base64 import b64encode, b64decode
import scrypt
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt(plainText, password):
    salt = get_random_bytes(AES.block_size)

    privateKey = scrypt.hash(
        password.encode(), salt=salt, N=2 ** 14, r=8, p=1, buflen=32)
    # cipher config
    cipherConfig = AES.new(privateKey, AES.MODE_GCM)
    # return encrypted text
    cipherText, tag = cipherConfig.encrypt_and_digest(bytes(plainText, 'utf-8'))
    return {
        'cipher_text': b64encode(cipherText).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipherConfig.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    salt = b64decode(enc_dict['salt'])
    nonce = b64decode(enc_dict['nonce'])
    cipherText = b64decode(enc_dict['cipher_text'])
    tag = b64decode(enc_dict['tag'])
    privateKey = scrypt.hash(
        password.encode(), salt=salt, N=2 ** 14, r=8, p=1, buflen=32)

    # cipher config
    cipher = AES.new(privateKey, AES.MODE_GCM, nonce=nonce)
    # decrypt
    decrypted = cipher.decrypt_and_verify(cipherText, tag)

    return decrypted


def main():
    password = input("Enter Password: ")
    # Encrypt
    text = "Secret message"
    encrypted = encrypt(text, password)
    print(encrypted)
    # Decrypt
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))


if __name__ == "__main__":
    main()
