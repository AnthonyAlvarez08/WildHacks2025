from flask import Flask, render_template, request
from sim.simloop import SimLoop
from sim.request import Request
import sim.constants as constants

app = Flask(__name__)


simulation: SimLoop = None

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():

    flag = False
    flagmsg = ""

    if request.method == "POST":
        # simulation.advance_one_year()
        # simulation.end_player_turn()

        print(request.form)
        target_country, mycountry, option, quantity = (request.form[i] for i in ['country', 'mycountry', 'option', 'quantity'])
        print(target_country, mycountry, option, quantity)

        if "ask" in option:
            resource = ""
            if "VEG" in option:
                resource = constants.VEG
            if "MEAT" in option:
                resource = constants.MEAT
            if "GRAIN" in option:
                resource = constants.GRAIN


            simulation.request_resources(simulation.find_country(mycountry), simulation.find_country(target_country), resource, float(quantity))
        elif "end turn" == option:
            simulation.end_player_turn()
            simulation.advance_one_year()
        elif "invest" in option:
            if "AGRI" in option:
                res = simulation.invest_in_agriculture(simulation.find_country(mycountry))
            else:
                res = simulation.invest_money_prod(simulation.find_country(mycountry))

            flag = True
            temp = "Success" if res else "Failure"
            flagmsg = f"Operation results: { temp }"
        else:
            res = simulation.give_aid(simulation.find_country(mycountry), simulation.find_country(target_country), quantity)
            flag = True
            temp = "Success" if res else "Failure"
            flagmsg = f"Operation results: { temp }"



            


    # simulation = SimLoop()
    # for i in range(10):
    #     # print("Iteration", i)
    #     simulation.advance_one_year()
    #     simulation.end_player_turn()
    return render_template("index.html", stuff= "Welcome to Food Trading Sim", 
                           countries=[i.name for i in simulation.countries],
                           mycountries = [i.name for i in simulation.countries if i.player_controlled],
                           options=["give money", "ask for VEG", "ask for MEAT", "ask for GRAIN", "invest in AGRICULTURE", "invest in INFRASTRUCTURE (more money per turn)", "end turn"],
                           flag=flag,
                           flagmsg=flagmsg,
                           log=simulation.log[simulation.log_start:])

if __name__ == '__main__':
    simulation = SimLoop()

    # for i in range(10):
    #     # print("Iteration", i)
    #     simulation.advance_one_year()
    #     simulation.end_player_turn()
        
    # pprint(simulation.log)
    # for i in simulation.log:
    #     print(i); print()
    # print()
    # print(simulation.food_trading.mat)
            
    app.run(debug=True)
