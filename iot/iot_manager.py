# Import python modules
import logging, time, threading, os, sys, datetime, json, sys, traceback, copy
import glob

# Import the IoT communications class
from iot.iot_pubsub import IoTPubSub


class IoTManager:
    """ Manages IoT communications to the Google cloud backend MQTT service """

    # Initialize logger
    extra = {"console_name":"IoT", "file_name": "IoT"}
    logger = logging.getLogger( 'iot' )
    logger = logging.LoggerAdapter(logger, extra)

    # Place holder for thread object.
    thread = None

    # Keep track of the previous values that we have published.  
    # We only publish a value if it changes.
    prev_vars = None
    sentAboutJson = False

    #--------------------------------------------------------------------------
    def __init__( self, state, ref_device_manager ):
        """ Class constructor """
        self.state = state
        self.ref_device_manager = ref_device_manager
        self.error = None
        self._stop_event = threading.Event() # so we can stop this thread
        try:
            # pass in the callback that receives commands
            self.iot = IoTPubSub( self.command_received ) 
        except( Exception ) as e:
            self.error = e
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.critical( "Exception creating class: {}".format( e ))
            traceback.print_tb( exc_traceback, file=sys.stdout )
            exit( 1 )


    #--------------------------------------------------------------------------
    # This is a callback that is called by the IoTPubSub class when this 
    # device receives commands from the UI.
    def command_received( self, command, arg0, arg1 ):
        """
        Process commands received from the backend (UI).
        """
        try:
            if command == IoTPubSub.CMD_START:
                recipe_json = arg0
                recipe_dict = json.loads( arg0 )

                # Make sure we have a valid recipe uuid
                if 'uuid' not in recipe_dict or \
                    None == recipe_dict["uuid"] or \
                    0 == len( recipe_dict["uuid"] ):
                        self.logger.error( \
                                "command_received: missing recipe UUID")
                        return
                recipe_uuid = recipe_dict['uuid']
            
                # first stop any recipe that may be running
                self.ref_device_manager.process_stop_recipe_event()

                # put this recipe in our DB (by uuid)
                self.ref_device_manager.load_recipe_json( recipe_json )

                # start this recipe from our DB (by uuid)
                self.ref_device_manager.process_start_recipe_event( \
                        recipe_uuid )

                # record that we processed this command
                self.iot.publishCommandReply( command, recipe_json )
                return

            if command == IoTPubSub.CMD_STOP:
                self.ref_device_manager.process_stop_recipe_event()
                self.iot.publishCommandReply( command, '' )
                return

            self.logger.error( "command_received: Unknown command: {}".format( \
                command ))
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.critical( "Exception in command_received(): %s" % e)
            traceback.print_tb( exc_traceback, file=sys.stdout )
            return False


    #--------------------------------------------------------------------------
    @property
    def error( self ):
        """ Gets error value. """
        return self._error


    #--------------------------------------------------------------------------
    @error.setter
    def error( self, value ):
        """ Safely updates recipe error in shared state. """
        self._error = value
#TODO: need iot dict in state if we do this
#        with threading.Lock():
#            self.state.iot["error"] = value


    #--------------------------------------------------------------------------
    def spawn( self ):
        self.logger.info("Spawning IoT thread")
        self.thread = threading.Thread( target=self.thread_proc )
        self.thread.daemon = True
        self.thread.start()


    #--------------------------------------------------------------------------
    def stop( self ):
        self.logger.info("Stopping IoT thread")
        self._stop_event.set()


    #--------------------------------------------------------------------------
    def stopped( self ):
        return self._stop_event.is_set()


    #--------------------------------------------------------------------------
    def publish( self ):
        vars_dict = self.state.environment["reported_sensor_stats"] \
            ["individual"]["instantaneous"]

        # Keep a copy of the first set of values (usually None).
        if self.prev_vars == None:
            self.prev_vars = copy.deepcopy( vars_dict )

        # for each value, only publish the ones that have changed.
        for var in vars_dict:
            if self.prev_vars[var] != vars_dict[var]:
                self.prev_vars[var] = copy.deepcopy( vars_dict[var] )
                self.iot.publishEnvVar( var, vars_dict[var] )


    #--------------------------------------------------------------------------
    def thread_proc( self ):
        while True:

            # Publish about.json for a record of versions on this machine.
            if not self.sentAboutJson:
                self.sentAboutJson = True
                try:
                    about_json = open( "about.json" ).read()
                    self.iot.publishCommandReply( "boot", about_json )
                    self.logger.info( "Published boot message with versions." )
                except:
                    self.error = "Unable to load about.json file."
                    self.logger.critical( self.error )


            if self.stopped():
                break

            # send and receive messages over IoT
            self.iot.process_network_events() 

            # check for images to publish
            try:
                imageFileList = glob.glob( 'images/*.png' )
                for imageFile in imageFileList:

                    # Is this file open by a process? (fswebcam)
                    if 0 == os.system( \
                        'lsof -f -- {} > /dev/null 2>&1'.format( imageFile )):
                        continue # Yes, so skip it and try the next one.

                    # 2018-06-15-T18:34:45Z_Camera-Top.png
                    fn1 = imageFile.split( '_' ) 
                    fn2 = fn1[ 1 ] # Camera-Top.png
                    fn3 = fn2.split( '.' )
                    cameraName = fn3[ 0 ] # Camera-Top
                
                    f = open( imageFile, 'rb' )
                    fileBytes = f.read()
                    f.close()

                    self.iot.publishBinaryImage( cameraName, 'png', fileBytes )
                    os.remove( imageFile ) # clean up!
            
            except( Exception ) as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.logger.critical( "Exception: {}".format( e ))
                traceback.print_tb( exc_traceback, file=sys.stdout )

            # idle for a bit
            time.sleep( 1 )


