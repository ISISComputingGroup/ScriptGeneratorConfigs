from genie_python.genie_script_generator import ScriptDefinition


class DoRun(ScriptDefinition):
    def run(self, the="1", imat="2", fields="2", there="2", are="2", more="2"):
        print(the)
        print(imat)
        print(fields)
        print(there)
        print(are)
        print(more)

    def parameters_valid(self, the="1", imat="2", fields="2", there="2", are="1", more="2"):
        if are != "1":
            return "are is not 1"
        else:
            return None

    def estimate_time(self, the="1", imat="2", fields="2", there="2", are="1", more="2"):
        return float(the) * float(imat)

    def get_help(self):
        return None
