from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class RadarParameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pri = db.Column(db.String(128))
    num_pulse = db.Column(db.String(128))
    range_samples = db.Column(db.String(128))

    def __init__(self, pri, num_pulse, range_samples):
        self.pri = pri
        self.num_pulse = num_pulse
        self.range_samples = range_samples

    def __repr__(self):
        return '<Pulse {}>'.format(self.num_pulse)

# class TargetDetails(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tgt_lat = db.Column(db.String(128))
#     tgt_long = db.Column(db.String(128))
#     tgt_name = db.Column(db.String(128))

class Pulse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(128))
    polarisation = db.Column(db.String(128))
    pulse_width = db.Column(db.String(128))
    pri = db.Column(db.String(128))

    def __init__(self, frequency, pulse_width, polarisation, pri):
        self.frequency = frequency
        self.pulse_width = pulse_width
        self.polarisation = polarisation
        self.pri = pri

    def __repr__(self):
        return '<Pulse {},{},{},{}>'.format(self.pulse_width,self.pri,self.polarisation,self.frequency)


# p = Pulse(frequency='1300',polarisation='VV',pulse_width='5')

class Experiments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(64), index=True, unique=False)
    polarisation = db.Column(db.String(64), index=True, unique=False)
    pulse_width = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Pulse {},{},{}>'.format(self.frequency,self.pulse_width,self.polarisation)
