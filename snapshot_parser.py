import json
import time
"""Creates a Dicitonary of required datapoints from the formatted snapshot
"""
def snapshot_dictifyer(snapshotformatted):
    snapshotdictionary = {"map": "", "round": "", "allplayers": "", "phase_countdowns": "", "auth": ""}       
    key_list = ["map", "round", "allplayers", "phase_countdowns", "auth"]

    iterator = 0
    while iterator < 5:
        dictionary = json.loads(str(snapshotformatted[iterator]))
        # allplayers - standardising key names
        if iterator == 2:
            while False:
                if len(list(dictionary.keys())) == 10: return True
                print('''Server has not been fully populated yet. Waiting 10 seconds and trying again.
If you keep getting this error, restart the program after the server has been populated with all 10 players.''')
                time.sleep(10)
                return False
            d3keys = list(dictionary.keys())
            for j in range(len(d3keys)):
                dictionary[str("player" + str(j + 1))] = dictionary.pop(str(d3keys[j]))
        snapshotdictionary[str(key_list[iterator])] = dictionary    
        iterator += 1    
    return snapshotdictionary

"""Compiles the list of attributes needed by the predictive model from the above Dictionary  
"""
def snapshot_arrayfier(snapshotdictionary):
    """Creating list of attributes for prediction

    ## Order of attributes - 
    ##'map', 'bomb_planted','ct_score', 't_score', 'time_left','ct_players_alive', 't_players_alive',
    ##'ct_health', 't_health', 'ct_armor', 't_armor','ct_pistols_special', 't_pistols_special', 't_pistols_standard',
    ##'ct_pistols_standard', 'ct_primaries_force', 't_primaries_force', 'ct_primaries_fullbuy', 't_primaries_fullbuy', 
    ##'ct_grenades', 't_grenades', 'ct_helmets', 't_helmets', 'ct_defuse_kits'

    ## Encoded Lables:Original Values
    ## round_winner = {'CT': 0, 'T': 1}
    ## map = {'de_cache': 0, 'de_dust2': 1, 'de_inferno': 2, 'de_mirage': 3, 'de_nuke': 4, 'de_overpass': 5, 'de_train': 6, 'de_vertigo': 7}
    ## bomb_planted = {False: 0, True: 1}
    """

    snap = snapshotdictionary
    predictors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    """adding var0 - map"""
    map_codes = {'de_cache': 0, 'de_dust2': 1, 'de_inferno': 2, 'de_mirage': 3, 'de_nuke': 4, 'de_overpass': 5,
                 'de_train': 6, 'de_vertigo': 7, 'de_ancient': 4}
    predictors[0] = map_codes[str(snap["map"]["name"])]

    """adding var1 - bomb_planted"""
    if "bomb" in snap["round"].keys():
        predictors[1] = 1

    """adding var2,3 - scores"""

    predictors[2] = snap["map"]["team_ct"]["score"]
    predictors[3] = snap["map"]["team_t"]["score"]

    """adding var4 - time_left"""

    predictors[4] = int(float(snap["phase_countdowns"]["phase_ends_in"]))

    """adding var 5,6,7,8 - players alive and team health"""

    counter_t = 0
    counter_ct = 0
    health_t = 0
    health_ct = 0
    for i in range(10):
        if snap["allplayers"][str("player" + str(i + 1))]["state"]["health"] > 0:
            if snap["allplayers"][str("player" + str(i + 1))]["team"] == "T":
                counter_t += 1
                health_t += snap["allplayers"][str("player" + str(i + 1))]["state"]["health"]
            if snap["allplayers"][str("player" + str(i + 1))]["team"] == "CT":
                counter_ct += 1
                health_ct += snap["allplayers"][str("player" + str(i + 1))]["state"]["health"]

    predictors[5] = counter_ct
    predictors[6] = counter_t
    predictors[7] = health_ct
    predictors[8] = health_t

    """adding var 9,10 - armor"""

    armor_t = 0
    armor_ct = 0

    for i in range(10):
        if snap["allplayers"][str("player" + str(i + 1))]["state"]["armor"] > 0:
            if snap["allplayers"][str("player" + str(i + 1))]["team"] == "T":
                armor_t += snap["allplayers"][str("player" + str(i + 1))]["state"]["armor"]
            if snap["allplayers"][str("player" + str(i + 1))]["team"] == "CT":
                armor_ct += snap["allplayers"][str("player" + str(i + 1))]["state"]["armor"]

    predictors[9] = armor_ct
    predictors[10] = armor_t

    """adding vars 11 to 20 - weapons and grenades"""

    ct_pistols_special = 0;
    t_pistols_special = 0;
    pistols_special = ["weapon_cz75auto", "weapon_elite", 'weapon_r8revolver', 'weapon_deagle', 'weapon_fiveseven',
                       'weapon_p250', 'weapon_tec9']
    t_pistols_standard = 0;
    ct_pistols_standard = 0;
    pistols_standard = ['weapon_usps', 'weapon_glock', 'weapon_hkp2000']
    ct_primaries_force = 0;
    t_primaries_force = 0;
    primaries_force = ['weapon_bizon', 'weapon_famas', 'weapon_galilar', 'weapon_mac10', 'weapon_mag7', 'weapon_mp5sd',
                       'weapon_mp7', 'weapon_mp9', 'weapon_negev', 'weapon_nova', 'weapon_p90', 'weapon_sawedoff',
                       'weapon_ssg08', 'weapon_ump45', 'weapon_xm1014', ]
    ct_primaries_fullbuy = 0;
    t_primaries_fullbuy = 0;
    primaries_fullbuy = ['weapon_ak47', 'weapon_aug', 'weapon_awp', 'weapon_g3sg1', 'weapon_m249', 'weapon_m4a1s',"weapon_m4a1",
                         "weapon_m4a1_silencer",'weapon_m4a4', 'weapon_scar20', 'weapon_sg556']
    ct_grenades = 0;
    t_grenades = 0;
    grenades = ["weapon_hegrenade", "weapon_frag_grenade", "weapon_flashbang", "weapon_smokegrenade", "weapon_decoy",
                "weapon_molotov", "weapon_incgrenade", ]
    ignore = ["weapon_knife", "weapon_knife_t", "weapon_c4"]

    for i in range(10):
        player = str("player" + str(i + 1))    
        if snap["allplayers"][player]["team"] == "T":
            for iterator in range(len(list(snap["allplayers"][player]["weapons"].keys()))):
                weapon = str("weapon_" + str(iterator))
                if snap["allplayers"][player]["weapons"][weapon]["name"] in ignore:
                        continue
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in pistols_special:
                        t_pistols_special += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in pistols_standard:
                        t_pistols_standard += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in primaries_force:
                       t_primaries_force += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in primaries_fullbuy:
                        t_primaries_fullbuy += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in grenades:
                        t_grenades += 1

        elif snap["allplayers"][player]["team"] == "CT":
            for iterator in range(len(list(snap["allplayers"][player]["weapons"].keys()))):
                weapon = str("weapon_" + str(iterator))
                if snap["allplayers"][player]["weapons"][weapon]["name"] in ignore:
                    continue
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in pistols_special:
                    ct_pistols_special += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in pistols_standard:
                    ct_pistols_standard += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in primaries_force:
                    ct_primaries_force += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in primaries_fullbuy:
                    ct_primaries_fullbuy += 1
                elif snap["allplayers"][player]["weapons"][weapon]["name"] in grenades:
                    ct_grenades += 1

    weapons_count = [ct_pistols_special, t_pistols_special, t_pistols_standard, ct_pistols_standard, 
                     ct_primaries_force, t_primaries_force, ct_primaries_fullbuy, t_primaries_fullbuy, ct_grenades, t_grenades]
    predictors[11:21] = weapons_count[0:10]

    """adding vars 21,22 - helmets"""

    helmets_t = 0
    helmets_ct = 0

    for i in range(10):
        player = str("player" + str(i + 1))
        if snap["allplayers"][player]["state"]["helmet"] is True:
            if snap["allplayers"][player]["team"] == "T":
                helmets_t += 1
            if snap["allplayers"][player]["team"] == "CT":
                helmets_ct += 1    

    predictors[21] = helmets_ct
    predictors[22] = helmets_t

    """adding var23 - defuse kits
    ##data not transmitted, check it out later"""

    return predictors