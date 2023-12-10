class Customer:
    headings = ['ID', 'Name', 'Color', 'Mode', 'Type', 'Pos']
    fields = {
        '-ID-': 'Game ID:',
        '-Name-': 'Game Name:',
        '-Color-': 'Game Color:',  # Cambio de 'Class' a 'Color'
        '-Mode-': 'Game Mode:',
        '-Type-': 'Game Type:',
        '-PosFile-': 'Position into File'
    }

    def __init__(self, ID, name, color, mode, type, posFile):
        self.ID = ID
        self.name = name
        self.color = color  # Cambio de 'class_' a 'color'
        self.mode = mode
        self.type = type
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.posFile == self.posFile

    def __str__(self):
        return f"{self.ID} {self.name} {self.color} {self.mode} {self.type} {self.posFile}"

    def __repr__(self):
        return f"Customer(ID={self.ID}, name={self.name}, color={self.color}, mode={self.mode}, cust_type={self.type}, posFile={self.posFile})"

    def customerinPos(self, pos):
        return str(self.posFile) == str(pos)

    def setCustomer(self, name, color, mode, type):  # Cambio de 'class_' a 'color'
        self.name = name
        self.color = color  # Cambio de 'class_' a 'color'
        self.mode = mode
        self.type = type
