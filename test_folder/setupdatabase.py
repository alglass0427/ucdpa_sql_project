from app_test import db,create_app
from app_test.ModelExamples import Puppy
app = create_app()
#CREATES ALL TABLES -  TRANSFORMAS MODEL CLASS INTO TABLES

# db.create_all()
#lambda allows throw away functions  -- 
# def adder(x):
#     return lambda y: x + y
with app.app_context():
    sam = Puppy('Sammy',3)
    frank = Puppy('Frank',4)

    print (sam.id)
    print (frank.id)

    # Add the instances to the session
    db.session.add_all([sam, frank])

    # # Commit the session to save the instances to the database
    db.session.commit()

    # # Print the IDs after committing to the session (should now show the assigned IDs)
    print(sam.id)  # Should now show the assigned ID from the database
    print(frank.id)  # Should now show the assigned ID from the database