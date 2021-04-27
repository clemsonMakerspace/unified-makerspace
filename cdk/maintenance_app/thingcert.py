
def create_key(KeyName):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography import x509
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, str(KeyName))])
    ).sign(key, hashes.SHA256(), default_backend())

    KEY_TEXT = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
    ).decode("UTF-8")
    CSR_TEXT = csr.public_bytes(serialization.Encoding.PEM).decode("UTF-8")

    return KEY_TEXT, CSR_TEXT

def createThing(self, ThingNum, CUmakeit_IoT_Policy):
    from aws_cdk import (
        core,
        aws_iot as iot,
        aws_secretsmanager as secrets
    )

    thingName = "CUmakeit_" + ThingNum
    key_cert_name = thingName + "_IoT_Key_Cert"
    cert_name = thingName + "_Cert"
    cert_attachment_ID = thingName + "CertificateAttachment"
    policy_attachment_ID = thingName + "PolicyAttachment"
    private_key_name = "PrivateKey" + thingName
    certificate_secrets_name = "Certificate" + thingName

    key, csr = create_key(key_cert_name)

    thing = iot.CfnThing(self, thingName, thing_name=thingName)

    # Create cert
    cert = iot.CfnCertificate(self, cert_name, certificate_signing_request=csr, status='ACTIVE')

    # Attach the Certificate to the Thing
    iot.CfnThingPrincipalAttachment(self, cert_attachment_ID, principal=cert.attr_arn, thing_name=thing.ref)

    # Attach the Policy to the Certificate
    iot.CfnPolicyPrincipalAttachment(self, policy_attachment_ID, principal=cert.attr_arn, policy_name=CUmakeit_IoT_Policy.ref)

    # Add to secrets manager
    private_key = secrets.CfnSecret(self, private_key_name, name=private_key_name, secret_string = key)

    certificate_secret = secrets.CfnSecret(self, certificate_secrets_name, name=certificate_secrets_name, secret_string=csr)

    # secret = secrets.CfnSecret(self, "PrivateKeySecretCUmakeit_01", secret_string=json.dumps({"certificateId": CUmakeit_01_Cert, "csr": csr, "privateKey": key}))

    core.CfnOutput(self, thingName + "_ID", value=thing.ref)
    core.CfnOutput(self, thingName+"Certificate_ID", value=cert.ref)
    core.CfnOutput(self, thingName+"PrivateKey", value=private_key.ref)
    core.CfnOutput(self, thingName+"Certificate", value=certificate_secret.ref)

    return thing, cert
