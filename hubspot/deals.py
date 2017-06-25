import hubspot.api


class Deal(object):
    data = None
    api = None
    stage = None

    def __init__(self, data):
        self.data = data

    def get_stage(self):
        if self.stage is None:
            stage = self.fetch_stage()
            self.stage = stage

        return self.stage

    def fetch_stage(self):
        stage_id = self.data['properties']['dealstage']['value']
        return hubspot.api.fetch_stage(stage_id)

    def get_amount(self):
        return int(self.data['properties']['amount']['value'])

    def get_amount_expected(self):
        return self.get_amount() * self.get_stage().get_win_probability()

    def is_won(self):
        return self.get_stage().is_won()


class Stage(object):
    data = None

    def __init__(self, data):
        self.data = data

    def is_won(self):
        return self.data['closedWon']

    def get_win_probability(self):
        return self.data['probability']
