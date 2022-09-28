import sys
import argparse
import main
from createtown import create_connected_town, get_pseudorandom_number
from pavingplan import PavingPlan, paving_plan_from_file
import matplotlib.pyplot as plt
from random import random
from createtown import get_pseudorandom_number


def __main__(version, student_name):
    town = main.build_town_from_file("static/town.txt")

    argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--alternative', dest="a",
                        action="store_true", help="show current town in alternate format (what test wants)")
    parser.add_argument('-an', '--alternative-new', dest="a",
                        action="store_true", help="show current town in alternate format (what spec wants)")
    parser.add_argument('-r', '--read', dest="r",
                        help="read town data from file identified by parameter")
    parser.add_argument('-s', '--standard', dest="s", action="store_true",
                        help="show current town in standard format")
    parser.add_argument('-sf', '--standard-formatted', dest="sf", action="store_true",
                        help="show current town in standard format -- pretty print")
    parser.add_argument('-v', '--version', dest="v",
                        action="store_true", help="show version")
    parser.add_argument('-w', '--write', dest="w",
                        help="write current town to file identified by parameter")
    parser.add_argument('-c', '--create', dest="c", nargs=2, type=int,
                        help="creates town given number of buildings and streets")
    parser.add_argument('-p', '--pave', dest="p", nargs=1,
                        help="creates and writes paving plan to given location")
    parser.add_argument('-d', '--display', dest="d", action="store_true",
                        help="displays stored paving data and total cost")
    parser.add_argument('-e', '--evaluate', dest="e", nargs=1,
                        help="evaluate given paving plan for current town")
    parser.add_argument('-g', '--graph', dest="g", action="store_true",
                        help="Tracks speed of pseudorandom number generator and graphs the results")
    parser.add_argument('-he', dest="h", action="store_true")
    args = parser.parse_args()

    if len(argv) == 0:
        town.print_town_s()
        return 0

    if args.c:
        town = create_connected_town(args.c[0], args.c[1])

    elif args.r:
        town = main.build_town_from_file(args.r)

    if args.a:
        town.print_town_a()
    if args.s:
        town.print_town_s()
    if args.sf:
        town.print_town_s_formatted()
    if args.v:
        print(f'version {version[0]} by {student_name[0]}')
    if args.w:
        town.write_town(args.w)
        print(args.w)
    if args.p:
        new_plan = PavingPlan(town)
        new_plan.name = "\"" + town.name.strip("\"") + " Paving Plan" + "\""
        new_plan.verify_paving_plan(town)
        new_plan.write_paving_plan(args.p[0])
    if args.d:
        plan = paving_plan_from_file("static/pavingplan.txt", town)
        plan.find_total_cost(town)
        plan.print_paving_plan()
    if args.e:
        plan = paving_plan_from_file(args.e[0], town)
        plan.evaluate_paving_plan()
    if args.g:
        our_pseudorandom = []
        python_pseudorandom = []
        for i in range(0,1000):
            our_pseudorandom.append(get_pseudorandom_number(51))
            python_pseudorandom.append(int(random()*51))

        plt.hist(our_pseudorandom)
        plt.title('Our Psuedorandom Number Generator')
        plt.ylabel('Frequency')
        plt.xlabel('Number Generated')
        plt.show()
        plt.hist(python_pseudorandom)
        plt.title('Python\'s Psuedorandom Number Generator')
        plt.ylabel('Frequency')
        plt.xlabel('Number Generated')
        plt.show()

    if args.h:
        print('''Syntax: [-option [parameter]]
                  options:
                  \ts   show current town in standard format
                  \ta   show current town in alternate format
                  \tr   read town data from file identified by parameter
                  \tw   write current town to file identified by parameter
                  \tv   show version
                  \tc   create a randomly generated town
                  \tp   creates and writes paving plan to given location
                  \td   displays stored paving data and total cost
                  \te   evaluate given paving plan for current town
                  \tg   Tracks speed of pseudorandom number generator and graphs the results
                  \th   help (this display)''')
    return 0


version = [1.0]
student_names = ["Joe Gunter", "Juan Ruiz", "David Soth-Kimmel", "Stilian Balasopoulov"]


__main__(version, student_names)
