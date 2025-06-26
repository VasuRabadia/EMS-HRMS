import pymongo
import pymongo.mongo_client
import random


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["Main"]
    collection = database["Employees Dummy"]
    number_of_entries = 100

    first_names = [
        "John",
        "Jane",
        "Emily",
        "Michael",
        "Jessica",
        "Daniel",
        "Sophia",
        "David",
        "Mia",
        "James",
        "Olivia",
        "Liam",
        "Ava",
        "Noah",
        "Isabella",
        "Mason",
        "Emma",
        "Lucas",
        "Amelia",
        "Elijah",
        "Charlotte",
        "William",
        "Sophia",
        "Benjamin",
        "Alexander",
        "Julia",
        "Gabriel",
        "Evelyn",
        "Logan",
        "Abigail",
        "Caleb",
        "Hannah",
        "Jaxon",
        "Avery",
        "Landon",
        "Riley",
        "Parker",
        "Savannah",
        "Julian",
        "Aubrey",
        "Gavin",
        "Lily",
        "Cameron",
        "Paisley",
        "Bryson",
        "Rowan",
        "Remi",
        "Kai",
        "Sage",
        "River",
        "Ethan",
        "Luna",
        "Aiden",
        "Piper",
        "Sawyer",
        "Everly",
        "Owen",
        "Ruby",
        "Cohen",
        "Wesley",
    ]
    last_names = [
        "Doe",
        "Smith",
        "Johnson",
        "Brown",
        "Davis",
        "Wilson",
        "Moore",
        "Taylor",
        "Anderson",
        "Martinez",
        "Hernandez",
        "Clark",
        "Rodriguez",
        "Lewis",
        "Lee",
        "Walker",
        "Hall",
        "Young",
        "King",
        "Wright",
        "Scott",
        "Green",
        "Adams",
        "Baker",
        "Brooks",
        "Jenkins",
        "Martin",
        "Thompson",
        "White",
        "Harris",
        "Nelson",
        "Lee",
        "Hall",
        "Russell",
        "Patel",
        "Brooks",
        "Martin",
        "Sanchez",
        "Jenkins",
        "Thompson",
        "White",
        "Harris",
        "Davis",
        "Nelson",
        "Lee",
        "Hall",
        "Russell",
        "Patel",
        "Brooks",
    ]

    print(len(first_names), len(last_names))
    names = []
    try:
        query = {}
        projection = {"_id": 0, "name": 1}
        names_list = list(collection.find(query, projection))
        for i in names_list:
            names.append(i["name"])
        names = list(map(str, names))
        names.sort()
    except Exception:
        print(len(names), names)

    while len(names) < number_of_entries:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        if full_name not in names:
            names.append(full_name)

    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Austin",
        "Jacksonville",
        "San Francisco",
        "Indianapolis",
        "Seattle",
        "Denver",
        "Washington",
        "Boston",
        "El Paso",
        "Detroit",
        "Nashville",
        "Portland",
        "Oklahoma City",
        "Las Vegas",
        "Louisville",
        "Baltimore",
        "Memphis",
        "Milwaukee",
        "Albuquerque",
        "Tucson",
        "Fresno",
        "Sacramento",
        "Kansas City",
        "Atlanta",
        "Colorado Springs",
        "Virginia Beach",
        "Raleigh",
        "Omaha",
        "Miami",
        "Oakland",
        "Minneapolis",
        "Tulsa",
        "Wichita",
        "New Orleans",
        "Arlington",
        "St. Louis",
        "Cleveland",
    ]

    new_insert = []
    for i in range(number_of_entries):
        name = names[i % len(names)]
        reference_name = random.choice(names)
        if reference_name == name:
            reference_name = None
        total_investment = random.randint(0, 1000) * 10000
        plan = random.choice(["Basic", "Silver", "Gold", "Platinum"])
        last_generated_date_date = random.randint(1, 28)
        last_generated_date_month = random.randint(1, 12)
        last_generated_date_year = str(random.randint(2019, 2023))
        if last_generated_date_date < 10:
            last_generated_date_date = str(f"0{last_generated_date_date}")
        else:
            last_generated_date_date = str(last_generated_date_date)
        if last_generated_date_month < 10:
            last_generated_date_month = str(f"0{last_generated_date_month}")
        else:
            last_generated_date_month = str(last_generated_date_month)
        last_generated_date = f"{
            last_generated_date_date}-{last_generated_date_month}-{last_generated_date_year}"
        mobile_number = f"{random.randint(7000000000, 9999999999)}"
        city = cities[i % len(cities)]
        investment_date_date = random.randint(1, 28)
        investment_date_month = random.randint(1, 12)
        investment_date_year = str(random.randint(2019, 2023))
        if investment_date_date < 10:
            investment_date_date = str(f"0{investment_date_date}")
        else:
            investment_date_date = str(investment_date_date)
        if investment_date_month < 10:
            investment_date_month = str(f"0{investment_date_month}")
        else:
            investment_date_month = str(investment_date_month)
        investment_date = f"{
            investment_date_date}-{investment_date_month}-{investment_date_year}"
        email = f"{name.lower().replace(' ', '.')}@example.com"
        age = random.randint(20, 40)

        new_insert.append(
            {
                "name": name,
                "reference_name": reference_name,
                "total_investment": total_investment,
                "plan": plan,
                "last_generated_date": last_generated_date,
                "mobile_number": mobile_number,
                "city": city,
                "investment_date": investment_date,
                "email": email,
                "age": age,
            }
        )

    collection.insert_many(new_insert)
