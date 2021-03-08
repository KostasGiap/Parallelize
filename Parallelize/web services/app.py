from flask import Flask, request
import mysql.connector
import datetime



class MYSQL(object):
  def __init__(self):
    user = "user"
    password = "MyPassword@123"
    host = "127.0.0.1"
    database = "electricity"
    self.cnx = mysql.connector.connect(user=user, password=password,
                                          host=host, database=database)
    self.cursor = self.cnx.cursor()

  # Executes a specific stored procedure
  # Saves  client id and electric value into mysql server
  def ExecProcedure(self, client_id, e_value):
    query = "CALL Add_Value(%s, %s);"
    self.cursor.execute(query, (client_id, e_value))
    self.cnx.commit()

  # Executes a specific stored procedure
  # Saves total electricity value into mysql server
  def ExecProcedure2(self, total):
    query = "CALL Add_Total_Value (%s);"
    self.cursor.execute(query, (total,))
    self.cnx.commit()

  # Closes the connection with mysql server
  def Close(self):
    self.cursor.close()
    self.cnx.close()


# Receives a POST request from client
# And stores the data into mysql server
app = Flask(__name__)
@app.route("/", methods=["POST"])
def connect(total=0, date_init=datetime.datetime.now()):
  client_id = request.form.get('ip') 
  e_value = request.form.get('data')
  total += int(e_value)
  print "client id: {0} electric value: {1}".format(client_id, e_value)
  mysqldb.ExecProcedure(client_id, e_value)
  if datetime.datetime.now() == date_init + datetime.timedelta(days=1):
    mysqldb.ExecProcedure2(total)
    total = 0
    date_init = datetime.datetime.now()
  return ""



if __name__ == '__main__':
  mysqldb = MYSQL()
  app.run(debug=True, port=8080)
