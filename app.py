from flask import Flask, render_template_string, request, flash, redirect, url_for, render_template
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin, current_user
import json

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # # Flask settings
    # SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'tst_app',
        'host': 'mongodb://localhost:27017/tst_app'
    }
def create_app():
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Setup Flask-MongoEngine
    db = MongoEngine(app)

    class Indication_of_validation(db.Document):
        ID_Bus = db.IntField(default=0)
        Quantity_of_validation = db.IntField(default=0)
        Time_of_validation = db.StringField(default='')

    class Weight_of_the_bus(db.Document):
        Min_weight = db.IntField(default= 0)
        Max_weight = db.IntField(default= 0)
        Time_of_validation = db.StringField(default='')

    class Buses(db.Document):
        DefaultWeight = db.IntField(default=0)
        Capacity = db.IntField(default=0)

    class Routes(db.Document):
        Name_of_route = db.IntField(default=0)
        Status = db.StringField(default='')
        Routes_lenght = db.IntField(default=0)
        Quantity_of_controllers = db.IntField(default=0)
        Quantity_of_station = db.IntField(default=0)





    @app.route('/')
    def hello_world():
        # add test data
        # Bus = Buses(DefaultWeight = 12000,
        #             Types_of_buses_Type = 'middle')
        # Bus.save()
        #
        # Route = Routes(Name_of_route = 2,
        #                Status = 'red',
        #                Routes_lenght= 20,
        #                Quantity_of_controllers =0,
        #                Quantity_of_station =5)
        # Route.save()

        # Test_Validator = Indication_of_validation(ID_Bus = 1,
        #                                           Quantity_of_validation = 100,
        #                                           Time_of_validation = '2019 12 6 12:00')
        # Test_Validator.save()
        # Test_Validator = Indication_of_validation(ID_Bus=1,
        #                                           Quantity_of_validation=110,
        #                                           Time_of_validation='2019 12 6 12:05')
        # Test_Validator.save()
        # Test_Validator = Indication_of_validation(ID_Bus=1,
        #                                           Quantity_of_validation=115,
        #                                           Time_of_validation='2019 12 6 12:08')
        # Test_Validator.save()
        # Test_Validator = Indication_of_validation(ID_Bus=1,
        #                                           Quantity_of_validation=130,
        #                                           Time_of_validation='2019 12 6 12:13')
        # Test_Validator.save()
        # Test_Validator = Indication_of_validation(ID_Bus=1,
        #                                           Quantity_of_validation=130,
        #                                           Time_of_validation='2019 12 6 12:20')
        # Test_Validator.save()
        #
        # Test_Weight = Weight_of_the_bus(Min_weight=12500,
        #                                 Max_weight=12700,
        #                                 Time_of_validation='2019 12 6 12:00')
        # Test_Weight.save()
        # Test_Weight = Weight_of_the_bus(Min_weight=12400,
        #                                 Max_weight=12800,
        #                                 Time_of_validation='2019 12 6 12:05')
        # Test_Weight.save()
        # Test_Weight = Weight_of_the_bus(Min_weight=12700,
        #                                 Max_weight=12800,
        #                                 Time_of_validation='2019 12 6 12:08')
        # Test_Weight.save()
        # Test_Weight = Weight_of_the_bus(Min_weight=12800,
        #                                 Max_weight=12800,
        #                                 Time_of_validation='2019 12 6 12:13')
        # Test_Weight.save()
        # Test_Weight = Weight_of_the_bus(Min_weight=12000,
        #                                 Max_weight=12000,
        #                                 Time_of_validation='2019 12 6 12:20')
        # Test_Weight.save()
        # fun for result quantity people and load of bus
        people_avg_weigth =75
        def load(capasity,weight,bus_weight):
            Load = (weight-bus_weight)/people_avg_weigth/capasity*100
            return Load

        def tickets_by_weight(max_weight, min_weight,people_avg_weight):
            Load = (max_weight-min_weight)/people_avg_weight
            return Load

        # ticket_before is quantity of tickets on last station
        # ticket_before is quantity of tickets on current station
        def validation_tickets(ticket_before, ticket_after):
            return ticket_after-ticket_before

        def people_without_ticket(max_weight, min_weight,people_avg_weight,ticket_before, ticket_after):
            ticket_weight = tickets_by_weight(max_weight, min_weight,people_avg_weight)
            validation_ticket = validation_tickets(ticket_before, ticket_after)
            return ticket_weight - validation_ticket

        # result test data from mongodb

        Weigth = Weight_of_the_bus.objects.all()
        minWeight =[]
        maxWeight =[]
        for weigth in Weigth:
            minWeight.append(weigth.Min_weight)
            maxWeight.append(weigth.Max_weight)
        Valid =[]
        Validator = Indication_of_validation.objects.all()
        for valid in Validator:
            Valid.append(valid.Quantity_of_validation)


        withoutTicket = []
        BusLoad = []
        quantity_of_bus_station = 0
        rout = Routes.objects.all()
        for r in rout:
            quantity_of_bus_station = r.Quantity_of_station

        busCapacity = 0
        busWeight = 0
        bus = Buses.objects.all()
        for b in bus:
            busCapacity = b.Capacity
            busWeight = b.DefaultWeight

        for station in range(quantity_of_bus_station):
            BusLoad.append(round(load(busCapacity,maxWeight[station],busWeight),4))
            withoutTicket.append(round(people_without_ticket(maxWeight[station], minWeight[station],
                                                       people_avg_weigth,Valid[station], Valid[station+1]),4))
        # print('Loadind')
        # print(BusLoad)
        # print('without tickets')
        # print(withoutTicket)
        # print(withoutTicket)


        # test station name
        StationName =[]
        for i in range(len(BusLoad)):
            StationName.append("Station#"+str(i+1))
        # print(StationName)

        return render_template('index.html', BusLoad = BusLoad, withoutTicket = withoutTicket, StationName = StationName)

    return app
# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)