import mysql.connector
import pandas as pd
import smtplib
import random
import csv
import datetime

class Election_Day:
    def __init__(self):
        self.candidates = {1: "sinchan", 2: "himavaari", 3: "hattori", 4: "sinshoo", 5: "masaav"}
        self.votes_count = {i: 0 for i in self.candidates.keys()}
        self.conn = mysql.connector.connect(
            host='localhost',
            database='election',
            user='root',
            password='12345'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS votes (email VARCHAR(255), candidate INT)")
        self.conn.commit()

    def email(self):
        try:
            enter_email = input("Enter your mail id: ")
            otp = random.randint(00000, 99999)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("uma14275@gmail.com", "xzby zxqy ewar exij")
            msg = f" This is Your OTP  {otp} is working on today only"
            s.sendmail("your-email@gmail.com", enter_email, msg)
            s.quit()
            otp_input = int(input("Enter your OTP: "))
            if otp == otp_input:
                return enter_email
            else:
                print("Invalid OTP !!  please enter the correct OTP...")
                return False
        except smtplib.SMTPException as e:
            print(f"Error sending email !! please enter correct email id...: {e}")
            return False

    def voting(self, email):
        while True:
            x = datetime.datetime.now()
            print("\nCandidates Name with Number:")
            print("------------")
            print("1. Sinchan")
            print("2. Himavaari")
            print("3. Hattori")
            print("4. Sinshoo")
            print("5. Masaav")
            print("0. Exit")
            vote = int(input("Enter your vote by choosing the number which candidate you want to win: "))
            if vote == 0:
                self.result()
                print("Election were  Completted Successfully!!")
                break
            elif vote in self.candidates.keys():
                print(f"Its done keep doing your Democratic Duty! {x}")
                self.votes_count[vote] += 1
                self.cursor.execute("INSERT INTO votes (email, candidates) VALUES (%s, %s)", (email, vote))
                self.conn.commit()
                print("Your Vote is recorded successfully and the results will be soon!")
                self.email()
            else:
                print("Ohh! There no candidate in that number")

    def result(self):
        with open('vote.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["candidate", "votes"])
            for i, j in self.votes_count.items():
                writer.writerow([self.candidates[i], j])
        for i, j in self.votes_count.items():
            print(f"{self.candidates[i]}: {j}")
        max_votes = max(self.votes_count.values())
        winners = [i for i, j in self.votes_count.items() if j == max_votes]
        if len(winners) == 1:
            print(f"The winner is {self.candidates[winners[0]]}")
        else:
            print("It's a tie between:")
            for winner in winners:
                print(self.candidates[winner])

election_day = Election_Day()
email = election_day.email()
if email:
    election_day.voting(email)