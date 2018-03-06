## FEHM: Finite Element Heat and Mass Transfer Code ##
### LA-CC-2012-083 Export control on source code ###

This repository is limited to FEHM team and collaborators with a LANL approved and signed Contributor Agreement.
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


See Versions and Notes under the Releases tab this repository.

The Most recent distributed release is FEHM V3.3.1 (December 2017) which is the version cloned for this repository. The FEHM software is a continuation of QA work performed for the Yucca Mountain Project (YMP) under Software Configuration Control Request (SCCR) (Software Tracking Numbers STN: 10086-2.21-00 August 2003, V2.22, STN 10086-2.22-01, V2.23, STN 10086-2.23-00, V2.24-01, STN 10086-2.24-01, and V2.25, STN 10086-2.25-00). 
The QA for these codes started under YMP QA and continue under under LANL EES-16 Software QA Policy and Proceedures as outlined in: "EES-16-13-003.SoftwareProcedure.pdf" 

Before distribution of FEHM software, tests are executed and verified as acceptable on LANL computers with operating systems Linux, Mac OSX, and WINDOWS. The overall validation effort for the FEHM software consists of a suite of directories and scripts that test the model whenever possible, against known analytical solutions of the same problem. The test suite was developed under YMP QA for FEHM RD.10086-RD-2.21-00 and is available for download.

FEHM Code source is export controlled with the following Copyright:

**Copyright 2013. Los Alamos National Security, LLC for FEHM LA-CC-2012-083.** This material was produced under U.S. Government contract DE-AC52-06NA25396 for Los Alamos National Laboratory (LANL), which is operated by Los Alamos National Security, LLC for the U.S. Department of Energy. The U.S. Government has rights to use, reproduce, and distribute this software. Neither the U.S. Government nor Los Alamos National Security, LLC or persons acting on their behalf, make any warranty, express or implied, or assumes any liability for the accuracy, completeness, or usefulness of the software, any information pertaining to the software, or represents that its use would not infringe privately owned rights.  

The licensed software, FEHM, may be Export Controlled. It may not be distributed or used by individuals or entities prohibited from having access to the software package, pursuant to United States export control laws and regulations. An export control review and determination must be completed before LANS will provide access to the identified Software. 

*Distribution of FEHM source code is limited to FEHM team collaborators with a LANS approved and signed Contributor Agreement. Contact Terry Miller tamiller@lanl.gov or an FEHM team member for more information.*
