import qrcode
from getpass import getpass
import base64
import re

def is_valid_base32(secret):
    """Validate if the input is a valid Base32 string."""
    # Remove spaces and convert to uppercase for consistency
    secret = secret.replace(" ", "").upper()
    # Check if the string contains only valid Base32 characters (A-Z, 2-7)
    if not re.match(r'^[A-Z2-7]+$', secret):
        return False
    # Base32 strings must have valid lengths (multiple of 8 bits when decoded)
    valid_lengths = {16, 26, 32, 52, 64}  # Common lengths for MFA keys
    if len(secret) not in valid_lengths:
        return False
    # Attempt to decode the Base32 string
    try:
        # Pad with '=' if necessary (Base32 requires length multiple of 8)
        padded_secret = secret + '=' * ((8 - len(secret) % 8) % 8)
        base64.b32decode(padded_secret)
        return True
    except Exception:
        return False
# Prompt user for input
label = input("Enter the account name (e.g., Facebook, YouTube...): ")
secret = getpass("Enter the MFA secret key (input is hidden): ")
issuer = input("Enter the issuer (Optional, press Enter to skip): ")
# Remove spaces from the secret key
secret = secret.replace(" ", "")
# Validate the secret key
if not is_valid_base32(secret):
    print("Error: Invalid Base32 secret key. Use only A-Z and 2-7, with valid length (e.g., 16, 26, 32 characters).")
    exit(1)
# Create the otpauth URL
if issuer:
    otpauth_url = f"otpauth://totp/{label}?secret={secret}&issuer={issuer}"
else:
    otpauth_url = f"otpauth://totp/{label}?secret={secret}"
# Create a QR code
qr = qrcode.QRCode(version=1, box_size=2, border=4)
qr.add_data(otpauth_url)
qr.make(fit=True)
# Print the QR code as ASCII art in the terminal
qr.print_ascii()
# Optional: Save the QR code as an image
save_image = input("Do you want to save the QR code as a PNG file? (y/n): ").lower()
if save_image == 'y':
    img = qr.make_image(fill="black", back_color="white")
    img.save("mfa_qrcode.png")
    print("QR code saved as mfa_qrcode.png")
