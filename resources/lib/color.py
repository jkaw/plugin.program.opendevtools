import xbmcgui

from resources.lib import settings

_addon_name = settings.get_addon_info('name')
_color = settings.get_setting_string('general.color')

_color_chart = ["black", "white", "whitesmoke", "gainsboro", "lightgray",
                "silver", "darkgray", "gray", "dimgray", "snow",
                "floralwhite", "ivory", "beige", "cornsilk", "antiquewhite",
                "bisque", "blanchedalmond", "burlywood", "darkgoldenrod", "ghostwhite",
                "azure", "aliveblue", "lightsaltegray", "lightsteelblue", "powderblue",
                "lightblue", "skyblue", "lightskyblue", "deepskyblue", "dodgerblue",
                "royalblue", "blue", "mediumblue", "midnightblue", "navy",
                "darkblue", "cornflowerblue", "slateblue", "slategray", "yellowgreen",
                "springgreen", "seagreen", "steelblue", "teal", "fuchsia",
                "deeppink", "darkmagenta", "blueviolet", "darkviolet", "darkorchid",
                "darkslateblue", "darkslategray", "indigo", "cadetblue", "darkcyan",
                "darkturquoise", "turquoise", "cyan", "paleturquoise", "lightcyan",
                "mintcream", "honeydew", "aqua", "aquamarine", "chartreuse",
                "greenyellow", "palegreen", "lawngreen", "lightgreen", "lime",
                "mediumspringgreen", "mediumturquoise", "lightseagreen", "mediumaquamarine", "mediumseagreen",
                "limegreen", "darkseagreen", "forestgreen", "green", "darkgreen",
                "darkolivegreen", "olive", "olivedab", "darkkhaki", "khaki",
                "gold", "goldenrod", "lightyellow", "lightgoldenrodyellow", "lemonchiffon",
                "yellow", "seashell", "lavenderblush", "lavender", "lightcoral",
                "indianred", "darksalmon", "lightsalmon", "pink", "lightpink",
                "hotpink", "magenta", "plum", "violet", "orchid",
                "palevioletred", "mediumvioletred", "purple", "marron", "mediumorchid",
                "mediumpurple", "mediumslateblue", "thistle", "linen", "mistyrose",
                "palegoldenrod", "oldlace", "papayawhip", "moccasin", "navajowhite",
                "peachpuff", "sandybrown", "peru", "chocolate", "orange",
                "darkorange", "tomato", "orangered", "red", "crimson",
                "salmon", "coral", "firebrick", "brown", "darkred",
                "tan", "rosybrown", "sienna", "saddlebrown"]


def color_picker():
    select_list = []
    dialog = xbmcgui.Dialog()
    current_color = settings.get_setting_string('general.color')
    for i in _color_chart:
        select_list.append(color_string(i, i))
    color = dialog.select(
        "{}: {}".format(_addon_name, settings.get_localized_string(32050)), select_list,
        preselect=_color_chart.index(current_color)
    )
    if color > -1:
        settings.set_setting_string("general.display_color", color_string(_color_chart[color], _color_chart[color]))
        settings.set_setting_string("general.color", _color_chart[color])


def color_string(text, color=_color):
    return "[COLOR {}]{}[/COLOR]".format(color, text)