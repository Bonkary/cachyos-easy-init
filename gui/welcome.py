from .widgets import *

class Welcome(BasicWidget):
    def __init__(self):
        super().__init__()
        


class PackageManagers(BasicWidget):
    def __init__(self):
        super().__init__()
        
        selectLabel = BasicLabel("Select a package manager(s)")
        yayCheck = BasicCheckbox("yay")
        paruCheck = BasicCheckbox("paru"
                                  )
        
        
        
        
class GpuType(BasicWidget):
    def __init__(self):
        super().__init__()
        

class OptionalApps(BasicWidget):
    def __init__(self):
        super().__init__()