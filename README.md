# Online Appendix 
This appendix is supplementary material to the SEAMS 2018 submission 
"Adapting a System with Noisy Outputs with Statistical Guarantees"
by Ilias Gerostathopoulos, Christian Prehofer and Tomas Bures. 

## Preliminaries 
We provide here a number of Python scripts, packaged as [jupyter notebooks](http://jupyter.org/), 
used to analyze the application of the cost-aware self-optimization framework 
with statistical guarantees on [CrowdNav](https://github.com/Starofall/CrowdNav) 
self-adaptation exemplar.

The scripts work with data collected from CrowdNav and persisted in different pickle files. 

To run the scripts, follow these steps: 
* Clone or download the current branch (seams18) of this project. _(Please be aware that this might take 
awhile since the repository is ~130 MB)_
* Unzip the file "results-Crowdnav.zip". This should create a new folder 
called "results-CrowdNav" which would be child to the project's parent ("RTX") folder
* Navigate to the parent directory of the project and issue: ```jupyter notebook```.
This will open a new tab in your default browser. 
From here on you can choose to run any notebook from the ones described below. 

To run the code of a single notebook, follow these steps: 
* Click on one notebook; this will open in a new tab
* Run the code cells from top to bottom by issuing ```Shift + Enter``` to each of them

### Software requirements
To run the scripts you need to have the following software installed in your system. 
* Python (tested with version 2.7)
* Jupyter (tested with version 4.4.0). For system-specific installation instructions, 
visit [Installing Jupyter](http://jupyter.org/install) . 
If you have ```pip``` package manager installed in your system, just run the command: 
```python -m pip install --upgrade pip; python -m pip install jupyter``` 

## Generation of System model
In this phase, we run factorial ANOVA in order to determine the input parameters 
with the largest effect on the output of the system. 
 
To try it out, run the scripts in these notebooks: 
* ```analysis-anova-single.ipynb```, for running factorial ANOVA on the data 
from a single CrowdNav situation 
*  ```analysis-anova-merged.ipynb```, for running factorial ANOVA on the data 
from all recorded CrowdNav situations
 
## Runtime optimization with cost handling

In this phase, we run Bayesian optimization with Gaussian processes (BOGP) 
to find an optimal configuration. 
To see the results from the BOGP in our baseline scenario and our 2-stage approach, 
run the scripts in this notebook: 

* ```analysis-BOGP.ipynb```

## Comparison with baseline configuration

In this phase, we check with t-test whether the best configuration found by the previous phase is 
statistically singificantly better than the baseline (default) configuration for this CrowdNav situation.
To see the results, run the scripts in this notebook: 
 
* ```analysis-t-test.ipynb```

## Futher: How to run your own experiments

To run your own experiments, you need to set up kafka, elasticsearch, RTX and CrowdNav, 
as desccribed in the main [RTX readme](https://github.com/Starofall/RTX/tree/master) 
and in this [getting started guide](https://github.com/Starofall/RTX/wiki/RTX-&-CrowdNav-Getting-Started-Guide).

#### _Contact_ 

For questions, contact [Ilias Gerostathopoulos](https://github.com/iliasger) 
at gerostat@in.tum.de  