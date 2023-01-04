#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on January 04, 2023, at 16:51
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '2'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from setupScript
# load libraries
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
import pylink

from EyelinkHelperFunctions import *
from EyelinkSetup import *

from string import ascii_letters, digits
import string
import time
import random

import psychtoolbox as ptb

# set a short name for your study. This name will be the first few letters of the data file.
studyAbbr = '' # max 3 characters
# Run 'Before Experiment' code from driftCorrectionScript
# setup a variable to control whether to do driftcorrection at the beginning of each tiral.
driftRequested = False


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'template'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'results/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\babylab-eyetracker\\Documents\\Psychopy_examples\\PsychoPy_EyeLink_Templates\\template.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1707, 1920], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "el_Setup" ---
# Run 'Begin Experiment' code from setupScript
# --- Show participant info dialog --
expInfo['participant'] = studyAbbr + '_' + ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +  string.digits, k = 4))

# loop until we get a valid filename
while True:
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    # show dialog and wait for OK or Cancel
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(dlg.data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()
    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]
    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break
#
#expInfo['date'] = data.getDateStr()  # add a simple timestamp
#expInfo['expName'] = expName
#expInfo['psychopyVersion'] = psychopyVersion

# Set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + \
    u'results/%s' % (session_identifier)

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

# create a 'graphics' folder to save the VFRAME commands for each trial
#graphics_folder = os.path.join(session_folder, 'graphics')
#if not os.path.exists(graphics_folder):
#    os.makedirs(graphics_folder)

# get the native screen resolution used by PsychoPy
scn_width, scn_height = win.size

########################
### Eyelink initialization starts###
########################

dummy_mode = False
if (not dummy_mode):
    el_tracker = elSetupStep1(dummy_mode)
    el_tracker = elSetupStep2(el_tracker, edf_fname)
    el_tracker = elSetupStep3(el_tracker, dummy_mode)
    el_tracker, genv = elSetupStep4(el_tracker, win)

########################
### Eyelink initialization ends###
########################


# --- Initialize components for Routine "introduction" ---

# --- Initialize components for Routine "el_Calibration" ---

# --- Initialize components for Routine "el_DriftCorrection" ---

# --- Initialize components for Routine "trial" ---
image = visual.ImageStim(
    win=win,
    name='image', 
    image='images/AM28H.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "el_Setup" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
el_SetupComponents = []
for thisComponent in el_SetupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "el_Setup" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in el_SetupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "el_Setup" ---
for thisComponent in el_SetupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "el_Setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "introduction" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
introductionComponents = []
for thisComponent in introductionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "introduction" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in introductionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "introduction" ---
for thisComponent in introductionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "introduction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "el_Calibration" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from calibrationScript
########################
### Eyelink setup starts###
########################
if (not dummy_mode):
    el_tracker = elSetupStep5(el_tracker, dummy_mode)

driftRequested = False

########################
### Eyelink setup ends###
########################
# keep track of which components have finished
el_CalibrationComponents = []
for thisComponent in el_CalibrationComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "el_Calibration" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in el_CalibrationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "el_Calibration" ---
for thisComponent in el_CalibrationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from calibrationScript
win.flip()
# the Routine "el_Calibration" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
blockLoop = data.TrialHandler(nReps=5.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='blockLoop')
thisExp.addLoop(blockLoop)  # add the loop to the experiment
thisBlockLoop = blockLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlockLoop.rgb)
if thisBlockLoop != None:
    for paramName in thisBlockLoop:
        exec('{} = thisBlockLoop[paramName]'.format(paramName))

for thisBlockLoop in blockLoop:
    currentLoop = blockLoop
    # abbreviate parameter names if possible (e.g. rgb = thisBlockLoop.rgb)
    if thisBlockLoop != None:
        for paramName in thisBlockLoop:
            exec('{} = thisBlockLoop[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    trialLoop = data.TrialHandler(nReps=5.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trialLoop')
    thisExp.addLoop(trialLoop)  # add the loop to the experiment
    thisTrialLoop = trialLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
    if thisTrialLoop != None:
        for paramName in thisTrialLoop:
            exec('{} = thisTrialLoop[paramName]'.format(paramName))
    
    for thisTrialLoop in trialLoop:
        currentLoop = trialLoop
        # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
        if thisTrialLoop != None:
            for paramName in thisTrialLoop:
                exec('{} = thisTrialLoop[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "el_DriftCorrection" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from driftCorrectionScript
        while (not dummy_mode) and driftRequested :
            # terminate the task if no longer connected to the tracker or
            # user pressed Ctrl-C to terminate the task
            if (not el_tracker.isConnected()) or el_tracker.breakPressed():
                terminate_task()
                # return pylink.ABORT_EXPT
        
            # drift-check and re-do camera setup if ESCAPE is pressed
            try:
                # in the following line, int(scn_width / 2), int(scn_height / 2) mean the target will show up at the center of the screen.
                # you can set the target location to other values (in pixels).
                error = el_tracker.doDriftCorrect(int(scn_width / 2), int(scn_height / 2), 1, 1)
                # break following a success drift-check
                if error is not pylink.ESC_KEY:
        #            driftRequested = False
                    continueRoutine = False  # skip attention getter for this trial.
                    break
            except:
                pass
         
        # keep track of which components have finished
        el_DriftCorrectionComponents = []
        for thisComponent in el_DriftCorrectionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "el_DriftCorrection" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in el_DriftCorrectionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "el_DriftCorrection" ---
        for thisComponent in el_DriftCorrectionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from driftCorrectionScript
        driftRequested = False
        # the Routine "el_DriftCorrection" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from el_ControlScript
        ############################
        # Eyelink recording starts
        ############################
        if (not dummy_mode):
            try:
                el_tracker.startRecording(1, 1, 1, 1)
                # send a "TRIALID" message to mark the start of a trial, see Data
                # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
                el_tracker.sendMessage('BLOCK_ID %d, TRIAL_ID %d' % ((blockLoop.thisN + 1), (trialLoop.thisN + 1)))
        
                # record_status_message : show some info on the Host PC
                # here we show how many trial has been tested
                status_msg = 'BLOCK_ID %d, TRIALID %d' % ((blockLoop.thisN + 1), (trialLoop.thisN + 1))
                el_tracker.sendCommand("record_status_message '%s'" % status_msg)
                
            except RuntimeError as error:
                print("ERROR:", error)
                abort_trial()
                # return pylink.TRIAL_ERROR
        
            # Allocate some time for the tracker to cache some samples
            pylink.pumpDelay(100)
        
            # clear the Data Viewer screen as well
            bgcolor_RGB = (140, 140, 140)
            el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)
        # Run 'Begin Routine' code from el_SendMarkersScript
        # eye tracker markers
        sendMarker = True
        # Run 'Begin Routine' code from el_LandmarkScript
        # this script is to draw landmarks on the Host PC
        
        if (not dummy_mode):
            # convert the size of image tool into pixels
            imageLocation = obj2pix(image, win)
            
            # Drawing reference landmarks in the data file.
            el_tracker.sendCommand('draw_box %d %d %d %d 15' % imageLocation)
            
            # Drawing reference landmarks on the Host PC screen - Optional
            # See COMMANDS.INI in the Host PC's exe folder for a list of commands
            # region occupied by the movie
            el_tracker.sendMessage('!V DRAWBOX 0 255 0 %d %d %d %d' % imageLocation)
        # keep track of which components have finished
        trialComponents = [image]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from el_SendMarkersScript
            # send a mark to eye tracker to mark the start of stimuli onset
            # the following is an example for the onset of the image component
            # here, 'image' is the name of the Component in this Routine.
            if sendMarker and image.status == STARTED and (not dummy_mode):
                sendMarker = False
                el_tracker.sendMessage('image_starts')
            
            # the following is an example for the offset of the image tool.
            # this might not always work as image offset might overlap with trial offset.
            if sendMarker == False and image.status == FINISHED and (not dummy_mode):
                el_tracker.sendMessage('image_ends')
                sendMarker = True
            
            # *image* updates
            if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.started')
                image.setAutoDraw(True)
            if image.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    image.tStop = t  # not accounting for scr refresh
                    image.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image.stopped')
                    image.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from el_ControlScript
        ############################
        # Eyelink recording stops
        ############################
        
        if (not dummy_mode):
            el_tracker.sendMessage('trial_ends')
            # save data to the eye tracking file
        
            # record trial variables to the EDF data file, for details, see Data
            # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
            # as an example, the following line will create a variable of phase and assign 'test' as its value
            el_tracker.sendMessage('!V TRIAL_VAR phase %s' % 'test')
            # another example, the following line will create a variable of trialNum and assign trialLoop.thisN + 1 as its value
            el_tracker.sendMessage('!V TRIAL_VAR trialNum %s' % (trialLoop.thisN + 1))
            
            # clear the screen
            clear_screen(win, genv)
        
            # send a message to clear the Data Viewer screen as well
            el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)
        
            # close the VCL file that contain the VFRAME messages
            # dlf_file.close()
        
            # stop recording; add 100 msec to catch final events before stopping
            pylink.pumpDelay(100)
            el_tracker.stopRecording()
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
    # completed 5.0 repeats of 'trialLoop'
    
    thisExp.nextEntry()
    
# completed 5.0 repeats of 'blockLoop'

# Run 'End Experiment' code from setupScript
# Step 7: disconnect, download the EDF file, then terminate the task
edf_file = edf_fname + ".EDF"
terminate_task(win, session_folder, session_identifier, edf_file, genv)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
