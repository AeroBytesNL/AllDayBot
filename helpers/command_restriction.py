from database import Database



def check_restriction(user_id, command):
    Database.cursor.execute(f"SELECT * FROM command_restriction WHERE user_id = {user_id} LIMIT 1")
    res = Database.cursor.fetchone() 

    commands = []   
    commands = [res[1], {res[2]}, res[3], res[4], res[5]]
        
    if command in commands:
        return False
    else:
        return True


def insert_command_restriction(user_id, command_one, command_two, command_three, command_four, command_five):
    Database.cursor.execute(f"SELECT * FROM command_restriction WHERE user_id={user_id} LIMIT 1")
    res = Database.cursor.fetchone()

    # if user in DB
    if res != None:
        Database.cursor.execute(f"UPDATE command_restriction SET command_res_one='{command_one}', command_res_two='{command_two}', command_res_three='{command_three}', command_res_four='{command_four}', command_res_five='{command_five}' WHERE user_id={user_id}")
        Database.db.commit()

    else:
        Database.cursor.execute(f"INSERT INTO command_restriction (user_id, command_res_one, command_res_two, command_res_three, command_res_four, command_res_five) VALUES ({user_id}, '{command_one}', '{command_two}', '{command_three}', '{command_four}', '{command_five}')")
        Database.db.commit()



def delete_command_restriction(user_id):
    Database.cursor.execute(f"DELETE FROM command_restriction WHERE user_id = {user_id}")
    Database.db.commit()



def see_restricted_users():
    Database.cursor.execute("SELECT * FROM command_restriction")
    return Database.cursor.fetchall()