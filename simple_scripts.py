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
                             'swfreq':(0.0,0.0), # switching frequency
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
        if (re.match(myproject.catalog_info['type'], 'LatLongVel') || 
            re.match(myproject.catalog_info['type'], 'LatLongVelInt') ||
            re.match(myproject.catalog_info['type'], 'LatLongVelMap')):

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
            
        elif self.catalog_info['type'] == 'LatLongInt':
            try:
                catalog_data = np.genfromtxt(self.project_info['catalog_location'],
                                             dtype='S25,S25,S25,f',
                                             names='srcname','lat','long','int')
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
                                             names='srcname','lat','long','vel','int')
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
                                             names='srcname','lat','long','lat_size','long_size')
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
                                             names='srcname','lat','long','vel','lat_size','long_size')
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


    def get_backend_defaults(backend_config):

        """
        Purpose: set defaults for backend configuration. 

        Output: backend structure with values set.

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
            """

    def get_backend_preset(backend_config):

        """
        Purpose: have the user select which backend present they want to use

        Output: backend structure with appropriate values for preset

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
            """

    def get_manual_backend_config(backend_config):

        """
        Purpose: set up a single, user-specified spectral window

        Output: backend structure with appropriate values

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
            """

    def set_up_map():

        """
        Purpose: set up a single map with the given parameters

        Output: mapping script

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code
            """


    def print_catalog():

        """
        Purpose: print out catalog

            """
            
    def print_backend_config():

        """
        Purpose: print out backend configuration for observing

        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code

            """


    def print_observing_script():

        """
        Purpose: print out observing script


        Date        Programmer      Description of Changes
        ----------------------------------------------------------------------
        9/25/2013   A.A. Kepley     Original Code

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

    # set up the project meta-data
    myproject.get_project_id()    
    myproject.get_script_name()

    # get the catalog
    myproject.get_user_catalog()
    myproject.get_user_catalog_type()
    myproject.get_user_catalog_position_definitions()

    # get velocity definitions
    myproject.get_user_catalog_velocity_definitions()

    # Read the catalog
    myproject.read_catalog() 

    # set up the backend
    #    myproject.set_backend_defaults(backend_info) # do I want this?
    myproject.get_backend_preset()

    ## Do I want to do this here with series of elif statements or do I want to do this in a function?
    if myproject.project_info['backend_present'] == 'other':
        myproject.get_manual_backend_config(backend_info)
    else:
        pass

    # set up map if doing map


    # output scripts (give option to either print to screen or output to file).
