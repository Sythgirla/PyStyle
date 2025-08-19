#Import list
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from pathlib import Path
from tkinter import *
from tkinter.ttk import *

#Make Root for Tkinter
root = tk.Tk()
root.configure(
    width=1000, 
    height=600
)
root.resizable(False, False) #Make window non-resizable


#Definition of showing error codes for debugging
def throwError(errorCode, level):
    errorWindow = Toplevel(root)
    errorWindow.geometry("200x100")
    errorWindow.grab_set()
    errorWindow.resizable(False, False)

    errorText = tk.Label(
        errorWindow,
        justify="center",
        text=errorCode
    )
    errorText.place(
        anchor="center",
        relx=0.5,
        rely=0.5
    )
    def fatalClose():
        root.destroy()

    def colorErrorWidgets(widget):
        match level:
            case "warning":
                widget.config(background=warningColor)
            case "danger":
                widget.config(background=dangerColor)
            case "fatal": #If the error is fatal, it will automatically assume a unique color coding, along with closing the entire program once the window is closed.
                errorWindow.config(background="dark red")
                errorText.config(background="#d40000")
                errorFatal = tk.Label(
                    errorWindow,
                    justify="center",
                    text="This error is fatal. The program will" \
                    "\n close when exiting this screen.",
                    background="dark red"
                )
                errorFatal.place(
                    anchor="center",
                    relx=0.5,
                    rely=0.8
                )
                errorWindow.protocol("WM_DELETE_WINDOW", fatalClose)

    colorErrorWidgets(errorWindow)
    colorErrorWidgets(errorText)
try:
    from pyStyle import StyleFactory
    import yaml
except:
    throwError("ImportFailed/Missing", "fatal")
#Initiate StyleFactory from PyStyle.py
st=StyleFactory(root)
#Set values for tkinter widgets
ich = tk.IntVar()
ico = tk.IntVar()
#Set default values for color variables
primaryColor = "#f0f0f0"
secondaryColor = "#d2d2d2"
tertiaryColor = "#008000"
textColor = "#000000"
warningColor = "#bf7900"
dangerColor = "#d40000"
#Create variables for custom palettes
current = []
custom1Palette = []
custom2Palette = []
custom3Palette = []
#Definition for changing colors
def chooseColor(type : str, override : bool = False):
    if override == False: #Override = False? Assume button to change color is pressed - thus open color picker
        try:
            (rgb, hash) = colorchooser.askcolor()
            if hash == None:
                return
            global primaryColor, secondaryColor, tertiaryColor, textColor, warningColor, dangerColor
            match type: #Check which color that needs to change
                case "Primary":
                    primaryColor = hash
                case "Secondary":
                    secondaryColor = hash
                case "Tertiary":
                    tertiaryColor = hash
                case "Text":
                    textColor = hash
                case "Warning":
                    warningColor = hash
                case "Danger":
                    dangerColor = hash
            reloadUI()

        except:
            throwError("ColorTypeNotFound")
    else: #Override = True? Assume radiobutton to change color palette is pressed - thus change all colors to a predefined value
        try:
            match type: #Check which preset to change to
                case "Default": #This is the default color palette.
                    primaryColor = "#f0f0f0" #Hex colors are used for simple coloring
                    secondaryColor = "#d2d2d2"
                    tertiaryColor = "#008000"
                    textColor = "#000000"
                    warningColor = "#bf7900"
                    dangerColor = "#d40000"
                case "Light":
                    primaryColor = "#ffffff"
                    secondaryColor = "#f8f8f8"
                    tertiaryColor = "#008000"
                    textColor = "#000000"
                    warningColor = "#bf7900"
                    dangerColor = "#d40000"
                case "Dark":
                    primaryColor = "#3f3f3f"
                    secondaryColor = "#808080"
                    tertiaryColor = "#008000"
                    textColor = "#ffffff"
                    warningColor = "#bf7900"
                    dangerColor = "#d40000"
                case "Contrast":
                    primaryColor = "#000000"
                    secondaryColor = "#171717"
                    tertiaryColor = "#008000"
                    textColor = "#ffffff"
                    warningColor = "#bf7900"
                    dangerColor = "#d40000"
                case "VisualStudioCode":
                    primaryColor = "#002451"
                    secondaryColor = "#001C40"
                    tertiaryColor = "#008000"
                    textColor = "#ffffff"
                    warningColor = "#bf7900"
                    dangerColor = "#d40000"
                case "Previous": #This preset is from current colors in config.yaml
                    global configYAML
                    primaryColor = str(configYAML['current colors'][0])
                    secondaryColor = str(configYAML['current colors'][1])
                    tertiaryColor = str(configYAML['current colors'][2])
                    textColor = str(configYAML['current colors'][3])
                    warningColor = str(configYAML['current colors'][4])
                    dangerColor = str(configYAML['current colors'][5])
                case "Custom1": #This and the following are from colors in custom palettes 1-3 in config.yaml
                    global custom1Palette
                    primaryColor = custom1Palette[0]
                    secondaryColor = custom1Palette[1]
                    tertiaryColor = custom1Palette[2]
                    textColor = custom1Palette[3]
                    warningColor = custom1Palette[4]
                    dangerColor = custom1Palette[5]
                case "Custom2":
                    global custom2Palette
                    primaryColor = custom2Palette[0]
                    secondaryColor = custom2Palette[1]
                    tertiaryColor = custom2Palette[2]
                    textColor = custom2Palette[3]
                    warningColor = custom2Palette[4]
                    dangerColor = custom2Palette[5]
                case "Custom3":
                    global custom3Palette
                    primaryColor = custom3Palette[0]
                    secondaryColor = custom3Palette[1]
                    tertiaryColor = custom3Palette[2]
                    textColor = custom3Palette[3]
                    warningColor = custom3Palette[4]
                    dangerColor = custom3Palette[5]
            reloadUI(True) #Reload the UI to reflect changes
        except:
            throwError("ColorPresetNotFound", "warning") #Something went wrong? Error will pop up and defaults will be picked instead.
#Definition to pop up a message to verify the preset action. This is to prevent accidental swaps.
def popupPreset():
    class Result: #Class is required to return values in these definitions.
        value = None

    def popAccept():
        Result.value = True
        popupWindow.destroy()

    def popDeny():
        Result.value = False
        popupWindow.destroy()

    # Make a new, mini window with "Yes" and "No" buttons
    popupWindow = Toplevel(root)
    popupWindow.geometry("200x100")
    popupWindow.grab_set()
    popupWindow.resizable(False, False)
    popupLabel = tk.Label(
        popupWindow,
        justify="center",
        text="Apply this preset?")
    popupLabel.place(
        relwidth=1,
        relheight=0.5
    )
    popupYes = tk.Button( #The "Yes" button
        popupWindow,
        justify="center",
        text="Yes",
        command=lambda: popAccept()
    )
    popupYes.place(
        relx=0.05,
        rely=0.7,
        relwidth=0.4
    )
    popupNo = tk.Button( #The "No" button
        popupWindow,
        justify="center",
        text="No",
        command=lambda: popDeny()
    )
    popupNo.place(
        relx=0.55,
        rely=0.7,
        relwidth=0.4
    )
    popupWindow.wait_window() #Wait for window before continuing
    return Result.value

def popupSaveCustom():
    class Result:
        value = 0

    def pop1():
        Result.value=1
        popupWindow.destroy()

    def pop2():
        Result.value=2
        popupWindow.destroy()

    def pop3():
        Result.value=3
        popupWindow.destroy()

    def popC():
        Result.value=0
        popupWindow.destroy()

    popupWindow = Toplevel(root)
    popupWindow.geometry("300x100")
    popupWindow.grab_set()
    popupWindow.resizable(False, False)
    popupLabel = tk.Label(
        popupWindow,
        justify="center",
        text="Save under which config?"
    )
    popupLabel.place(
        anchor="center",
        relx=0.5,
        rely=0.2
    )
    popupCustom1 = tk.Button(
        popupWindow,
        justify="center",
        text="Custom 1",
        command=lambda: pop1()
    )
    popupCustom2 = tk.Button(
        popupWindow,
        justify="center",
        text="Custom 2",
        command=lambda: pop2()
    )
    popupCustom3 = tk.Button(
        popupWindow,
        justify="center",
        text="Custom 3",
        command=lambda: pop3()
    )
    popupCancel = tk.Button(
        popupWindow,
        justify="center",
        text="Cancel",
        command=lambda: popC()
    )
    popupCustom1.place(
        anchor="center",
        relx=0.125,
        rely=0.7
    )
    popupCustom2.place(
        anchor="center",
        relx=0.35,
        rely=0.7
    )
    popupCustom3.place(
        anchor="center",
        relx=0.575,
        rely=0.7
    )
    popupCancel.place(
        anchor="center",
        relx=0.85,
        rely=0.7
    )

    popupWindow.wait_window()
    return Result.value
#Definition to make the popup appear depending on variables given
def appearPopup(type : str, nextVar : list):
    try: 
        match type:
            case "PresetApply":
                if ich.get() == True:
                    chooseColor(nextVar[0], nextVar[1])
                else:
                    if popupPreset():
                        chooseColor(nextVar[0], nextVar[1])
            case "SaveCustomPreset":
                match popupSaveCustom():
                    case 0: #Case 0 is for cancelling the save. Either by clicking X or "Cancel"
                        pass
                    case 1: 
                        global custom1Palette #We need global variables to edit them in the scope to everywhere else.
                        custom1Palette = [] #Reset the custom palette to prevent issues when saving on the same palette
                        for x in nextVar: #Simple way of pushing all variables into the custom palette
                            custom1Palette.append(x)
                    case 2:
                        global custom2Palette
                        custom2Palette = []
                        for x in nextVar:
                            custom2Palette.append(x)
                    case 3:
                        global custom3Palette
                        custom3Palette = []
                        for x in nextVar:
                            custom3Palette.append(x)
    except:
        throwError("PopupTypeNotFound", "warning")

colors = [primaryColor, secondaryColor, tertiaryColor, textColor, warningColor, dangerColor]
#Definition to reload the UI to reflect current changes
def reloadUI(override : bool = False): 
    PrimaryColorButton.config(text=primaryColor) #Set all buttons to reflect new hex codes
    SecondaryColorButton.config(text=secondaryColor)
    TeriaryColorButton.config(text=tertiaryColor)
    TextColorButton.config(text=textColor)
    WarningColorButton.config(text=warningColor)
    DangerColorButton.config(text=dangerColor)
    global colors
    colors = [primaryColor, secondaryColor, tertiaryColor, textColor, warningColor, dangerColor]
    #Get the int variable of instant color apply, and override. If either is "True", instantly apply colors. Else, don't apply
    if ico.get() == 1 or override == True:
        st._configure_styles(colors)


config_path = Path("config.yaml")
#Open, or make, config.txt, and attempt to read its lines.
def load_config():
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    else:
        return None
        
try:        
    configYAML = load_config()
    custom1Palette = configYAML['custom palette 1']
    custom2Palette = configYAML['custom palette 2']
    custom3Palette = configYAML['custom palette 3']
except: #If config file is not detected, or is read improperly, it will create a fully new config. This will result in 2 errors for now.
    try:
        f = open("config.yaml", "x")
    except:
        pass
    yamlconfig = {
        'current colors': [
            primaryColor,
            secondaryColor,
            tertiaryColor,
            textColor,
            warningColor,
            dangerColor
        ],
        'custom palette 1': 
            custom1Palette,
        'custom palette 2':
            custom2Palette,
        'custom palette 3':
            custom3Palette,
    }
    with open(config_path, "a") as f:
        yaml.dump(yamlconfig, f)
    throwError("ConfigNotDetected/Broken", "danger")

    
#Creating of all labels and buttons of the side-UI to change the colors.
#Manual setup:
PrimaryColorLabel = tk.Label(
    root,
    text="Primary Color: ",
)
PrimaryColorLabel.place(
    x=24,
    y=10
)
PrimaryColorButton = tk.Button(
    root,
    text=primaryColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Primary")
)
PrimaryColorButton.place(
    x=110,
    y=9
)

SecondaryColorLabel = tk.Label(
    root,
    text="Secondary Color: "
)
SecondaryColorLabel.place(
    x=10,
    y=40
)
SecondaryColorButton = tk.Button(
    root,
    text=secondaryColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Secondary")
)
SecondaryColorButton.place(
    x=110,
    y=39
)

TertiaryColorLabel = tk.Label(
    root,
    text="Tertiary Color: "
)
TertiaryColorLabel.place(
    x=25,
    y=70
)
TeriaryColorButton = tk.Button(
    root,
    text=tertiaryColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Tertiary")
)
TeriaryColorButton.place(
    x=110,
    y=69
)

TextColorLabel = tk.Label(
    root,
    text="Text Color: "
)
TextColorLabel.place(
    x=43,
    y=100
)
TextColorButton = tk.Button(
    root,
    text=textColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Text")
)
TextColorButton.place(
    x=110,
    y=99
)

WarningColorLabel = tk.Label(
    root,
    text="Warning Color: "
)
WarningColorLabel.place(
    x=20,
    y=130
)
WarningColorButton = tk.Button(
    root,
    text=warningColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Warning")
)
WarningColorButton.place(
    x=110,
    y=129
)

DangerColorLabel = tk.Label(
    root,
    text="Danger Color: "
)
DangerColorLabel.place(
    x=28,
    y=160
)
DangerColorButton = tk.Button(
    root,
    text=dangerColor,
    height=1,
    width=10,
    command=lambda: chooseColor("Danger")
)
DangerColorButton.place(
    x=110,
    y=159
)

ApplyButton = tk.Button(
    root,
    text="Apply Changes",
    command=lambda: st.update_styles(root, colors)
)
ApplyButton.place(
    x=10,
    y=525
)
InstantChanges = tk.Checkbutton(
    root,
    text="Skip popup?",
    variable=ich
)
InstantChanges.place(
    x=7,
    y=550
)
InstantColor = tk.Checkbutton(
    root,
    text="Instantly accept colors?",
    variable=ico
)
InstantColor.place(
    x=7,
    y=575
)

#Preset setup:
DefaultPresetButton = tk.Button(
    root,
    text="Default",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Default", True])
)
DefaultPresetButton.place(
    x=10,
    y=250
)
LightPresetButton = tk.Button(
    root,
    text="Light",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Light", True])
)
LightPresetButton.place(
    x=10,
    y=280
)
DarkPresetButton = tk.Button(
    root,
    text="Dark",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Dark", True])
)
DarkPresetButton.place(
    x=10,
    y=310
)
ContrastPresetButton = tk.Button(
    root,
    text="Contrast",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Contrast", True])
)
ContrastPresetButton.place(
    x=10,
    y=340
)
VSCPresetButton = tk.Button(
    root,
    text="VSC",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["VisualStudioCode", True])
)
VSCPresetButton.place(
    x=10,
    y=370
)
SaveCustomButton = tk.Button(
    root,
    text="Save Custom",
    height=1,
    width=10,
    command=lambda: appearPopup("SaveCustomPreset", [primaryColor, secondaryColor, tertiaryColor, textColor, warningColor, dangerColor])
)
SaveCustomButton.place(
    x=110,
    y=250
)
LoadCustomButton1 = tk.Button(
    root,
    text="Custom1",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Custom1", True])
)
LoadCustomButton1.place(
    x=110,
    y=310
)    
LoadCustomButton2 = tk.Button(
    root,
    text="Custom2",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Custom2", True])
)
LoadCustomButton2.place(
    x=110,
    y=340
)
LoadCustomButton3 = tk.Button(
    root,
    text="Custom3",
    height=1,
    width=10,
    command=lambda: appearPopup("PresetApply", ["Custom3", True])
)
LoadCustomButton3.place(
    x=110,
    y=370
)

#Seperator to add a more sleek design to the UI
Seperator = ttk.Separator(
    root,
    orient="vertical"
)
Seperator.place(
    relheight=1,
    x=247.5
)


#Example UI:
UIFrame = ttk.Frame(
    width=750,
    height=600
)
UIFrame.place(
    x=250,
    y=0
)
UIFrameButton = ttk.Button(
    UIFrame,
    text="funny button"
)
UIFrameButton.place(
    anchor="nw",
    x=20,
    y=20
)
UIFrameCheckButton = ttk.Checkbutton(
    UIFrame,
    text='funny check button'
)
UIFrameCheckButton.place(
    anchor="nw",
    x=170,
    y=25
)
UIFrameComboBox = ttk.Combobox(
    UIFrame,
    values=['funny value 1', 'funny value 2'],
    state="readonly"
)
UIFrameComboBox.place(
    anchor="nw",
    x=380,
    y=30
)
UIFrameEntry = ttk.Entry(
    UIFrame,
)
UIFrameEntry.place(
    anchor="nw",
    x=530,
    y=30
)
UIFrameLabel = ttk.Label(
    UIFrame,
    text="funny text"
)
UIFrameLabel.place(
    anchor="nw",
    x=660,
    y=25
)
UIFrameLabelFrame = ttk.LabelFrame(
    UIFrame,
    text="funny text frame",
    width=150,
    height=50
)
UIFrameLabelFrame.place(
    anchor="nw",
    x=20,
    y=170
)
UIFrameMenu = ttk.Menubutton(
    UIFrame,
    text="funny menu button"
    
)
UIFrameMenu.place(
    anchor="nw",
    x=200,
    y=165
)
UIFrameNotebook = ttk.Notebook(
    UIFrame
)
UIFrameNotebookT1 = ttk.Frame(
    UIFrame
)
UIFrameNotebookT2 = ttk.Frame(
    UIFrame
)
UIFrameNotebook.add(UIFrameNotebookT1)
UIFrameNotebook.tab(0, text="funny notebook tab")
UIFrameNotebook.add(UIFrameNotebookT2)
UIFrameNotebook.tab(1, text="funnier notebook tab")
UIFrameNotebook.place(
    anchor="nw",
    x=370,
    y=170
)
UIFrameProgressBar = ttk.Progressbar(
    UIFrame,
    mode="indeterminate",
)
UIFrameProgressBar.place(
    anchor="nw",
    x=20,
    y=320
)
UIFrameRadioButton1 = ttk.Radiobutton(
    UIFrame,
    text="funny radio button"
)
UIFrameRadioButton1.place(
    anchor="nw",
    x=140,
    y=312
)
UIFrameScale = ttk.Scale(
    UIFrame
)
UIFrameScale.place(
    anchor="nw",
    x=20,
    y=470
)
UIFrameScrollbar = ttk.Scrollbar(
    UIFrame,
)
UIFrameScrollbar.place(
    anchor="nw",
    x=170,
    y=470
)
UIFrameTreeview = ttk.Treeview(
    UIFrame,
    selectmode="browse",
    show="headings",
    columns=["one", "twenty one"],
)
UIFrameTreeview["columns"] = ("one", "twenty one")
UIFrameTreeview.column(0, stretch=False, minwidth=140, width=140, anchor="center")
UIFrameTreeview.column(1, stretch=False, minwidth=140, width=140, anchor="center")
UIFrameTreeview.heading(0, text="fun")
UIFrameTreeview.heading(1, text="ny")
UIFrameTreeview.insert("", "end", values=("funny", "funnier"))
UIFrameTreeview.insert("", "end", values=("funniest", "funnierst"))
UIFrameTreeview.place(
    anchor="nw",
    x=370,
    y=270
)

def fixes_treeview_static(treeview : Widget):
    StyleFactory.add_treeview(treeview)
    treeview.bind('<Button-1>', StyleFactory.treeview_static)
    treeview.bind('<Motion>', StyleFactory.treeview_static)
fixes_treeview_static(UIFrameTreeview)

def on_closing():
    yamlconfig = {
        'current colors': [
            primaryColor,
            secondaryColor,
            tertiaryColor,
            textColor,
            warningColor,
            dangerColor
        ],
        'custom palette 1': 
            custom1Palette,
        'custom palette 2':
            custom2Palette,
        'custom palette 3':
            custom3Palette,
    }
    try:
        with open('config.yaml', 'w') as f:
            yaml.dump(yamlconfig, f)
    except:
        print("yaml not saved")
    root.destroy()
chooseColor("Previous", True)

style=ttk.Style()
st.update_styles(root, colors)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()