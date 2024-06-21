# Setup

We already cloned and compiled [the repository of the of the biLouvain algorithm](https://github.com/paolapesantez/biLouvain) for you. The compiling is done by running the "makefile" file within `./biLouvain/src/`.

## What you have to do for running the algorithm

### On your own
You have two options: If you already have a makefile runner, use that in the `./biLouvain/src/` directory and use a terminal corresponding to your makefile runner.

### Otherwise
#### For Windows with our help
- First go to the [Cygwin install page](https://www.cygwin.com/install.html). And click on "setup-x86_64.exe" to get the installer.
- Once on the **Select Packages** page, make sure that the "View" dropdown is changed to "Full".
- Search for "gcc-g++", click on the dropdown in the column "New" and change "Skip" to a newest version (we used "11.4.0-1").
- *Optional:* if you want to compile your code yourself, do the previous step for the package "make" as well, we used version "4.4.1-2".
  - When you want to compile your own code: open the Cygwin terminal. Go to the project by typing `cd C/[your own path]/INFOMNWSC-Experimental/biLouvain/src` hit enter, and then type `make` and hit enter.
- *Important:* It's useful to make a shortcut in your Windows menu so you can easily open the Cygwin Terminal.


#### For Linux
Linux doesn't need to install anypackage and already has the needed components installed. However, you do need to compile the code yourself:
- In the Terminal. Go to the project by typing `cd C/[your own path]/INFOMNWSC-Experimental/biLouvain/src` hit enter
- Type `make` and hit enter. (if that doesn't work, install the 'make' package first).

#### For MacOS
Both of us don't have a Mac, so we're not entirely sure. But in principle, MacOS has the same instruction as Linux.  
However, does that not work: install a [similar package manager like Cygwin](https://alternativeto.net/software/cygwin/?platform=mac).  
Everything else is quite the same as the installation steps for windows, but use your own package manager instead of Cygwin.

# Running the algorithm
- Open your package manager terminal (if not using Linux).  
- In Terminal: `cd C/[your own path]/INFOMNWSC-Experimental`

#### Running a single case:
- Type: `./biLouvain/src/biLouvain -i input/pollinator_edges.txt -d "," -ci 0.01 -cp 0.00001 -o  output/ResultsSingleRun` => The values after '-ci' and '-cp' can be changed. "pollinator_edges.txt" can be changed to "test.txt" if you want to see if the algorithm can just run.

#### Running all our test cases:
*Note:* This takes about 23 minutes!
- Type: `./execute_all_cases.sh`

## Note
Everytime you want to rerun the algorithm, you have to delete the generated input (not the original) and output files. They won't be updated otherwise.

# Python scripts
You won't have to run the python scripts, but still a short explanation in chronological order:
- `input_prep.py` Used to make the original network graph from the .csv file from 'Center for Plant Conservation', into one that we can use for the biLouvain algorithm.
- `algorithm_prep.py` Used for making a .sh (bash) file that can optionally run the algorithm several times (all the testcases).
- `analyze_output.py` Used for reading the modularity from the output and generating the graph and table that is being used in the paper.
- `analyze_communities.py` Used for identifying the communities from one of the output files and generating the statistical analysis values: both the classification metrics as the confusion matrix.
