from app_test import db,create_app
from app_test.ModelExamples import Puppy
app = create_app()
#CREATES ALL TABLES -  TRANSFORMAS MODEL CLASS INTO TABLES


with app.app_context():
###CREATE
    myPuppy = Puppy('Rufus',5)
    db.session.add(myPuppy)
    db.session.commit()

####READ
# .all() gives the __str__ /  __repr__ for each entry
# query.filter_by(email=email).first()
# query.get(user_id)
# query.filter_by(user_id=user_id).all()
    all_puppies = Puppy.query.all()
    print(f"PRINT ALL THE PUPPIES : {all_puppies}")
    puppy_one = Puppy.query.get(1)
    print(f"PRINT first : {puppy_one}") ## when column is not defined the  __str__ /  __repr__  is returned
    print(f"PRINT first name: {puppy_one.name}")
    print(f"PRINT first age: {puppy_one.age}") 

#### FILTERS

    puppy_select_where = Puppy.query.filter_by(name = 'Frank')
    print(puppy_select_where)
    # SELECT puppies.id AS puppies_id, puppies.name AS puppies_name, puppies.age AS puppies_age
    # FROM puppies    
    # WHERE puppies.name = ?
    print(puppy_select_where.all())

### UPDATE
    first_puppy = Puppy.query.get(1)
    first_puppy.age =  10
    db.session.add(first_puppy)
    db.session.commit()
    

    first_puppy = Puppy.query.get(1)
    print (first_puppy.age)


###DELETE
    all_puppies = Puppy.query.all()
    print(f"ALL PUPPIES BEFORE DELETE : {all_puppies}")
    # puppies_to_delete = Puppy.query.filter(id != 1)
    puppies_to_delete = Puppy.query.get(1)
    print(f"PUPPIES TO BE DELETED: {puppies_to_delete}")
    db.session.delete(puppies_to_delete)
    db.session.commit()

    all_puppies = Puppy.query.all()
    print(f"ALL PUPPIES AFTER DELETE : {all_puppies}")
    