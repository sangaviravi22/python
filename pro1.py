import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SkyCinemas:
    def __init__(self):
        self.movies = ["kalkki", "maharaja", "indian 2"]
        self.classes = {"first class": 200, "second class": 150,"third class":100}
        self.gst_rate=0.8
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="theepa_theater"
        )
        self.cursor = self.db.cursor()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS theepa_theater")
        self.db.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(255),
                email VARCHAR(255),
                total DECIMAL(10, 2)
            )
        """)
        self.db.commit()

    def display_movies(self):
        print("WELCOME TO SKY CINEMAS")
        print("Available movies:")
        for movie in self.movies:
            print(movie)

    def get_movie_details(self):
        name_of_the_movie = input("Enter movie name which you want to see: ")
        if name_of_the_movie in self.movies:
            print("Movie is available")
            return name_of_the_movie
        else:
            print("Movie is not available")
            return None

    def get_class_details(self):
        enter_class = input("Enter which class you want : ")
        if enter_class in self.classes:
            print("Single ticket price is", self.classes[enter_class])
            return enter_class
        else:
            print("Class is not available")
            return None

    def calculate_total(self, enter_class, how_many):
        base_total=self.classes[enter_class] * int(how_many)
        gst_amount=base_total*self.gst_rate
        total = base_total+gst_amount
        print(f"Your total booking ticket  price including gst is {total:.2f}")
        return total,gst_amount

    def make_payment(self, cm, pay):
        if cm == "on hand" and pay == "paid":
            print("Your ticket is booked!! Enjoy the movie with your family!!")
            return True
        elif cm == "online" and pay == "paid":
            print("Your ticket is booked!! Enjoy the movie with your family!!")
            return True
        else:
            print(" Sorry!! Your ticket is not booked")
            return False

    def send_email(self, bill, total,gst_amount):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("uma14275@gmail.com", "xzby zxqy ewar exij")
            msg=MIMEMultipart()
            msg['From']="uma14275@gmail.com"
            msg['To']=bill
            msg['Subject']="Your ticket bokking conformation"
            body=(
                f"Base price of the  ticket: {total - gst_amount:.2f}\n\n"
                f" Ticket price with gst_amount: {gst_amount:.2f}\n"
                f" Your Tickets booking total_price: {total:.2f}\n\n"
                f"Thanks for booking ticket with us!!"
            )
            msg.attach(MIMEText(body,'plain'))

            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print("Error occurs in the email:", e)
        except Exception as e:
            print(" Sorry the mail is not send because the occuring errors:", e)

    def book_ticket(self):
        self.display_movies()
        name_of_the_movie = self.get_movie_details()
        if name_of_the_movie:
            enter_class = self.get_class_details()
            if enter_class:
                how_many = int(input("How many tickets you want to book: "))
                total, gst_amount = self.calculate_total(enter_class, how_many)
                cm = input("Is cash pay in online or on hand: ")
                pay = input("paid/unpaid? ")
                if self.make_payment(cm, pay):
                    bill = input("Enter your mail for bill: ")
                    self.send_email(bill, total,gst_amount)
                    self.cursor.execute("""INSERT INTO ticket_processing (movie_name, email, total)VALUES (%s, %s, %s)""", (name_of_the_movie, bill, total))
                    self.db.commit()
                    print("Ticket booked successfully!")

if __name__ == "__main__":
    sky_cinemas = SkyCinemas()
    sky_cinemas.create_database()
    sky_cinemas.create_table()
    while True:
        command = input("Type 'book' to book a ticket or 'exit' to exit: ")
        if command.lower() == 'exit':
            break
        elif command.lower() == 'book':
            sky_cinemas.book_ticket()
        else:
            print("Invalid command. Please try again later with a valid command.") 