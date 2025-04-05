from flask import Flask, render_template
from sim.simloop import SimLoop
from pprint import pprint
app = Flask(__name__)




@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    simulation = SimLoop()

    for i in range(6):
        # print("Iteration", i)
        simulation.advance_one_year()
        
    # pprint(simulation.log)
    for i in simulation.log:
        print(i); print()
    print()
            
    # app.run(debug=True)

# hello world
# goodbye
# sad