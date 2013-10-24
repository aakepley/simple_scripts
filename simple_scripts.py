import numpy as np
import re
import os

class Project:

    def __init__(self):

        # Do I want to make this into one big dictionary instead of 3 separate dictionaries?

        # general project info
        self.project_info = {'project_id': "",        # AGBT13B_306            
                             'script_name': "",       # test1
                             'catalog_location': "",  # /path/to/filename
                             'backend_preset': "",    # short name for preset or other if not using a preset
                             'observing_method': "",  # nod (nodding), psw (position switching), fsw (frequency switching).
                             'map': False}            # True if map, False otherwise. Can't have map=True and observing_method='nod'.
        
        # Catalog info
        self.catalog_info = {'type': "",                 # LatLong, LatLongVel, LatLongInt, LatLongVelInt, LatLongMap, LatLongVelMap
                             'longitude_coordinate': "", # RA, GLong
                             'latitude_coordinate': "",  # Dec, GLat
                             'epoch': "",                # J2000, B1950, Galactic
                             'velocity_definition': "",  # Bary, topo, lsr
                             'velocity_convention': "",  # optical, radio
                             'catalog': {'srcname': np.array([]),
                                         'lat': np.array([]),
                                         'long': np.array([]),
                                         'vel':np.array([]),
                                         'int':np.array([]),
                                         'offset':np.array([]),
                                         'long_size': np.array([]),
                                         'lat_size': np.array([])}} 

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
    

    def display_welcome_message():

        """
        Purpose: display a welcome message

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code
        """

        print """

        Welcome to the automatic GBT script generator!

        To use this program, you will need to have your project ID
        code, which can be found on the cover-sheet of your proposal,
        a text file with your catalog, and what observing mode you
        would like to use.

        Only the simplest and most common GBT observing modes are
        available in this tool. If you want to use a more complex
        observing mode, you could use this tool to create scripts and
        then modify the scripts to suit your purposes.

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
        
    def get_script_name(self):

        """
        Purpose: get name for scripts. Final scripts are put in a
        directory with this name. 

        Input: user inputs script name
        Output: set script name 

        Note (10/24/2013): This function may not be necessary. Delete?

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        # get the name and location for the script directory
        while True:

            script_name = raw_input("Enter a name for your scripts: ")

            if re.match(r"[^\w+]",script_name,):
                print "Script name must only contain alphanumeric characters."
            # check to make sure that the directory doesn't already exist.
            elif os.path.isdir(script_name):                    
                print "Directory already exists."
            else:
                break

        # create the directory
        try:
            os.mkdir(script_name)
        except:
            print "Could not create directory."

        # set the name of the script in the project_info structure
        self.project_info['script_name'] = script_name

    def get_user_catalog(self):

        """
        Purpose: get the location of the user's catalog.

        Input: user catalog location

        Output: set catalog location in project_info

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        import os

        while True:
            catalog_location = raw_input("Enter the location of your catalog: ")

            if os.path.isfile(catalog_location):
                break
            else:
                print "Could not open catalog"                

        self.project_info['catalog_location'] = catalog_location

    def get_user_catalog_type(self):

        """
        Purpose: Get the type of catalog from the user

        Input: catalog type

        Output: set catalog type in catalog_info

        Note (10/24/2013): Refactor how I do this to more easily
        include variable offsets for each source?

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/2/2013       A.A. Kepley     Original Code
        """
        while True:
            prompt = """
            What are the columns in your catalog?
            1.) Name (col. 1), position (col. 2 & 3)
            2.) Name (col. 1), position (col. 2 & 3), velocity (col. 4)
            3.) Name (col. 1), position (col. 2 & 3), integration time (col. 4)
            4.) Name (col. 1), position (col. 2 & 3), velocity (col. 4), integration time (col. 5)
            5.) Name (col. 1), position (col. 2 & 3), map size (col. 4 & 5)
            6.) Name (col. 1), position (col. 2 & 3), velocity (col. 4), map size (col. 5 & 6)
            """

            catalog_type = int(raw_input(prompt))

            if catalog_type == 1:
                self.catalog_info['type'] = 'LatLong'
                break
            elif catalog_type == 2:
                self.catalog_info['type'] = 'LatLongVel'
                break
            elif catalog_type == 3:
                self.catalog_info['type'] = 'LatLongInt'
                break
            elif catalog_type == 4:
                self.catalog_info['type'] = 'LatLongVelInt'
                break
            elif catalog_type == 5:
                self.catalog_info['type'] = 'LatLongMap'
                break
            elif catalog_type == 6:
                self.catalog_info['type'] = 'LatLongVelMap'
                break
            else:
                print "You did not select a valid option."

    def get_user_catalog_position_definitions(self):

        """
        Purpose: ask user for definitions for long-lat coordinates

        Output: values for definitions of long-lat coordinates

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        while True:
            prompt = """
            Select the coordinate frame definition for your catalog:
            1.) RA/Dec (J2000)
            2.) Ra/Dec (B1950)
            3.) Galactic Latitude and Longitude (GLAT/GLONG)
            """

            catalog_definition = int(raw_input(prompt))

            if catalog_definition == 1:
                self.catalog_info['longitude_coordinate'] = 'RA'
                self.catalog_info['latitude_coordinate'] = 'Dec'
                self.catalog_info['epoch'] = 'J2000'
                break
            elif catalog_definition == 2:
                self.catalog_info['longitude_coordinate'] = 'RA'
                self.catalog_info['latitude_coordinate'] = 'Dec'
                self.catalog_info['epoch'] = 'B1950'
                break
            elif catalog_definition == 3:
                self.catalog_info['longitude_coordinate'] = 'GLONG'
                self.catalog_info['latitude_coordinate'] = 'GLAT'
                break
            else:
                print "You did not select a valid option."

    def get_user_catalog_velocity_definitions(self):

        """
        Purpose: ask user for definitions for velocity frame

        Output: values for definitions of velocity definitions

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        # If the catalog contains velocities, get the velocity frame.
        if (re.match(self.catalog_info['type'], 'LatLongVel') or
            re.match(self.catalog_info['type'], 'LatLongVelInt') or
            re.match(self.catalog_info['type'], 'LatLongVelMap')):

            while True:
                prompt = """
                Select the velocity frame for your catalog:
                1.) LSR optical
                2.) LSR radio
                3.) Barycentric (~heliocentric) optical 
                4.) Barycentric (~heliocentric) radio
                5.) Topocentric radio
                """

                catalog_definition = int(raw_input(prompt))
                
                if catalog_definition == 1:
                    self.catalog_info['velocity_definition'] = 'LSR'
                    self.catalog_info['velocity_convention'] ='VOPT'
                    break
                elif catalog_definition == 2:
                    self.catalog_info['velocity_definition'] = 'LSR'
                    self.catalog_info['velocity_convention'] ='VRAD'
                    break
                elif catalog_definition == 3:
                    self.catalog_info['velocity_definition'] = 'BAR'
                    self.catalog_info['velocity_convention'] ='VOPT'
                    break
                elif catalog_definition == 4:
                    self.catalog_info['velocity_definition'] = 'BAR'
                    self.catalog_info['velocity_convention'] ='VRAD'
                    break
                elif catalog_definition == 5:
                    self.catalog_info['velocity_definition'] = 'TOP'
                    self.catalog_info['velocity_convention'] ='VRAD'
                    break
                else:
                    print "You did not select a valid option."

        else:
            return
            
    def read_catalog(self):

        """
        Purpose: read in user catalog.

        The catalog should have at least three columns with name,
        longitude-like coordinate (e.g., RA), latitude-like
        coordinate (Dec). The names should not include any
        spaces. I'm assuming that the longitude- and latitude-like
        coordinate are input as hh:mm:ss.s or dd:mm:ss.s.

        If there is a fourth column, it is assumed to be the
        source velocity in km/s. If a fourth column is not
        included, the velocities for all sources is assumed to be
        zero and the topocentric-radio velocity definition is
        selected.

        If there are five columns, the fifth column is assume to
        be an integration time per source.

        If there are six columns, the fifth and sixth columns are
        the Longitude and Latitude sizes for a map. The user can
        specify the coordinate system for the Longitude and
        Latitude (e.g., RA/Dec, GLAT, GLONG) and it does not need
        to be the same as the coordinate system for each
        source. In other words, you can specify your map centers
        in RA/Dec and map in GLAT/GLONG.

        Output: set coordinates in catalog dictionary.

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        if self.catalog_info['type'] == 'LatLong':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25',
                                             names=['srcname','lat','long'])
            except:
                print "catalog not in right format"

            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.get_integration_time()

        elif self.catalog_info['type'] == 'LatLongVel':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f',
                                             names=['srcname','lat','long','vel'])
            except:
                print "catalog not in right format"

            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.catalog_info['catalog']['vel'] = catalog_data['vel']
            self.get_integration_time()
            
        elif self.catalog_info['type'] == 'LatLongInt':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f',
                                             names=['srcname','lat','long','int'])
            except:
                print "catalog not in right format"
                
            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.catalog_info['catalog']['int'] = catalog_data['int']

        elif self.catalog_info['type'] == 'LatLongVelInt':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f,f',
                                             names=['srcname','lat','long','vel','int'])
            except:
                print "catalog not in right format"
                
            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.catalog_info['catalog']['vel'] = catalog_data['vel']
            self.catalog_info['catalog']['int'] = catalog_data['int']

        elif self.catalog_info['type'] == 'LatLongMap':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f,f',
                                             names=['srcname','lat','long','lat_size','long_size'])
            except:
                print "catalog not in right format"

            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.catalog_info['catalog']['lat_size'] = catalog_data['lat_size']
            self.catalog_info['catalog']['long_size'] = catalog_data['long_size']
            self.project_info['map'] = True

        elif self.catalog_info['type'] == 'LatLongVelMap':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f,f,f',
                                             names=['srcname','lat','long','vel','lat_size','long_size'])
            except:
                print "catalog not in right format"
                
            self.catalog_info['catalog']['srcname'] = catalog_data['srcname']
            self.catalog_info['catalog']['lat'] = catalog_data['lat']
            self.catalog_info['catalog']['long'] = catalog_data['long']
            self.catalog_info['catalog']['vel'] = catalog_data['vel']
            self.catalog_info['catalog']['lat_size'] = catalog_data['lat_size']
            self.catalog_info['catalog']['long_size'] = catalog_data['long_size']
            self.project_info['map'] = True

        else:
            print "not a valid catalog type"


    def get_integration_time(self):

        """
        Purpose: have user set integration time that they want to use

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley             Original Code
        """

        while True:
            prompt = """
            Enter the integration time per source in seconds:
            """

            int_time = raw_input(prompt)

            if int_time.isdigit():
            
                int_array = np.empty(len(self.catalog_info['catalog']['int']))
                int_array.fill(int_time)
                self.catalog_info['catalog']['int'] = int_array.copy()
                break

    def get_psw_offset(self):

        """
        Purpose: have user set the offset that they want to use for position switching

        Date            Programmer              Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley             Original Code
        """

        pass

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


                
    def set_up_backend(self):

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
  

    def set_up_map(self):

        """
        Purpose: set up a single map with the given parameters

        Output: mapping script

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
        """

        pass

    def print_catalog(self):

        """
        Purpose: print out catalog

        Date            Programmer      Description of Change
        ----------------------------------------------------------------------
        10/4/2013       A.A. Kepley     Original Code

        """

        filename = self.project_info['project_id'] + '.cat'

        try:
            f = open(filename, 'w')
        except:
            print "Could not open filename"


        f.write("format=spherical\n")
        f.write("coordmode="+self.catalog_info['epoch'] + "\n")
        f.write("veldef=" +
                self.catalog_info['velocity_convention'] + '-' +
                self.catalog_info['velocity_definition'] + "\n")

        if self.catalog_info['type'] == 'LatLongVel':
            f.write("HEAD = " +
                    "NAME" + "    " +
                    self.catalog_info['longitude_coordinate'] + "    " +
                    self.catalog_info['latitude_coordinate'] + "    " +
                    "VEL" + "\n")
            # write out values from catalogx
            for i in range(len(self.catalog_info['catalog']['lat'])):
                f.write(self.catalog_info['catalog']['srcname'][i] + "    " +
                        self.catalog_info['catalog']['lat'][i] + "    " +
                        self.catalog_info['catalog']['long'][i] + "     " +
                        str(self.catalog_info['catalog']['vel'][i]) + "\n")

        f.close()

            
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

        f.write('myconfig=""""\n')

        # how do i want to deal with switching frequencies here?
        for key in self.backend_info.keys():
            if self.backend_info[key]:
                if type(self.backend_info[key]) is str:
                    f.write(key+"='"+str(self.backend_info[key])+"'\n")
                elif type(self.backend_info[key]) is tuple:
                    param_string = ""
                    for i in self.backend_info[key]:
                        param_string = param_string + str(self.backend_info[key][i]) + ','
                        f.write(key+"="+param_string+"\n")
                else:
                    f.write(key+"="+str(self.backend_info[key])+"\n")
                
        f.write('"""\n')

        f.close()

    def print_focus_script(self):

        """
        Purpose: print out focus script

        Date            Programmer      Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley     Original Code

        """

        configfile = self.project_info['project_id'] + '.config'
        catfile = self.project_info['project_id'] + '.cat'
        mypath = os.getcwd() # assumes I'm running on the GBT systems.

        filename = self.project_info['project_id'] + '_focus.obs'

        try:
            f = open(filename, 'w')
        except:
            print "Could not open filename"

        f.write("#Configuration file\n")
        f.write("execfile('"+mypath+configfile+"')\n")
        f.write("\n")

        f.write("# Catalog files including official flux calibrators and pointing calibrators for the GBT\n")
        f.write("Catalog('"+mypath+catfile+"')\n")
        f.write("Catalog(fluxcal)\n")
        f.write("Catalog(pointing)\n")
        f.write("\n")

        f.write("# Slewing to source. Change src= variable to point and focus near another source \n")
        f.write("src = '" + self.catalog_info['catalog']['srcname'][0] + "'\n")
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
        """
        
        pass

    def print_single_pointing_script(self):
        
        """
        Purpose: print out single-pointing observing script

        Date            Programmer         Description of Changes
        ----------------------------------------------------------------------
        10/24/2013      A.A. Kepley        Original Code

        """

        # get info on configuration and catalog
        configfile = self.project_info['project_id'] + '.config'
        catfile = self.project_info['project_id'] + '.cat'
        mypath = os.getcwd() # assumes I'm running on the GBT systems.

        # for each source in catalog create observing script need to
        # ask for the integration time if you don't already have
        # it. probably write an extra function to do this.
        for src in self.catalog_info['catalog']['srcname']:

            filename = self.project_info['project_id'] + '_' + src + '.obs'
            try:
                f = open(filename, 'w')
            except:
                print "Could not open filename"

            
            f.write("#Configuration file\n")
            f.write("execfile('"+mypath+configfile+"')\n")
            f.write("\n")
            
            f.write("# Catalog files including official flux calibrators and pointing calibrators for the GBT\n")
            f.write("Catalog('"+mypath+catfile+"')\n")
            f.write("Catalog(fluxcal)\n")
            f.write("Catalog(pointing)\n")
            f.write("\n")

            f.write("# Slewing to source. Change src variable to point and focus near another source \n")
            f.write("src = '" + src + "'\n")
            f.write("Slew(src)\n")
            f.write("\n")

            ## ADD CONFIG AND BALANCE STATEMENT HERE???
            
            # select the observing command based on the observing mode.
            if self.project_info['observing_method'] == 'psw':
                obs_command = 'OnOff(src,Offset(J2000,"00:15:00","00:33:00"),'+str(self.catalog_info['catalog']['int']) + ')\n'
            elif self.project_info['observing_method'] == 'fsw':
                obs_command = 'Track(src,None,'+ str(self.catalog_info['catalog']['int']) + ')\n'
            elif self.project_info['observing_method'] == 'nod':
                obs_command = 'Nod'
                obs_command = 'Nod(src,1,2,'+ str(self.catalog_info['catalog']['int']) + ')\n'
            else:
                print "Observing mode not recognized"

            if obs_command:
                f.write(obs_command)
            

            f.close()
                    

    def  display_goodbye_message():
    
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

    myproject.display_welcome_message()
    # set up the project meta-data
    myproject.get_project_id()    
    #    myproject.get_script_name()

    # get the catalog
    myproject.get_user_catalog()
    myproject.get_user_catalog_type()
    myproject.get_user_catalog_position_definitions()

    # get velocity definitions
    myproject.get_user_catalog_velocity_definitions()

    # read the catalog
    myproject.read_catalog() 

    # set up the backend
    myproject.get_backend_preset()
    myproject.set_up_backend()

    # set up map if doing map

    # print catalog
    myproject.print_catalog()

    # print backend config
    myproject.print_backend_config()

    # print focus script
    myproject.print_focus_script()

    # print observing scripts
    myproject.print_observing_script()

    myproject.display_goodbye_message()
