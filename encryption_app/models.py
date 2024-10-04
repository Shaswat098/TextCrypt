from django.db import models
from cryptography.fernet import Fernet
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA, ECC
from Crypto.Random import get_random_bytes
import base64

class EncryptedMessage(models.Model):
    message = models.TextField()
    encrypted_message = models.TextField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    encryption_type = models.CharField(max_length=10, choices=[('AES', 'AES'), ('Fernet', 'Fernet'), ('RSA', 'RSA'), ('ECC', 'ECC')])

    def save(self, *args, **kwargs):
        if self.encryption_type == 'AES':
            key = get_random_bytes(16)  # AES key must be either 16, 24, or 32 bytes long
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(self.message.encode())
            self.encrypted_message = base64.b64encode(nonce + ciphertext).decode()  # Store as string
            self.key = base64.b64encode(key).decode()  # Store key as base64 string

        elif self.encryption_type == 'Fernet':
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            self.encrypted_message = cipher_suite.encrypt(self.message.encode()).decode()  # Store as string
            self.key = key.decode()  # Store key as string

        elif self.encryption_type == 'RSA':
            # Generate RSA key pair
            key = RSA.generate(2048)
            self.private_key = base64.b64encode(key.export_key()).decode()  # Store private key as string
            self.public_key = base64.b64encode(key.publickey().export_key()).decode()  # Store public key as string

            # Encrypt the message with AES
            aes_key = get_random_bytes(16)
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            nonce = cipher_aes.nonce
            ciphertext, tag = cipher_aes.encrypt_and_digest(self.message.encode())
            self.encrypted_message = base64.b64encode(nonce + ciphertext).decode()  # Store as string

            # Encrypt the AES key with the RSA public key
            cipher_rsa = PKCS1_OAEP.new(key.publickey())
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            self.key = base64.b64encode(encrypted_aes_key).decode()  # Store encrypted AES key as string

        elif self.encryption_type == 'ECC':
            # Generate ECC key pair
            key = ECC.generate(curve='P-256')
            public_key = key.public_key()
            self.key = key.export_key(format='PEM').decode()  # Store the private key as PEM string

            # Encrypt the message with AES
            aes_key = get_random_bytes(16)
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            nonce = cipher_aes.nonce
            ciphertext, tag = cipher_aes.encrypt_and_digest(self.message.encode())
            self.encrypted_message = base64.b64encode(nonce + ciphertext).decode()  # Store as string

            # Encrypt the AES key with ECC public key
            cipher_ecc = PKCS1_OAEP.new(public_key)
            encrypted_aes_key = cipher_ecc.encrypt(aes_key)
            self.key = base64.b64encode(encrypted_aes_key).decode()  # Store encrypted AES key as string

        super().save(*args, **kwargs)

    def decrypt(self):
        if self.encryption_type == 'AES':
            key = base64.b64decode(self.key.encode())  # Decode from base64 to bytes
            encrypted_data = base64.b64decode(self.encrypted_message.encode())  # Decode from base64 to bytes
            nonce = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt(ciphertext).decode()  # Return the decrypted message as string

        elif self.encryption_type == 'Fernet':
            key = self.key.encode()  # Convert to bytes
            cipher_suite = Fernet(key)
            return cipher_suite.decrypt(self.encrypted_message.encode()).decode()  # Return decrypted message

        elif self.encryption_type == 'RSA':
            key = RSA.import_key(base64.b64decode(self.key.encode()))  # Decode and use the stored key
            cipher = PKCS1_OAEP.new(key)
            encrypted_data = base64.b64decode(self.encrypted_message)
            return cipher.decrypt(encrypted_data).decode()  # Return decrypted message

        # elif self.encryption_type == 'ECC':
        #     private_key = ECC.import_key(self.key)  # Import the stored private key
        #     cipher_ecc = PKCS1_OAEP.new(private_key)  # Assuming ECC decryption is similar to RSA for demonstration
        #     encrypted_data = base64.b64decode(self.encrypted_message)
        #     return cipher_ecc.decrypt(encrypted_data).decode()  # Return decrypted message
