class Role(object):
    def __init__(self):
        self.roles ={
            "civilian":{
                "alignment":1,
                "summary":"",
                "abilities":"",
                "attributes":"",
                "goal":"",
            },
            "mafia":{
                "alignment":-1,
            },
            "detective":{
                "alignment":1,
            },
            "doctor":{
                "alignment":1,
            },
        };