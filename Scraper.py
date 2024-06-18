import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Ange sökvägen till din ChromeDriver
chrome_driver_path = r"C:/Users/saali/OneDrive/Skrivbord/chromedriver-win32/chromedriver.exe"

# Starta webbläsaren
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Navigera till Zalando-sidan för herrskor
driver.get("https://www.zalando.se/herrskor/")

# Vänta några sekunder för att säkerställa att sidan har laddats helt
time.sleep(10)  # Vänta 10 sekunder för att låta sidan ladda helt

# Hitta alla produktkort
product_cards = driver.find_elements(By.CSS_SELECTOR, "div[class^='cat_articleCard-']")

print(f"Hittade {len(product_cards)} produktkort")

# Öppna en CSV-fil för att skriva resultaten
with open('zalando_skor_under_700.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Definiera kolumnnamnen
    fieldnames = ['Produkt', 'Pris (kr)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Skriv kolumnnamnen till CSV-filen
    writer.writeheader()

    # Loop igenom varje produktkort
    for card in product_cards:
        try:
            # Hitta produktnamn och pris
            name_element = card.find_element(By.CSS_SELECTOR, "a[class*='cat_infoText-']")
            price_element = card.find_element(By.CSS_SELECTOR, "span[class*='cat_originalPrice-']")

            # Hämta texten från elementen
            name = name_element.text
            price_text = price_element.text.replace("kr", "").replace(",", ".")

            print(f"Produkt: {name}, Pristext: {price_text}")

            # Kontrollera om priset är numeriskt
            try:
                price = float(price_text)
                # Om priset är under 700 kr, skriv till CSV-filen
                if price < 700:
                    writer.writerow({'Produkt': name, 'Pris (kr)': price})
                    print(f"Produkt: {name}, Pris: {price} kr")
            except ValueError:
                print(f"Kunde inte konvertera pris: {price_text}")
        except Exception as e:
            # Hantera eventuella fel
            print(f"Error: {e}")

# Stäng webbläsaren
driver.quit()
