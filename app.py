from flask import Flask,render_template,request, redirect, flash
import utils
utils.validate_folders(['templates', 'covid_data', 'static'])

import covid_api
import click._compat
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dajdsjas'

def consoleLog(text):
    click.secho(str(text), fg='green')
 
@app.route('/', methods = ["GET"])
def home():
    return render_template('homepage.html') 
 

@app.route('/submitTrain', methods = ["POST"])
def submit_train():
    train_number = request.form.get('tain_no')

    # if train number is not numeric
    if not train_number.isnumeric():
        flash('Train number not numeric')
        return render_template('homepage.html')
    
    data = covid_api.route_data(train_number)
    #data = [(False, 'Jasidih Jn', 'Deoghar', 'jharkhand', ['1.07', '0.00', '0.70', '0.00', '0.00'], ['3683', '23', '3642', '6951', '0']), (True, 'Madhupur Jn', 'Deoghar', 'jharkhand', ['1.07', '0.00', '0.70', '0.00', '0.00'], ['3683', '23', '3642', '6951', '0']), (True, 'Chittaranjan', 'Paschim Bardhaman', 'westbengal', ['7.33', '0.07', '12.10', '0.00', '0.00'], ['16357', '169', '16012', '0', '0']), (True, 'Asansol Jn', 'Paschim Bardhaman', 'westbengal', ['7.33', '0.07', '12.10', '0.00', '0.00'], ['16357', '169', '16012', '0', '0']), (True, 'Joychandi Pahar', 'Purulia', 'westbengal', ['3.93', '0.03', '4.87', '0.00', '0.00'], ['7262', '49', '7128', '0', '0']), (True, 'Purulia Jn', 'Purulia', 'westbengal', ['3.93', '0.03', '4.87', '0.00', '0.00'], ['7262', '49', '7128', '0', '0']), (True, 'Chakradharpur', 'West Singhbhum', 'jharkhand', ['0.27', '0.00', '0.40', '0.00', '0.00'], ['4841', '39', '4799', '0', '0']), (True, 'Rourkela', 'Sundargarh', 'odisha', ['12.07', '0.00', '15.73', '0.00', '0.00'], ['15719', '177', '15461', '0', '0']), (True, 'Jharsuguda Jn', 'Jharsuguda', 'odisha', ['3.20', '0.00', '3.30', '0.00', '0.00'], ['7859', '26', '7798', '1663', '0']), (True, 'Sambalpur', 'Sambalpur', 'odisha', ['6.47', '0.03', '9.17', '0.00', '0.00'], ['10005', '78', '9851', '2007', '0']), (True, 'Bargarh Road', 'Bargarh', 'odisha', ['6.07', '0.00', '7.07', '0.00', '0.00'], ['10648', '42', '10564', '0', '0']), (True, 'Balangir', 'Balangir', 'odisha', ['2.20', '0.00', '1.90', '0.00', '0.00'], ['8826', '41', '8774', '87867', '0']), (True, 'Titlagarh', 'Balangir', 'odisha', ['2.20', '0.00', '1.90', '0.00', '0.00'], ['8826', '41', '8774', '87867', '0']), (True, 'Kesinga', 'Kalahandi', 'odisha', ['1.13', '0.03', '1.43', '0.00', '0.00'], ['6390', '32', '6349', '1458', '0']), (True, 'Muniguda', 'Rayagada', 'odisha', ['1.57', '0.00', '1.70', '0.00', '0.00'], ['8450', '45', '8398', '578', '0']), (True, 'Rayagada', 'Rayagada', 'odisha', ['1.57', '0.00', '1.70', '0.00', '0.00'], ['8450', '45', '8398', '578', '0']), (True, 'Parvatipuram', 'Vizianagaram', 'andhrapradesh', ['1.03', '0.00', '1.40', '0.00', '0.00'], ['41159', '238', '40910', '531433', '0']), (True, 'Bobbili', 'Vizianagaram', 'andhrapradesh', ['1.03', '0.00', '1.40', '0.00', '0.00'], ['41159', '238', '40910', '531433', '0']), (True, 'Vizianagram Jn', 'Vizianagaram', 'andhrapradesh', ['1.03', '0.00', '1.40', '0.00', '0.00'], ['41159', '238', '40910', '531433', '0']), (True, 'Visakhapatnam', 'Visakhapatnam', 'andhrapradesh', ['10.40', '0.20', '13.60', '0.00', '0.00'], ['59996', '567', '59400', '744983', '0']), (True, 'Samalkot Jn', 'East Godavari', 'andhrapradesh', ['7.17', '0.00', '10.83', '0.00', '0.00'], ['124421', '636', '123722', '944746', '0']), (True, 'Rajamundry', 'East Godavari', 'andhrapradesh', ['7.17', '0.00', '10.83', '0.00', '0.00'], ['124421', '636', '123722', '944746', '0']), (True, 'Eluru', 'West Godavari', 'andhrapradesh', ['4.23', '0.07', '5.27', '0.00', '0.00'], ['94316', '542', '93730', '793098', '0']), (True, 'Vijayawada Jn', 'Krishna', 'andhrapradesh', ['11.47', '0.17', '16.33', '0.00', '0.00'], ['48884', '681', '48109', '782232', '0']), (True, 'Tenali Jn', 'Guntur', 'andhrapradesh', ['8.37', '0.03', '12.53', '0.00', '0.00'], ['75678', '671', '74961', '833823', '0']), (True, 'Ongole', 'Prakasam', 'andhrapradesh', ['1.03', '0.00', '2.30', '0.00', '0.00'], ['62200', '580', '61582', '697340', '0']), (True, 'S.P.S. Nellore', 'S.P.S. Nellore', 'andhrapradesh', ['5.23', '0.03', '6.07', '0.00', '0.00'], ['62451', '507', '61878', '682964', '0']), (True, 'Gudur Jn', 'S.P.S. Nellore', 'andhrapradesh', ['5.23', '0.03', '6.07', '0.00', '0.00'], ['62451', '507', '61878', '682964', '0']), (True, 'Sullurupeta', 'S.P.S. Nellore', 'andhrapradesh', ['5.23', '0.03', '6.07', '0.00', '0.00'], ['62451', '507', '61878', '682964', '0']), (True, 'Chennai Egmore', 'Chennai', 'tamilnadu', ['143.83', '1.90', '137.47', '1984.77', '0.00'], ['234837', '4142', '228942', '2667777', '0']), (True, 'Tambaram', 'Chengalpattu', 'tamilnadu', ['41.23', '0.53', '41.47', '0.00', '0.00'], ['52573', '780', '51436', '51771', '0'])]
    return render_template('covid_data.html', data = data)

if __name__ =='__main__':
    app.run(debug=True)
 
