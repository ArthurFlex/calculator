import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher._mode_eax import EaxMode

def public():
    with open('pub_key.pem','r',encoding='utf-8') as public_key:
        file=public_key.read()
    file=file.encode("utf-8")
    return file

def private():
    with open('priv_key.bin','r',encoding='utf-8') as private_key:
        file=private_key.read()
    file=file.encode("utf-8")
    return file

def public_usual(pathway:str):
    pathway_new=os.path.join(pathway,"Keys","pub_key.pem")
    sys_files_decode(pathway_new)
    with open(pathway_new,'r',encoding='utf-8') as public_key:
        file=public_key.read()
    sys_files_encode(pathway_new)    
    bib=file.encode("utf-8")
    return bib

def private_usual(pathway:str):
    pathway_new=os.path.join(pathway,"Keys","priv_key.bin")
    sys_files_decode(pathway_new)
    with open(pathway_new,'r',encoding='utf-8') as private_key:
        file=private_key.read()
    sys_files_encode(pathway_new)     
    bib=file.encode("utf-8")
    return bib

def pass_check(hashed_password:str, user_password:str):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def pass_hash(password:str):
    salt ="butcherofblavicken"
    byte_salt=b"butcherofblavicken"
    return hashlib.sha256(byte_salt + password.encode('utf-8')).hexdigest() + ':' + salt


def usual_files_encode(pathway:str,name_file:str):
    data: bytes=b''
    with open(name_file,'rb') as file_lol:
        data=file_lol.read()
    with open(name_file, 'wb') as file_out:

        recipient_key = RSA.import_key(
            public_usual(pathway)
        )
        session_key = get_random_bytes(16)

        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        file_out.write(cipher_rsa.encrypt(session_key))

        cipher_aes: EaxMode = AES.new(session_key, AES.MODE_EAX)# type: ignore
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
   
        file_out.write(cipher_aes.nonce)
        file_out.write(tag)
        file_out.write(ciphertext)


def sys_files_encode(name_file:str):
    data:bytes=b''
    with open(name_file,'rb') as file_lol:
        data=file_lol.read()
    with open(name_file, 'wb') as file_out:
        recipient_key = RSA.import_key(
            public()
            )
   
        session_key = get_random_bytes(16)
   
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        file_out.write(cipher_rsa.encrypt(session_key))

        cipher_aes: EaxMode = AES.new(session_key, AES.MODE_EAX)# type: ignore
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
   
        file_out.write(cipher_aes.nonce)
        file_out.write(tag)
        file_out.write(ciphertext)


def gen_keys(login:str,pathway:str):
    code = 'booooooobs'
    key = RSA.generate(1024)

    encrypted_key = key.exportKey(
        passphrase=code, 
        pkcs=8, 
        protection="scryptAndAES128-CBC"
    )
    
    with open(os.path.join(pathway,'priv_key.bin'), 'wb') as key_file: 
        key_file.write(encrypted_key)
    sys_files_encode(os.path.join(pathway,'priv_key.bin')) 
    with open(os.path.join(pathway,'pub_key.pem'), 'wb') as key_file:
        key_file.write(key.publickey().exportKey())
    sys_files_encode(os.path.join(pathway,'pub_key.pem')) 


def usual_files_decode(pathway:str,name_file:str):
    code = 'booooooobs'
    with open(name_file, 'rb') as boom:
        private_key = RSA.import_key(
            private_usual(pathway),
             passphrase=code
         )
        
        enc_session_key, nonce, tag, ciphertext = [
            boom.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
        ]
      
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes: EaxMode = AES.new(session_key, AES.MODE_EAX,nonce)# type: ignore
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    with open(name_file,'wb') as file_out:
        file_out.write(data)


def sys_files_decode(name_file:str):
    code = 'booooooobs'
    with open(name_file, 'rb') as boom:
        private_key = RSA.import_key(
            private(),
             passphrase=code
         )
        
        enc_session_key, nonce, tag, ciphertext = [
            boom.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
        ]
      
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes: EaxMode = AES.new(session_key, AES.MODE_EAX,nonce)# type: ignore
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    with open(name_file,'wb') as file_out:
        file_out.write(data)