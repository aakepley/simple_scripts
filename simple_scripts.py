class Project:

    def __init__(self):
        # Do I want to make this into one big object instead of 3 separate objects??
        
        # general project info
        project_info = {'project_id': "",        # AGBT13B_306            
                        'script_name': "",       # test1
                        'catalog_location': "", # /path/to/filename
                        'backend_preset': "",        # short name for preset or other if not using a preset
                        'observing_method': "",      # nod (nodding), psw (position switching), fsw (frequency switching).
                        'map': False}                # True if map, False otherwise. Can't have map=True and observing_method='nod'
        
        # integration time??
        # add actual catalog info too??
        # Add map size as two separate columns??
        catalog_info = {'longitude_coordinate': "", # RA, GLong
                        'latitude_coordinate': "",  # Dec, GLat
                        'epoch': "",                # J2000, B1950, Galactic
                        'velocity_definition': "",  # Bary, topo, lsr
                        'velocity_convention': ""}  # optical, radio

        # these are taken from the configuration keywords for astrid
        backend_info = {'receiver':'', # Rcvr1_2, etc
                        'backend': '', # Spectrometer
                        'obstype': '', # Spectroscopy
                        'restfreq': 0.0, # MHz
                        'bandwidth': 0.0 , # 12.5, 50, 200, 800 MHz for Spectrometer
                        'swmode': '', # tp, tp_nocal, sp, sp_nocal (either want tp or sp)
                        'swtype': '' # only used when sp. none, fsw, bsw, psw
                        'swper': 0.0, # switching cycle in seconds 
                        'swfreq':(0.0,0.0), # switching frequency
                        'tint': 0.0, # integration time in seconds
                        'beam': '', # B1, B2, B3, B4, B12, etc.
                        'nwin': 0, #1,2,3 
#                        'deltafreq': '', probably don't need this
                        'vlow': '', # Can figure out from catalog or set to zero. Which is safer?
                        'vhigh':'', # Can figure out from catalog or set to zero. Which is safer?
                        'vframe': '', # Can figure out from catalog
                        'vdef': '', # Can figure out from catalog
                        'nchan': '', # low, medium, high
                        'spect.levels': ''} # 3 or 9. for 200 and 800 MHz only have 3 level sampling

        def __str__(self):
            """
            find a pretty way to print this info
            """
    

        def get_project_id(self):

            """
            Purpose: obtain project id from user
            
            Input: user inputs project ID 
            Output: project ID
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
            """
            
            project_id = raw_input("Input Project ID Number (i.e., AGBT13A_306): ")
            
            # add check on valid project_id number
            # add check on whether input valid, i.e., a string
            
            
            self.project_info['project_id'] = project_id
        
        def get_script_name(self):

            """
            Purpose: get name for scripts. Final scripts are put in a
            directory with this name.
            
            Input: user inputs script name
            Output: script name
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
            """
            script_name = raw_input("Enter a name for your scripts: ")

            # add check on valid script name
            # add check on whether input valid, i.e., a string

            # check if directory exists and create one if it doesn't.

            self.project_info['script_name'] = script_name

        def get_user_catalog():

            """
            Purpose: get the location of the user's catalog.
            
            Input: user catalog
            
            The catalog should have four columns with name, longitude-like
            coordinate (e.g., RA), latitude-like coordinate (Dec), and source
            velocity. In the future, I may add a fifth column for source
            integration time.
            
            The names should not include any spaces. I'm assuming that the
            longitude- and latitude-like coordinate are input as hh:mm:ss.s or
            dd:mm:ss.s.
            
            Output: user catalog location
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
            """

            catalog_location = raw_input("Enter the location of your catalog: ")

            # add check on valid project_id number
            # add check on whether input valid, i.e., a string

            self.project_info['catalog_location'] = catalog_location

        def get_user_catalog_definitions():

            """
            Purpose: ask user for definitions for long-lat coordinates and source velocities.
            
            Output: values for definitions of long-lat coordinates and source velocities.
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
            """
            
        def read_catalog(catalog_name):
                
            """
            Purpose: read in user catalog.
            
            Output: set coordinates in catalog dictionary.
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
            """

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

        def get_map_parameters():

            """
            Purpose: set up a single map with the given parameters
            
            Output: mapping script
            
            Date        Programmer      Description of Changes
            ----------------------------------------------------------------------
            9/25/2013   A.A. Kepley     Original Code
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

    # set up the backend
    #    myproject.set_backend_defaults(backend_info) # do I want this?
    myproject.get_backend_preset()

    ## Do I want to do this here with series of elif statements or do I want to do this in a function?
    if myproject.project_info['backend_present'] == 'other':
        myproject.get_manual_backend_config(backend_info)
    else:


    # set up map if doing map


    # output scripts (give option to either print to screen or output to file).






