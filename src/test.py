
from common.config import Config, Setting, registered_settings

a = Setting("test",
{
    "fps": 60,
    "volume":69
}, {
    "fps" : {
        "value_type" : "selectable",
        "selectable" : [15, 30, 60, 144]
    },
    "volume" : {
        "type" : type(1),
        "value_type" : "bound",
        "min_val" : 0,
        "max_val" : 100
    }
})   

registered_settings.append(a)