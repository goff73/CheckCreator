from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from num2words import num2words
from faker import Faker

# Constants
TEMPLATE_PATH = "check_template.png"
FONT_PATH = "Sedan-Regular.ttf"
CURSIVE_FONT_PATH = "DancingScript-Bold.ttf"
FONT_SIZE = 20
CURSIVE_FONT_SIZE = 30

# Text positions
CHECK_NUMBER_POSITION = (680, 30)
AMOUNT_POSITION = (600, 135)
PAYEE_NAME_POSITION = (130, 135)
ROUTING_NUMBER_POSITION = (100, 300)
ACCOUNT_NUMBER_POSITION = (400, 300)
CHECK_NUMBER_POSITION_BOTTOM = (680, 290)
DATE_POSITION = (510, 70)
SIGNATURE_POSITION = (520, 230)
DOLLARS_POSITION = (130, 190)

# Initialize Faker
fake = Faker()

def convert_amount_to_words(amount):
    dollars, cents = map(int, amount.split('.'))
    dollars_text = num2words(dollars).capitalize()  # Capitalize the first word
    cents_text = f"{cents:02d}/100"
    return f"{dollars_text} and {cents_text}"

def create_check_image(check_number, amount, payee_name, routing_number, account_number, date, signature):
    # Load the template image
    template_image = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(template_image)
    
    # Load fonts
    try:
        print(f"Attempting to load cursive font from: {CURSIVE_FONT_PATH}")
        cursive_font = ImageFont.truetype(CURSIVE_FONT_PATH, CURSIVE_FONT_SIZE)
        print("Fonts loaded successfully.")
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError as e:
        print(f"Font loading failed: {e}")
        font = ImageFont.load_default()
        cursive_font = ImageFont.load_default()
    
    # Convert amount to words
    amount_in_words = convert_amount_to_words(amount)

    # Draw text on the image
    draw.text(CHECK_NUMBER_POSITION, f"{check_number}", fill="black", font=font)
    draw.text(AMOUNT_POSITION, f"{amount}", fill="black", font=font)
    draw.text(PAYEE_NAME_POSITION, f"{payee_name}", fill="black", font=font)
    # Uncomment these lines if you want to include routing number, account number, and bottom check number
    # draw.text(ROUTING_NUMBER_POSITION, f"Routing No: {routing_number}", fill="black", font=font)
    # draw.text(ACCOUNT_NUMBER_POSITION, f"Account No: {account_number}", fill="black", font=font)
    # draw.text(CHECK_NUMBER_POSITION_BOTTOM, f"{check_number}", fill="black", font=font)
    draw.text(DATE_POSITION, f"{date}", fill="black", font=font)
    draw.text(SIGNATURE_POSITION, signature, fill="black", font=cursive_font)
    draw.text(DOLLARS_POSITION, amount_in_words, fill="black", font=font)
    
    # Save the image
    template_image.save(f"check_{check_number}.png")

# Example check data
check_data = [
    {"check_number": f"{i+100000}", "amount": f"{1500.00 + i}", "payee_name": fake.name(), 
     "routing_number": "123456789", "account_number": "987654321", "date": datetime.now().strftime("%m/%d/%Y"), 
     "signature": "Jane Smith"}
    for i in range(50)
]

# Generate checks
for check in check_data:
    create_check_image(check["check_number"], check["amount"], check["payee_name"], check["routing_number"], 
                       check["account_number"], check["date"], check["signature"])