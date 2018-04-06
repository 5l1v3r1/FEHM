## FEHM: Finite Element Heat and Mass Transfer Code ##
### No. C13153 LA-CC-2012-083 Open Source ###

The numerical background of the FEHM computer code can be traced to the early 1970s when it was used to simulate geothermal and hot dry rock reservoirs. The primary use over a number of years was to assist in the understanding of flow fields and mass transport in the saturated and unsaturated zones below the potential Yucca Mountain repository. Today FEHM is used to simulate groundwater and contaminant flow and transport in deep and shallow, fractured and un-fractured porous media throughout the US DOE complex. FEHM has proved to be a valuable asset on a variety of projects of national interest including Environmental Remediation of the Nevada Test Site, the LANL Groundwater Protection Program, geologic CO2 sequestration, Enhanced Geothermal Energy (EGS) programs, Oil and Gas production, Nuclear Waste Isolation, and Arctic Permafrost. Subsurface physics has ranged from single fluid/single phase fluid flow when simulating basin scale groundwater aquifers to complex multifluid/ multi-phase fluid flow that includes phase change with boiling and condensing in applications such as unsaturated zone surrounding nuclear waste storage facility or leakage of CO2/brine through faults or wellbores. The numerical method used in FEHM is the control volume method (CV) for fluid flow and heat transfer equations which allows FEHM to exactly enforce energy/mass conservation; while an option is available to use the finite element (FE) method for displacement equations to obtain more accurate stress calculations. In addition to these standard methods, an option to use FE for flow is available, as well as a simple Finite Difference scheme. Visit web pages at [fehm.lanl.gov](http://fehm.lanl.gov)

## License ##

FEHM is distributed as as open-source software under a BSD 3-Clause License. See [Copyright License](LICENSE.md)

## Developers ##

External Collaborators must sign a Contribution Agreement. [Contribution Agreement for External Collaborators](CONTRIBUTING.md)

This Version 3.3.1 from October 2017 has been moved from a mercurial repository on https//fehm.lanl.gov which will be closed.

The following are reminders for FEHM code developers using this repository.

A Git workflow follows these basic steps:
* Make changes to files
* Add the files (‘stage’ files)
* ‘Commit’ the staged files
* Push the commit (containing all modified files) to the central repo
 
1. To first get the repo, run the command

```
git clone https://github.com/lanl/FEHM.git
```

This will download the FEHM Git repo to your current directory.
 
2. Let’s say you’ve done some editing and you’re ready to push your changes to the FEHM repository.
Run the command

```
git add file1 file2 ... fileN
```
 
to add any files you have changed. You can also just run `git add .` if you want to add every changed file.
 
3. Now, run
 
``` 
git status
```
 
This gives an overview of all tracked and untracked files.
A tracked file is one that Git considers as part of the repo.
Untracked files are everything else – think of *.o files, or some test data output generated by an FEHM run.
 
Tracked files can be:
* Unmodified (you haven’t made any changes to it, relative to the last commit)
* Modified (you have edited the file since the last commit)
* Staged (the file has been added and is ready to be committed and then pushed)
 
Untracked files become tracked by using
```
git add filename
```
 
4. After verifying (with `git status`) that all the files you want to be pushed are properly staged, commit them using

```
git commit -m "My first Git commit!"
```
 
Then, push the files onto the GitHub repo with

```
git push origin master
```
 
5. If someone else has made edits, you will need to pull their changes to your local FEHM clone before you can push.
 
```
git pull origin master
git push origin master
```

## FEHM Release Versions ##


See Versions and Notes under the Releases tab this repository.

The Most recent distributed release is FEHM V3.3.1 (December 2017) which is the version cloned for this repository. The FEHM software is a continuation of QA work performed for the Yucca Mountain Project (YMP) under Software Configuration Control Request (SCCR) (Software Tracking Numbers STN: 10086-2.21-00 August 2003, V2.22, STN 10086-2.22-01, V2.23, STN 10086-2.23-00, V2.24-01, STN 10086-2.24-01, and V2.25, STN 10086-2.25-00). 
The QA for these codes started under YMP QA and continue under under LANL EES-16 Software QA Policy and Proceedures as outlined in: "EES-16-13-003.SoftwareProcedure.pdf" 

Before distribution of FEHM software, tests are executed and verified as acceptable on LANL computers with operating systems Linux, Mac OSX, and WINDOWS. The overall validation effort for the FEHM software consists of a suite of directories and scripts that test the model whenever possible, against known analytical solutions of the same problem. The test suite was developed under YMP QA for FEHM RD.10086-RD-2.21-00 and is available for download.
