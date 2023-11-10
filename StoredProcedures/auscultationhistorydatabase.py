class AuscultationHistoryDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.auscultations = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.auscultations = {}

        for line in self.file:
            recording_name, date, files, flagged = line.strip().split(";")
            files_list = files.split(",")
            self.auscultations[recording_name] = (date, files_list, flagged)

        self.file.close()

    def add_auscultation(self, recording_name, date, files, flagged):
        self.auscultations[recording_name] = (date, files, flagged)
        self.save()

    def delete_auscultation(self, recording_name):
        del self.auscultations[recording_name]

    def get_auscultations(self):
        return self.auscultations

    def get_flagged_auscultations(self):
        flagged_auscultations = {}
        for recording_name in self.auscultations:
            if(self.auscultations[recording_name][2] == 1):
                flagged_auscultations.append(self.auscultations[recording_name])
        return flagged_auscultations

    def save(self):
        with open(self.filename, "w") as file:
            for auscultation in self.auscultations:
                line = auscultation + ";" + self.auscultations[auscultation][0] + ";"
                for file in self.auscultations[auscultation][1]:
                    line += file + ","
                line += ";" + self.auscultations[auscultation][2] + "\n"
                file.write(line)
        file.close()
