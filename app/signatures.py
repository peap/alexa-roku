"""
Check signatures of incoming requests, to ensure they come from Alexa.

See: https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/
     docs/developing-an-alexa-skill-as-a-web-service
     #verifying-the-signature-certificate-url
"""
from base64 import b64decode
from urllib.parse import urlparse

import requests
from OpenSSL import crypto
from url_normalize import url_normalize


def cert_chain_url_valid(cert_url):
    """
    Ensure that the provided URL for the certificate chain is valid, by checking that:
    * it's HTTPS
    * the host is s3.amazonaws.com
    * the port, if specified, is 443
    * the path starts with '/echo.api/'
    """
    normalized = url_normalize(cert_url)
    parsed = urlparse(normalized)
    url_checks = {
        'scheme': parsed.scheme == 'https',
        'hostname': parsed.hostname == 's3.amazonaws.com',
        'port': parsed.port in (443, None),
        'path': parsed.path.startswith('/echo.api/'),
    }
    all_checks_pass = all(url_checks.values())
    return all_checks_pass


def parse_certificate(cert_url):
    """Get, parse, and return the PEM certificate at the given URL."""
    normalized_url = url_normalize(cert_url)
    cert_request = requests.get(normalized_url)
    cert_text = cert_request.text
    return cert_text


def signature_valid(signature, cert_text, data):
    """Verify signature against certificate text and signed data."""
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_text)
    decoded_signature = b64decode(signature)
    try:
        result = crypto.verify(certificate, decoded_signature, data, 'sha1')
    except crypto.Error:
        return False
    return result is None
