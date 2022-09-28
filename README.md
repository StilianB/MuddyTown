
***** MuddyTown Project *****

Joe Gunter, Juan Ruiz, David Soth-Kimmel, Stilian Balasopoulov

### Executing the program

## Setup

> `make setup`

## Running

> `python3 processtown.py {flags_and_arguments}``

OR

> `make run ARGS="{flags_and_arguments}"`
- `make run` is just the aliased make command for `python3 processtown.py`

# Flags

- `-a`
  - show current town in alternate format

- `-an`
  - show current town in alternate format conforming to spec requirements

- `-r`
  - read town data from file identified by parameter
  - takes one parameter
    - arg[0] should be the location to a text file containing town data
  - is typically followed by a subsequent flag

- `-s`
  - show current town in standard format

- `-sf`
  - show current town in a prettier standard format

- `-v`
  - print version and name

- `-w`
  - write current town to file identified by parameter
  - should be proceeded by reading a town with the `-r` flag, otherwise will use the default town from "town.txt"

- `-c`
  - creates town given number of buildings and streets
  - takes two arguments
    - arg[0] being number of buildings
    - arg[1] being number of streets

- `-p`
  - create a paving plan and write to file identified by parameter
  - takes one parameter
    - arg[0] should be the location of a text file

- `-d`
  - displays the paving plan stored in pavingplan.txt
  - determines total cost of given paving plan

- `-e`
  - evaluate given paving plan for stored town
  - takes one parameter
    - arg[0] should be the location of a text file

- `-g`
  - evaluate pseudorandom number generator
  - requires:
    - matplotlib.pyplot

- `-he`
  - help function that lists flag options


## Testing

> `./test.sh`

OR

> `make test`