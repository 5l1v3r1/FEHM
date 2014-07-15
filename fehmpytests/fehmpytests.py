#***********************************************************************
# Copyright 2014 Los Alamos National Security, LLC All rights reserved
# Unless otherwise indicated, this information has been authored by an
# employee or employees of the Los Alamos National Security, LLC (LANS),
# operator of the Los Alamos National Laboratory under Contract No.
# DE-AC52-06NA25396 with the U.S. Department of Energy. The U.S.
# Government has rights to use, reproduce, and distribute this
# information. The public may copy and use this information without
# charge, provided that this  Notice and any statement of authorship are
# reproduced on all copies. Neither the Government nor LANS makes any
# warranty, express or  implied, or assumes any liability or
# responsibility for the use of this information.      
#***********************************************************************
import unittest
import os
import sys
import argparse
import re
import numpy as np
import glob
from subprocess import call
from subprocess import PIPE
try:
    sys.path.insert(0,'../pyfehm')
    import fdata
except ImportError as err:
    print 'ERROR: Unable to import pyfehm fpost module'
    print err
    os._exit(0)

#Suppresses tracebacks
__unittest = True 

class fehmTest(unittest.TestCase):
    """
    Represents a FEHM test-case. 
    
    Initialize with the name of the test-case folder as a string argument.
    Example: test_case = Tests('saltvcon')
    
    To add the test-case to a suite, initialize a suite object, and call
    addTest() with the test-case as an argument.
    Example: suite = unittest.TestSuite()
             suite.addTest(test_case)
              
    Authors: Dylan Harp, Mark Lange
    Updated: June 2014 
    """    
        
    def __init__(self, testname, log):
        """
        Call the unittest constructor then initialize the main directory and
        log switch values and create a fail log if the log switch is turned on.
        
        :param testname: The name of the test method.
        :type name: str
        
        :param log: Switch that determines if a fail log will be generated.
        :type name: bool
        
        .. Authors: Mark Lange
        .. Updated: July 2014
        """
    
        super(fehmTest, self).__init__(testname)
        self.log = log
        
        #If log switch is on, create the fail log file.
        if self.log:
            self.fail_log = open('fail_log.txt', 'w')
        
        self.maindir = os.getcwd()
    
    # TESTS ######################################################### 
        
    def test_saltvcon(self):
        """
        **Test the Salt Variable Conductivity Macro**
         
        Tests the calculations of thermal conductivity of crushed and intact 
        salt.

        Intact salt:
            ``kxi = k_{t-300}(300/T)^1.14``
            *Munson et al. (1990) Overtest for Simulate Defense High-Level*
            *Waste (Room B): In Situ Data Report. WIPP. Sandia National*
            *Laboratories, SAND89-2671*

        Thermal conductivity of crushed salt from Asse mine:
            ``kx_asse = -270*phi^4+370*phi^3-136*phi^2+1.5*phi+5`` 
            *Bechtold et al. (2004) Backfilling and sealing of underground*
            *respositories for radioactive waste in salt 
            *(BAMBUS II project), EUR 20621, ISBN 92-894-7767-9*
            
        ``kx = (k_{t-300}/kx_asse)*(300/T)^1.14`` if kx is less then 1.e-6, set 
        to 1.e-6.

        The excel spreadsheet /information/saltvcon.xlsx contains the
        associated calculations. 
        
        .. Authors: Dylan Harp, Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['components'] = ['water']
        arguments['variables']  = ['Kx']
        arguments['format'] = 'relative' 
        
        #test_case() does not actually display this custom error message yet.
        arguments['err_msg'] = \
            '\nIncorrect intact salt thermal conductivity for node %s \
             \nRelative error: %s, Threshold: %s \
             \nExpected = %s Simulated = %s'
        
        self.test_case('saltvcon', arguments)
        
        
    def test_dissolution(self):
        """ 
        **Test the Dissoultion Macro**
        
        A one-dimensional transport simulation of calcite (CaC03(s)) 
        dissolution is tested. Profiles of concentration versus reactor 
        length, at selected times, will be compared against the analytical 
        solution.

        Details of this test are described in the FEHM V2.21 Validation Test 
        Plan on pages 93-95 *(STN: 10086-2.21-00, Rev.No. 00, Document ID: 
        10086-VTP-2.21-00, August 2003)* 
        
        .. Authors: Dylan Harp, Mark Lange    
        .. Updated: June 2014 by Mark Lange          
        """
    
        arguments = {}
        arguments['variables'] = ['Np[aq] (Moles/kg H20)']
        
        #test_case() does not actually display this custom error message yet.
        arguments['err_msg'] = '\nIncorrect concentration at time %s'
        
        self.test_case('dissolution', arguments)
        
    def test_salt_perm_poro(self):
        """ 
        **Test the Salt Permeability and Porosity Macro**

        The porosity-permeability function for compacted salt from *Cinar et 
        at. (2006)* is tested using a six node problem with porosities from 
        0.01 to 0.2. The excel spreadsheet in information/salt-perm-poro.xlsx 
        contains calculations of the perm-poro function.

        *Cinar, Y, G Pusch and V Reitenbach (2006) Petrophysical and 
        capillary properties of compacted salt. Transport in Porous Media. 
        64, p. 199-228, doi: 10.1007/s11242-005-2848-1* 
        
        .. Authors: Dylan Harp, Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
    
        arguments = {}
        arguments['variables'] = ['n', 'perm_x']
        
        #test_case() does not actually display this custom error message yet.
        arguments['err_msg'] = \
            '\nIncorrect permeability at node %s. Expected %s, Simulated '    
        
        self.test_case('salt_perm_poro', arguments)
  
    def test_avdonin(self):
        """
        **Test the Radial Heat and Mass Transfer Problem**
        
        Compares the generated contour and history files to old contour and 
        history files that are known to be correct. For contour files, only the
        temperature values at time 2 are tested. For history files, all 
        temperature values are tested. 
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange    
        """
        
        arguments = {}
        arguments['times'] = [2.0]
        arguments['variables'] = ['T']
        
        self.test_case('avdonin', arguments)
        
    def test_boun(self): 
        """
        **Test the Boundry Functionality**
        
        Compares the generated contour files to old contour files that are known
        to be correct. Only the pressure and hydraulic head values at time 2 are 
        tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['times'] = [2.0]
        arguments['variables'] = ['P', 'Hydraulic Head (m)']

        self.test_case('boun_test', arguments) 
        
    def test_cden(self):
        """
        **Test the Concentration Dependent Brine Density Functionality**
        
        Compares generated history files to old history files that are known to 
        be correct. Only the density values are tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['variables'] = ['density']
         
        self.test_case('cden_test') 
        
    def test_doe(self):
        """
        **Test the DOE Code Comparison Project, Problem 5, Case A**
        
        Compares the generated contour and history files to old contour and
        history files that are known to be correct. For contour files, only the
        pressure, temperature, and saturation values at time 3 are tested. For 
        history files, all pressure, temperature, and saturation values are 
        tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['times'] = [3.0]
        arguments['variables'] = ['P', 'T', 'saturation']
        
        self.test_case('doe', arguments)
        
    def test_head(self):
        """
        **Test Head Pressure Problem**
        
        Compares the generated contour files to old contour files that are known
        to be correct. Only the pressure values at day 2 are tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange 
        """
        
        arguments = {}
        arguments['times'] = [2.0]
        arguments['variables'] = ['P']
        
        self.test_case('head', arguments)
                    
    def test_ramey(self):
        """
        **Test Temperature in a Wellbore Problem**
        
        Compares the generated contour and history files to old contour and
        history file that are known to be correct. For the contour files, only 
        the temperature values at time 2 are tested. For the history files, all 
        temperature values are tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['times'] = [2.0]
        arguments['variables'] = ['T']
        
        self.test_case('ramey', arguments)
   
    def test_theis(self):
        """
        **Test Pressure Transient Analysis Problem**
        
        Compares the generated contour files to old contour files known to be 
        correct. Only the pressure values at time 2 are tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        arguments = {}
        arguments['times'] = [2.0]
        arguments['variables'] = ['P']
        
        self.test_case('theis', arguments)
        
    def test_dryout(self):
        """
        **Test Dry-Out of a Partially Saturated Medium**
        
        Compares the generated contour files to old contour files known to be 
        correct. The saturation is tested for all times.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange 
        """
        
        arguments = {}
        arguments['variables'] = ['saturation']
        
        self.test_case('dryout')
        
    def test_multi_solute(self):
        """
        **Test Multi-Solute Transport with Chemical Reaction**
        
        Compares the generated tracer files to old tracer files known to be 
        correct. All concentraction values are tested.
        
        .. Authors: Mark Lange
        .. Updated: June 2014 by Mark Lange
        """
        
        self.test_case('multi_solute')
        
    def test_sorption(self):
        """
        **Test One Dimensional Reactive Solute Transport**
        
        Compares the generated tracer files to old tracer files known to be
        correct. All concentraction values are tested.
        
        .. Authors: Mark Lange
        .. Updated: June  2014 by Mark Lange
        """
        
        self.test_case('sorption')
        
    def test_baro_vel(self):
        """
        **Test Pore-Scale Velocity in a Homogeneous Media**
        
        Compares the generated contour files with the old files known to be
        correct. Tests times 3-6 for a root mean square difference of less than 
        0.01.
        
        .. Authors: Mark Lange
        .. Updated: July 2014 by Mark Lange
        """
        
        args = {}
        args['test_measure'] = 'rms_difference'
        args['maxerr'] = 0.01
        args['times'] = [3.0, 4.0, 5.0, 6.0]
        
        self.test_case('baro_vel', args)
                
    # Test Developer Functionality ############################################
        
    def test_case(self, name, parameters={}):
        """ 
        Performs a test on a FEHM simulation and raises an AssertError if it 
        fails the test. 
         
        :param name: The name of the test-case folder.
        :type name: str
        
        :param parameters: Attribute values that override default values.
        :type parameters: dict
            
        The folder 'name' in fehmpytests must exist with correct structure.
        If parameters are not passed into this method, all simulated attributes 
        will be checked for a relative difference of less than 1.e-4. 
        
        Authors: Mark Lange
        Updated: June 2014 by Mark Lange                                
        """ 
         
        os.chdir(name)
        
        #Search for fehmn control files and extract subcases.
        filenames = glob.glob('input/control/*.files')
        subcases  = []
        for filename in filenames:
            subcase = re.sub('input/control/', '', filename)
            subcase = re.sub('.files', '', subcase)
            
            #File named 'fehmn.files' to be used for tests with single case.
            if subcase != 'fehmn':
                subcases.append(subcase)
            else:
                subcases = ['']
                break
                
        try:
            #Test the new files generated with each subcase.
            for subcase in subcases:
                parameters['subcase'] = subcase
                filetypes = ['*.avs', '*.csv', '*.his', '*.out', '*.trc']
                for filetype in filetypes:
                    parameters['filetype'] = filetype
                    #Check to make sure there are files of this type.
                    if len(glob.glob('compare/'+'*'+subcase+filetype)) > 0: 
                        test_method = \
                          self._test_template(filetype, subcase, parameters)
                        test_method()
                                        
        finally:
            #Allows other tests to be performed after exception.
            cleanup(['*.*'])
            os.chdir(self.maindir)
            
    def _test_template(self, filetype, subcase, parameters={}):
        """
        **Test Template**
        
        Calling this function with the filename and subcase will return the 
        correct test method. 
        
        :param parameters: Stores optional prespecified variable, time, node, 
                           component, and format values to override defaults.
        :type filesfile:   dict 
        
        The intent behind creating this method was to make it pythonic. If you 
        need to modify this function and need help understanding it, look into
        'closure' and functions as 'first class objects'.
        """
            
        #Get pre-specified parameters from call.
        keys = ['variables', 'times', 'nodes', 'components']
        values = dict.fromkeys(keys, [])
        values['maxerr'] = 1.e-4
        values['test_measure'] = 'max_difference'
        for key in values:
            if key in parameters:
                values[key] = parameters[key]                      
        mxerr = values['maxerr']
        components = values['components']
        test_measure = values['test_measure']
        
        self._run_fehm(subcase)
        
        def contour_case():      
            #Find the difference between the old and new
            f_old = fdata.fcontour('compare/*'+subcase+filetype) 
            f_new = fdata.fcontour('*'+subcase+filetype)
            f_dif = fdata.fdiff(f_new, f_old)

            msg = 'Incorrect %s at time %s.'
            
            #If no pre-specified times, grab them from f_dif.
            if len(values['times']) == 0:
                times = f_dif.times
            else:
                times = values['times']
            
            #If no pre-specified variables, grab them from f_dif.         
            if len(values['variables']) == 0:
                variables = f_dif.variables
            else:
                variables = values['variables']
            
            #Check the variables at each time for any significant differences.
            for t in times: 
                #Its possible some times do not have all variables in f_dif.
                for v in np.intersect1d(variables, f_dif[t]):
                    #Measure the difference into a single quantity.
                    f_dif[t][v] = map(abs, f_dif[t][v])
                    difference = { 
                        'max_difference': max(f_dif[t][v]),
                        'rms_difference': np.sqrt(np.mean(f_dif[t][v])) 
                    }[test_measure]
                    try:
                        self.assertTrue(difference<mxerr, msg%(v, t))
                    except AssertionError as e:
                        #Write to fail log if switch is on.
                        if self.log:
                            kvpairs = {'variable':str(v), 'time':str(t)}
                            line = 'Failed at subcase:'+subcase
                            line = line+' filetype:'+filetype
                            for key in kvpairs:        
                                line = line+' '+key+':'+kvpairs[key]
                            self.fail_log.write(line)   
                        raise e
                      
        def history_case():
            #Find the difference between the old and new
            f_old = fdata.fhistory('compare/*'+subcase+filetype) 
            f_new = fdata.fhistory('*'+subcase+filetype)
            f_dif = fdata.fdiff(f_new, f_old)
            
            #If no pre-specified variables, grab them from f_dif.         
            if len(values['variables']) == 0:
                variables = f_dif.variables
            else:
                variables = values['variables']
            
            #If no pre-specifed nodes, grab them from f_dif.
            if len(values['nodes']) == 0:
                nodes = f_dif.nodes
            else:
                nodes = values['nodes']   
               
            msg = 'Incorrect %s at node %s.'  
            
            #Check the nodes at each variable for any significant differences.   
            for v in variables:
                #Its possible some variables do not have all nodes in f_dif.
                for n in np.intersect1d(nodes, f_dif[v]):  
                    f_dif[v][n] = map(abs, f_dif[v][n])
                    difference = { 
                        'max_difference': max(f_dif[v][n]),
                        'rms_difference': np.sqrt(np.mean(f_dif[v][n])) 
                    }[test_measure]
                    try:   
            	        self.assertTrue(difference<mxerr, msg%(v, n))
            	    except AssertionError as e:
                        #Write to fail log if switch is on.
                        if self.log:
                            kvpairs = {'variable':str(v), 'node':str(n)}
                            line = 'Failed at subcase:'+subcase
                            line = line+' filetype:'+filetype
                            for key in kvpairs:        
                                line = line+' '+key+':'+kvpairs[key]
                            self.fail_log.write(line)   
                        raise e
            	    
        def tracer_case():
            #Find the difference between the old and new
            f_old = fdata.ftracer('compare/*'+subcase+filetype) 
            f_new = fdata.ftracer('*'+subcase+filetype)
            f_dif = fdata.fdiff(f_new, f_old)
            
            #If no pre-specified variables, grab them from f_dif.         
            if len(values['variables']) == 0:
                variables = f_dif.variables
            else:
                variables = values['variables']
            
            #If no pre-specifed nodes, grab them from f_dif.
            if len(values['nodes']) == 0:
                nodes = f_dif.nodes
            else:
                nodes = values['nodes']    

            msg = 'Incorrect %s at node %s.'  
            
            #Check the nodes at each variable for any significant differences.   
            for v in variables:
                #Its possible some variables do not have all nodes in f_dif.
                for n in np.intersect1d(nodes, f_dif[v]):
                    #Measure the difference into a single quantity.
                    f_dif[v][n] = map(abs, f_dif[v][n])
                    difference = { 
                        'max_difference': max(f_dif[v][n]),
                        'rms_difference': np.sqrt(np.mean(f_dif[v][n])) 
                    }[test_measure]     
                    try:
            	        self.assertTrue(difference<mxerr, msg%(v, n))
            	    except AssertionError as e:
                        #Write to fail log if switch is on.
                        if self.log:
                            kvpairs = {'variable':str(v), 'node':str(n)}
                            line = 'Failed at subcase:'+subcase
                            line = line+' filetype:'+filetype
                            for key in kvpairs:        
                                line = line+' '+key+':'+kvpairs[key]
                            self.fail_log.write(line)   
                        raise e   
            
        def output_case():
            #Find difference between old and new file assume 1 file per subcase.
            old_filename = glob.glob('compare/*'+subcase+filetype)[0]
            new_filename = glob.glob('*'+subcase+filetype)[0]
            f_old = fdata.foutput(old_filename)
            f_new = fdata.foutput(new_filename)
            f_dif = fdata.fdiff(f_new, f_old)
            
            #If no pre-specified variables, grab them from f_dif.         
            if len(values['variables']) == 0:
                variables = f_dif.variables
            else:
                variables = values['variables']

            #If no pre-specifed nodes, grab them from f_dif.
            if len(values['nodes']) == 0:
                nodes = f_dif.nodes
            else:
                nodes = values['nodes']
                
            msg = 'Incorrect %s at %s node %s.'  
            
            #Check the node at each component for significant differences.   
            for c in components:
                for n in nodes:
                    for v in variables:
                        #Measure the difference into a single quantity.
                        fdiff_array = map(abs, f_dif.node[c][n][v])
                        difference = { 
                            'max_difference': max(fdiff_array),
                            'rms_difference': np.sqrt(np.mean(fdiff_array)) 
                        }[test_measure]
                        try:
                            self.assertTrue(difference < mxerr, msg%(v,c,n))
                        except AssertionError as e:
                            #Write to fail log if switch is on.
                            if self.log:
                                kvpairs = { 'component': str(c), 
                                            'node': str(n),
                                            'variable': str(v), }
                                line = 'Failed at subcase:'+subcase
                                line = line+' filetype:'+filetype
                                for key in kvpairs:        
                                    line = line+' '+key+':'+kvpairs[key]
                                self.fail_log.write(line)   
                            raise e
        
        #Returns the test method for filetype.
        return { '*.avs': contour_case,
                 '*.csv': contour_case,
                 '*.his': history_case,
                 '*.trc': tracer_case,
                 '*.out': output_case, }[filetype]
                                    
    def _run_fehm(self, subcase):
        """ 
        **Utility function to run fehm**
        
        Asserts that fehm terminates successfully.

        :param filesfile: name of fehm files file
        :type filesfile: str 
        """
        
        #Find the control file for the test-case or for the subcase. 
        if subcase == '':
            filesfile = 'input/control/fehmn.files'
        else:
            filesfile = 'input/control/'+subcase+'.files'
            
        call(exe+' '+filesfile, shell=True, stdout=PIPE)
        outfile = None
        errfile = 'fehmn.err'

        with open( filesfile, 'r' ) as f:
            lines = f.readlines()
            # Check for new filesfile format
            for line in lines:
                if 'outp' in line:
                    outfile = line.split(':')[1].strip()
                elif 'error' in line:
                    errfile = line.split(':')[1].strip()
                           
            # Assume old format
            if outfile is None and ':' not in lines[0]: 
                outfile=lines[3].strip()
 
        complete = False
        if outfile:
            with open(outfile, 'r' ) as f:
                for line in reversed(f.readlines()):
                    if 'End Date' in line:
                        complete = True
                        break
                        
        if os.path.exists(errfile): 
            errstr = open( errfile, 'r' ).read()
        else: 
            errstr = ''
            
        # Change to maindir in case assertTrue fails    
        curdir = os.getcwd() 
        os.chdir(self.maindir)
        
        msg = 'Unsuccessful fehm simulation\nContents of '
        self.assertTrue(complete, msg+errfile+':\n\n'+errstr)
        os.chdir(curdir)
                     
def cleanup(files):
    """ 
    Utility function to remove files after test

    :param files: list of file names to remove
    :type files: lst(str) 
    """
        
    for g in files:
        for f in glob.glob(g):
            if os.path.exists(f): os.remove(f)
                  
def suite(mode, test_case, log):
    suite = unittest.TestSuite()
    
    #Default mode is admin for now. Should it be different?
    if mode == 'admin' or mode == 'default':
        suite.addTest(fehmTest('test_saltvcon', log))
        suite.addTest(fehmTest('test_dissolution', log))
        suite.addTest(fehmTest('test_salt_perm_poro', log))
        suite.addTest(fehmTest('test_avdonin', log))
        suite.addTest(fehmTest('test_boun', log))
        suite.addTest(fehmTest('test_cden', log))
        suite.addTest(fehmTest('test_doe', log))       
        suite.addTest(fehmTest('test_head', log))
        suite.addTest(fehmTest('test_ramey', log))
        suite.addTest(fehmTest('test_theis', log))
        suite.addTest(fehmTest('test_dryout', log))
        suite.addTest(fehmTest('test_multi_solute', log))
        suite.addTest(fehmTest('test_sorption', log))
        suite.addTest(fehmTest('test_baro_vel', log))
        
        #TODO - Look into why this test takes so long.
        #suite.addTest(fehmTest('test_evaporation', log))
        
        #TODO - Figure out how to read some other formats.
        #suite.addTest(fehmTest('test_sptr_btc', log))
        #suite.addTest(fehmTest('test_sorption', log))
        #suite.addTest(fehmTest('test_particle_capture', log))
        #suite.addTest(fehmTest('test_mptr', log))
        #suite.addTest(fehmTest('test_lost_part', log))
        #suite.addTest(fehmTest('test_chain', log))
        #suite.addTest(fehmTest('test_co2test', log))
        #suite.addTest(fehmTest('test_convection', log))
        #suite.addTest(fehmTest('test_dpdp_rich', log))
        #suite.addTest(fehmTest('test_erosion', log))
        #suite.addTest(fehmTest('test_gdpm', log))
        #suite.addTest(fehmTest('test_forward', log))
    
    elif mode == 'developer':
        #This mode will be a reduced set that runs faster.
        pass
             
    elif mode == 'solo':
        suite.addTest(fehmTest(test_case, log))
            
    elif mode == 'admin':
        pass
        
    return suite
        
if __name__ == '__main__':
    
    #Unless the user specifies a single test-case, this isn't important.
    test_case = ''

    #Set up command-line interface.
    parser = argparse.ArgumentParser(description='FEHM Test-Suite')
    
    #Comand-line Options
    group = parser.add_mutually_exclusive_group()   
    a = 'store_true'
    h = 'Run the entire test-suite.'
    group.add_argument('-a', '--admin', help=h, action=a)
    h = 'Run a portion of the test-suite.'
    group.add_argument('-d', '--dev', help=h, action=a)
    h = 'Run a single test-case.'
    group.add_argument('-s', '--solo', help=h, action=a)
    
    h = "Create a fail statistics file 'fail_log.txt'"
    parser.add_argument('-l', '--log', help=h, action=a)
    
    #Positional Arguments
    h = 'Path to the FEHM executable.'
    parser.add_argument('exe', help=h)
    h = 'Single test-case to run.'
    parser.add_argument('testcase', nargs='?', help=h, default=None)
     
    args = vars(parser.parse_args())
    
    exe = os.path.abspath(args['exe'])
    
    #Determine the mode.    
    if args['solo']:
        #Make sure that the test-case was specified, otherwise show help.
        if args['testcase'] != None:
            mode = 'solo'
            test_case = args['testcase']
        else:
            parser.print_help()   
    else:
        #Make sure user did not attempt to specify a test-case, show help if so.
        if args['testcase'] == None:
            if args['admin']:
                mode = 'admin'
            elif args['dev']:
                mode = 'developer'
            else:
                mode = 'default'
        else:
            #If user didn't specify admin or dev, assume solo mode.
            if not args['admin'] and not args['dev']:
                mode = 'solo'
                test_case = args['testcase']
            else:       
                parser.print_help()
                
    #If the user wants a log, give them a log.
    log = False            
    if args['log']:
        log = True
    
    #Run the test suite.    
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite(mode, test_case, log)
    runner.run(test_suite)



