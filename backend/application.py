from flask import Flask, render_template
from sim.simloop import SimLoop
app = Flask(__name__)




@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    simulation = SimLoop()

    for i in range(10):
        # print("Iteration", i)
        simulation.advance_one_year()
        simulation.end_player_turn()
        
    # pprint(simulation.log)
    for i in simulation.log:
        print(i); print()
    # print()
    # print(simulation.food_trading.mat)
            
    app.run()

# hello world
# goodbye
# sad