# On 64-bit system:

# source /home/gbt/sparrow/sparrow.bash

import numpy as np
import re
import os
from gbt.turtle.user import Catalog

class Project:

    def __init__(self):

        # Do I want to make this into one big dictionary instead of 3 separate dictionaries?

        # general project info
        self.project_info = {'project_id': "",        # AGBT13B_306            
                             'catalog_location': "",  # /path/to/filename
                             'backend_preset': "",    # short name for preset or other if not using a preset
                             'observing_method': "",  # nod (nodding), psw (position switching), fsw (frequency switching).
                             'map': False}            # True if map, False otherwise. Can't have map=True and observing_method='nod'

        # use the astrid catalog class for this
        self.catalog_info = Catalog()

        # Backend info
        # These are taken from the configuration keywords for astrid. I probably don't need them all.
        self.backend_info = {'receiver':'', # Rcvr1_2, etc
                             'backend': '', # Spectrometer
                             'obstype': '', # Spectroscopy
                             'restfreq': 0.0, # MHz
                             'bandwidth': 0.0 , # 12.5, 50, 200, 800 MHz for Spectrometer
                             'swmode': '', # tp, tp_nocal, sp, sp_nocal (either want tp or sp)
                             'swtype': '', # only used when sp. none, fsw, bsw, psw
                             'swper': 0.0, # switching cycle in seconds 
                             'swfreq':(), # switching frequency
                             'tint': 0.0, # integration time in seconds
                             'beam': '', # B1, B2, B3, B4, B12, etc. # Can probably set based on the receiver and the mapping.
                             'nwin': 0, #1,2,3 
                             # 'deltafreq': '', probably don't need this
                             # 'vlow': '', # Can figure out from catalog or set to zero. Which is safer?
                             # 'vhigh':'', # Can figure out from catalog or set to zero. Which is safer?
                             # 'vframe': '', # Can figure out from catalog. don't set here?
                             # 'vdef': '', # Can figure out from catalog. don't set here?
                             'nchan': '', # low, medium, high. Can I always just set this to high?
                             'spect.levels': ''} # 3 or 9. for 200 and 800 MHz only have 3 level sampling
    

    def display_welcome_message(self):

        """
        Purpose: display a welcome message

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code
        """

        ## will want to update this for new way I'm doing the script.

        print """

        Welcome to the automatic GBT script generator!

        To use this program, you will need to have

                1.) A catalog file. An example catalog file can be
                found in /home/astro-util/projects/simple on the GBT systems.

                2.) your project ID code, which can be found on the cover-sheet of your proposal, 

                3.) what observing mode you would like to use.

        Only the most common simple GBT observing modes are available
        in this tool. If you want to use a more complex observing
        mode, you could use this tool to create scripts and then
        modify the scripts to suit your purposes.

        """
    

    def get_project_id(self):

        """
        Purpose: obtain project id from user
        
        Input: user inputs project ID
        
        Output: set project ID in project_info dictionary
            
        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """
        
        # get the project ID from the user and check to make sure it is a valid format.
        while True:
            project_id = raw_input("Input Project ID Number (i.e., AGBT13A_306): ")
            
            # accept both regular (AGBT13A_253) and test projects (TGBT13A_253)                
            if re.match("[T,A]GBT\d\d\D_\d\d\d",project_id):
                break
            else:
                print "Project ID number must be of the form: AGBT13A_306 or TGBT13B_223"
                
        # set the name of the script in the project_info structure
        self.project_info['project_id'] = project_id
        
   
    def get_user_catalog(self):

        """
        Purpose: get the location of the user's catalog.

        Input: user catalog location

        Output: set catalog location in project_info

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        while True:
            catalog_location = raw_input("Enter the location of your catalog: ")

            if os.path.isfile(catalog_location):
                break
            else:
                print "Could not open catalog"                

        self.project_info['catalog_location'] = catalog_location
            
    def read_catalog(self):

        """
        Purpose: read in user catalog. I'm using the astrid catalog reader to read the catalog

        Input: GBT catalog file

        Output: set coordinates in catalog dictionary.

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        11/8/2013   A.A. Kepley     Modified to use astrid catalog reading function
        """

        self.catalog_info = Catalog(self.project_info['catalog_location'])        

        
    def setup_observations(self):
        
        """
        Purpose: set up integration time, offsets, and/or maps sizes if the user hasn't already
        

        Date       Programmer      Description of Changes
        ----------------------------------------------------------------------
        11/8/2013  A.A. Kepely     Original Code
        """
        
        self.map_or_point()

        if self.project_info['map'] is False :
            self.check_integration_time()
            if self.project_info['observing_method'] is 'psw':
                self.check_psw_offset()
        else:
            self.check_map_size()


    def map_or_point(self):
        
        """ 
        Purpose: ask user if they want to map.
        
        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        11/12/2013      A.A. Kepley             Original Code
        """
        # get the project ID from the user and check to make sure it is a valid format.
        while True:
            map_or_point = raw_input("Do you want to map your source [Y/N]?")
           
            if map_or_point in ['Y','y','yes']:
                self.project_info['map'] = True
                break
            elif map_or_point in ['N','n','no']:
                self.project_info['map'] = False
                break
            else:
                print "Enter Y or N."

        
    def check_integration_time(self):

        """
        Purpose: check integration time and if it isn't set have user set it.

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley             Original Code
        """

        defaultint = None

        for src in self.catalog_info.keys(): 
            if 'INT' not in self.catalog_info[src].keys():
                if not defaultint:
                    defaultint = self.get_integration_time()
                self.catalog_info[src]['INT'] = defaultint
                    

    def get_integration_time(self):
        
        """
        Purpose: get integration time
        
        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        11/8/2013       A.A. Kepley             Original Code
        """

        while True:
            prompt = """
                    Enter the integration time per source in seconds:
                    """

            int_time = raw_input(prompt)

            if float(int_time):
                return float(int_time)
            
            # Probably want some more logic here to make sure that the
            # integration time is okay.
        
    def check_psw_offset(self):

        """
        Purpose: get to see if the user hasn't set up the offset yet and let them set if if they need it.

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        11/12/2013      A.A. Kepley             Original Code

        """
    
        defaultoffset = None

        for src in self.catalog_info.keys(): 
            if 'LONG_OFFSET' or 'LAT_OFFSET' not in self.catalog_info[src].keys():
                if not defaultoffset:
                    defaultoffset = self.get_psw_offset()
                self.catalog_info[src]['LONG_OFFSET'] = defaultoffset
                self.catalog_info[src]['LAT_OFFSET'] = defaultoffset
            

    def get_psw_offset(self):

        """
        Purpose: have user set the offset that they want to use for position switching

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley             Original Code
        """
        
        # estimate of beam size in arcmin, not taking into account
        # redshift of source. If there is a substantial redshift, then
        # this will shift the assumed beam size.
        beam_size = 1.2 * 206265.0 * 3e8 /( self.backend_info['restfreq'] * 1e6 * 100.0) / 60.0

        while True:
            prompt = "Enter the offset you would like for the OFF position in arcmin. The suggested offset for your observing frequency is " + str(3.0*beam_size) + "\n"

            psw_offset = raw_input(prompt)

            if float(psw_offset):
                return float(psw_offset)
            
            # Probably want some more logic here to make sure that the
            # offset is okay.
        

    def check_map_size(self):
        
        """
        Purpose: check map size for source

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        11/12/2013      A.A. Kepley             Original Code

        """
        defaultlatsize = None
        defaultlongsize = None

        for src in self.catalog_info.keys(): 
            if 'LONG_SIZE'  not in self.catalog_info[src].keys():
                if not defaultlongsize:
                    defaultlongsize = self.get_map_size('long')
                self.catalog_info[src]['LONG_SIZE'] = defaultlongsize
            if 'LAT_SIZE'  not in self.catalog_info[src].keys():
                if not defaultlatsize:
                    defaultlatsize = self.get_map_size('lat')
                self.catalog_info[src]['LAT_SIZE'] = defaultlatsize


    def get_map_size(self, lat_or_long):

        """
        Purpose: have user set the offset that they want to use for position switching
        
        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley             Original Code
        """
        
        # estimate of beam size in arcmin, not taking into account
        # redshift of source. If there is a substantial redshift, then
        # this will shift the assumed beam size.
        beam_size = 1.2 * 206265.0 * 3e8 /( self.backend_info['restfreq'] * 1e6 * 100.0) / 60.0

        if lat_or_long is 'lat':
            direction = 'latitude'
        else:
            direction = 'longitude'

        while True:
            prompt = "Enter the size of the map in the " + direction + " direction in arcmin.\n"

            map_size = raw_input(prompt)

            if float(map_size):
                return float(map_size)

        # probably should do some checks to make sure that the size of
        # the map is reasonable (not too big or too small).

    def get_backend_preset(self):

        """
        Purpose: have the user select which backend present they want to use

        Output: backend structure with appropriate values for preset

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

    
        while True:

            prompt = """
                Select the desired backend configuration
                1.) Extragalactic neutral hydrogen (HI)
                """

            backend_preset = int(raw_input(prompt))

            if backend_preset == 1:
                self.project_info['backend_preset'] = 'ExGalHI'
                break
            else:
                print "Not a valid selection"


                
    def setup_backend(self):

        """
        Purpose: set defaults for backend configuration. 

        Output: backend structure with values set.

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
            """

        if self.project_info['backend_preset'] == 'ExGalHI':

            self.project_info['observing_method'] = 'psw' # position switching
            self.backend_info['receiver'] = 'Rcvr1_2'
            self.backend_info['obstype'] = 'Spectroscopy'
            self.backend_info['backend'] = 'Spectrometer'
            self.backend_info['restfreq'] =  1420.405752 # Double-check this number
            self.backend_info['bandwidth'] = 12.5 # MHz
            self.backend_info['swmode'] = 'tp'
            self.backend_info['swper'] = 1.0 # s
            self.backend_info['tint'] = 4.0 # s
            self.backend_info['nwin'] = 1
            self.backend_info['nchan'] = 'high'
            self.backend_info['spect.levels'] = 9

        else:
            print "not a valid backend preset"
  

    def print_backend_config(self):

        """
        Purpose: print out backend configuration for observing

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code

        """

        filename = self.project_info['project_id'] + '.config'

        try:
            f = open(filename, 'w')
        except:
            print "Could not open filename"

        f.write('myconfig="""\n')

        # how do i want to deal with switching frequencies here?
        for key in self.backend_info.keys():
            if self.backend_info[key]:
                if type(self.backend_info[key]) is str:
                    f.write(key+'="'+str(self.backend_info[key])+'"\n')
                elif type(self.backend_info[key]) is tuple:
                    param_string = ""
                    for i in self.backend_info[key]:
                        param_string = param_string + str(self.backend_info[key][i]) + ','
                        f.write(key+"="+param_string+"\n")
                else:
                    f.write(key+"="+str(self.backend_info[key])+"\n")
                
        f.write('"""\n')

        f.close()

    def write_script_header(self,f):

        """
        Purpose: write catalog header to file

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        11/12/2013      A.A. Kepley             Original
        """

        configfile = self.project_info['project_id'] + '.config'
        catfile = self.project_info['catalog_location']
        mypath = os.getcwd() # assumes I'm running on the GBT systems.

        f.write("#Configuration file\n")
        f.write("execfile('"+mypath+"/"+configfile+"')\n")
        f.write("\n")
                
        f.write("# Catalog files including official flux calibrators and pointing calibrators for the GBT\n")
        f.write("Catalog('" + mypath+ "/" + catfile + "')\n")
        f.write("Catalog(fluxcal)\n")
        f.write("Catalog(pointing)\n")
        f.write("\n")


    def print_focus_script(self):

        """
        Purpose: print out focus script

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code

        """

        
        filename = self.project_info['project_id'] + '_focus.obs'

        try:
            f = open(filename, 'w')
        except:
            print "Could not open filename"
            
        self.write_script_header(f)

        srcs = self.catalog_info.keys()

        f.write("# Slewing to source. Change src variable to point and focus near another source \n")
        f.write("src = '" + srcs[0] + "'\n")
        f.write("Slew(src)\n")
        f.write("\n")
        
        f.write("# Automatically use a pointing and focus calibrator near the desired source\n")
        f.write("Configure(myconfig)\n")
        f.write("AutoPeakFocus(src)\n")
        f.write('Break("Check pointing and focus")\n')
        f.write("\n")

        f.write("# Go back to source, configure, and balance \n")
        f.write("Slew(src)\n")
        f.write("Configure(myconfig) # need to do because AutoPeakFocus changes the backend configuration\n")
        f.write("Balance()\n")
        f.write('Break("Check balance")\n')
        f.write("\n")
        
        f.close()


    def print_observing_script(self):

        """
        Purpose: print out observing script


        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        if self.project_info['map'] == True:
            self.print_mapping_script()
        else:
            self.print_single_pointing_script()

    def print_mapping_script(self):

        """
        Purpose: print out mapping observing script

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code
        11/12/2013      A.A. Kepley     Updated to actually include code 
        """
        
        beam_size = 1.2 * 206265.0 * 3e8 /( self.backend_info['restfreq'] * 1e6 * 100.0) / 60.0 # arcmin

        # for each source in catalog create observing script need to
        # ask for the integration time if you don't already have
        # it. probably write an extra function to do this.
        for src in self.catalog_info.keys():

            delta = beam_size/2.4

            longoffsetobject = "Offset('" + self.catalog_info[src]['coordmode'] + "'," + str(self.catalog_info[src]['LONG_SIZE']/60.0) + ",0.0)"
            latoffsetobject = "Offset('" + self.catalog_info[src]['coordmode'] + "',0.0," + str(self.catalog_info[src]['LAT_SIZE']/60.0) + ")"
            
            for maptype in ['RALongMap','DecLatMap']:

                filename = self.project_info['project_id'] + '_' + src + '_' + maptype + '.obs'
                try:
                    f = open(filename, 'w')
                except:
                    print "Could not open filename"
                    
                self.write_script_header(f)

                f.write("# Slewing to source.  \n")
                f.write("src = '" + src + "'\n")
                f.write("Slew(src)\n")
                f.write("\n")

                # ADD CONFIG AND BALANCE STATEMENT HERE???
                                    
                if maptype is 'RALongMap':
                    scanduration = ceil(self.catalog_info[src]['LONG_SIZE'] / (beam_size/5.0) ) * self.backend_info['tint']
                    deltaoffsetobject = "Offset('" +  self.catalog_info[src]['coordmode'] + "', 0.0, " + str(delta/60.0) + ")"
                    obs_command = "RALongMap(src," + longoffsetobject + "," + latoffsetobject + "," + deltaoffsetobject + "," + str(scanduration) + ",beamName='B1')"
                    f.write(obs_command)
                    f.close()
                else:
                    scanduration = ceil(self.catalog_info[src]['LAT_SIZE'] / (beam_size/5.0) ) * self.backend_info['tint']
                    deltaoffsetobject = "Offset('" +  self.catalog_info[src]['coordmode'] + "'," +  str(delta/60.0) + ", 0.0)"
                    obs_command = "DecLatMap(src," + longoffsetobject + "," + latoffsetobject + "," + deltaoffsetobject + "," + str(scanduration) + ",beamName='B1')"
                    f.write(obs_command)
                    f.close()
                    


    def print_single_pointing_script(self):
        
        """
        Purpose: print out single-pointing observing script

        Date            Programmer         Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley        Original Code

        """

        # for each source in catalog create observing script need to
        # ask for the integration time if you don't already have
        # it. probably write an extra function to do this.
        for src in self.catalog_info.keys():

            filename = self.project_info['project_id'] + '_' + src + '.obs'
            try:
                f = open(filename, 'w')
            except:
                print "Could not open filename"
            
            self.write_script_header(f)

            f.write("# Slewing to source.  \n")
            f.write("src = '" + src + "'\n")
            f.write("Slew(src)\n")
            f.write("\n")

            ## ADD CONFIG AND BALANCE STATEMENT HERE???
            
            # select the observing command based on the observing mode.
            if self.project_info['observing_method'] == 'psw':
                offsetobject = "Offset('" +  self.catalog_info[src]['coordmode'] + "'," + \
                    str(self.catalog_info[src]['LONG_OFFSET']/60.0) + "," + \
                    str(self.catalog_info[src]['LAT_OFFSET']/60.0)+')'
                obs_command = 'OnOff(src,' + offsetobject + ","+str(self.catalog_info[src]['INT']) + ')\n'
            elif self.project_info['observing_method'] == 'fsw':
                obs_command = 'Track(src,None,'+ str(self.catalog_info[src]['INT']) + ')\n'
            elif self.project_info['observing_method'] == 'nod':
                obs_command = 'Nod'
                obs_command = 'Nod(src,1,2,'+ str(self.catalog_info[src]['INT']) + ')\n'
            else:
                print "Observing mode not recognized"

            if obs_command:
                f.write(obs_command)
            

            f.close()
                    

    def  display_goodbye_message(self):
    
        """
        Purpose: display a welcome message

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code
        """

        print """

        Thank you for using the automatic GBT script generator. Your
        scripts will be found in the directory you started the program
        from. To observe, please inspect the scripts and then load
        them into Astrid.

        """

def get_user_parameters():

    """
    Purpose: Get desired information from user

    Input: project information from user
    Output: user parameters into dictionary with project info

    Date        Programmer      Description of Changes
    ----------------------------------------------------------------------
    9/25/2013   A.A. Kepley     Original Code
    """

    # Create a new project
    myproject = Project()

    # display welcome message with instructions on how to run program
    myproject.display_welcome_message()

    # set up the project meta-data
    myproject.get_project_id()    

    # get the catalog
    myproject.get_user_catalog()

    # read the catalog
    myproject.read_catalog() 

    # set up the backend
    myproject.get_backend_preset()
    myproject.setup_backend()

    myproject.setup_observations()

    # print backend config
    myproject.print_backend_config()

    # print focus script
    myproject.print_focus_script()

    # print observing scripts
    myproject.print_observing_script()

    myproject.display_goodbye_message()
