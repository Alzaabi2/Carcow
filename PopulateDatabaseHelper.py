import string
from bs4 import BeautifulSoup
import requests
from csv import writer
import json
import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from lxml import etree
from scrapeV1_6_database_mass_search import *
from database import *

makes = ['acura', 'audi', 'bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'dodge', 'ford', 'gmc', 'honda', 'hyundai', 'infiniti', 'jaguar', 'jeep', 'kia', 'land_rover', 'lexus', 'lincoln', 'mazda', 'mercedes_benz', 'mitsubishi', 'nissan', 'porsche', 'ram', 'subaru', 'tesla', 'toyota', 'volkswagen', 'volvo', 'ac', 'alfa_romeo', 'am_general', 'american_motors', 'aston_martin', 'austin_healey', 'avanti_motors', 'bentley', 'bugatti', 'citroen', 'datsun', 'delorean', 'desoto', 'detomaso', 'edsel', 'ferrari', 'fiat', 'fisker', 'genesis', 'geo', 'hudson', 'hummer', 'international', 'isuzu', 'jensen', 'kaiser', 'karma', 'lamborghini', 'lasalle', 'lotus', 'lucid', 'maserati', 'maybach', 'mclaren', 'mercury', 'mg', 'mini', 'morgan', 'nash', 'oldsmobile', 'opel', 'packard', 'pagani', 'plymouth', 'polestar', 'pontiac', 'qvale', 'rivian', 'rolls_royce', 'saab', 'saleen', 'saturn', 'scion', 'smart', 'studebaker', 'sunbeam', 'suzuki', 'triumph', 'willys']
models = [['kia', 'sportage_plug_in_hybrid'], ['kia', 'stinger'], ['kia', 'telluride'], ['land_rover', 'defender'], ['land_rover', 'discovery'], ['land_rover', 'discovery_sport'], ['land_rover', 'freelander'], ['land_rover', 'lr2'], ['land_rover', 'lr3'], ['land_rover', 'lr4'], ['land_rover', 'range_rover'], ['land_rover', 'range_rover_evoque'], ['land_rover', 'range_rover_sport'], ['land_rover', 'range_rover_velar'], ['land_rover', 'series_ii'], ['land_rover', 'series_iii'], ['lexus', 'ct_200h'], ['lexus', 'es_all'], ['lexus', 'es_250'], ['lexus', 'es_300'], ['lexus', 'es_300h'], ['lexus', 'es_330'], ['lexus', 'es_350'], ['lexus', 'gs_all'], ['lexus', 'gs_200t'], ['lexus', 'gs_300'], ['lexus', 'gs_350'], ['lexus', 'gs_400'], ['lexus', 'gs_430'], ['lexus', 'gs_450h'], ['lexus', 'gs_460'], ['lexus', 'gs_f'], ['lexus', 'gx_460'], ['lexus', 'gx_470'], ['lexus', 'hs_250h'], ['lexus', 'is_all'], ['lexus', 'is_200t'], ['lexus', 'is_250'], ['lexus', 'is_250c'], ['lexus', 'is_300'], ['lexus', 'is_350'], ['lexus', 'is_350c'], ['lexus', 'is_500'], ['lexus', 'is_f'], ['lexus', 'lc_500'], ['lexus', 'lc_500h'], ['lexus', 'ls_all'], ['lexus', 'ls_400'], ['lexus', 'ls_430'], ['lexus', 'ls_460'], ['lexus', 'ls_500'], ['lexus', 'ls_500h'], ['lexus', 'ls_600h_l'], ['lexus', 'lx_all'], ['lexus', 'lx_450'], ['lexus', 'lx_470'], ['lexus', 'lx_570'], ['lexus', 'lx_600'], ['lexus', 'nx_200t'], ['lexus', 'nx_250'], ['lexus', 'nx_300'], ['lexus', 'nx_300h'], ['lexus', 'nx_350'], ['lexus', 'nx_350h'], ['lexus', 'nx_450h_plus'], ['lexus', 'rc_200t'], ['lexus', 'rc_300'], ['lexus', 'rc_350'], ['lexus', 'rc_f'], ['lexus', 'rx_all'], ['lexus', 'rx_300'], ['lexus', 'rx_330'], ['lexus', 'rx_350'], ['lexus', 'rx_350l'], ['lexus', 'rx_400h'], ['lexus', 'rx_450h'], ['lexus', 'rx_450hl'], ['lexus', 'sc_all'], ['lexus', 'sc_300'], ['lexus', 'sc_400'], ['lexus', 'sc_430'], ['lexus', 'ux_200'], ['lexus', 'ux_250h'], ['lincoln', 'aviator'], ['lincoln', 'blackwood'], ['lincoln', 'capri'], ['lincoln', 'continental'], ['lincoln', 'corsair'], ['lincoln', 'custom'], ['lincoln', 'ls'], ['lincoln', 'mkc'], ['lincoln', 'mks'], ['lincoln', 'mkt'], ['lincoln', 
'mkx'], ['lincoln', 'mkz'], ['lincoln', 'mkz_hybrid'], ['lincoln', 'mark_ii'], ['lincoln', 'mark_iii'], 
['lincoln', 'mark_iv'], ['lincoln', 'mark_lt'], ['lincoln', 'mark_v'], ['lincoln', 'mark_vi'], ['lincoln', 'mark_vii'], ['lincoln', 'mark_viii'], ['lincoln', 'nautilus'], ['lincoln', 'navigator'], ['lincoln', 'navigator_l'], ['lincoln', 'premiere'], ['lincoln', 'town_car'], ['lincoln', 'versailles'], ['lincoln', 'zephyr'], ['mazda', '1200'], ['mazda', '323'], ['mazda', '626'], ['mazda', 'b_series_trucks'], ['mazda', 'b2000'], ['mazda', 'b2200'], ['mazda', 'b2300'], ['mazda', 'b2600'], ['mazda', 'b3000'], ['mazda', 
'b4000'], ['mazda', 'b2500'], ['mazda', 'cx_3'], ['mazda', 'cx_30'], ['mazda', 'cx_5'], ['mazda', 'cx_50'], ['mazda', 'cx_7'], ['mazda', 'cx_9'], ['mazda', 'mpv'], ['mazda', 'mx_3'], ['mazda', 'mx_30'], ['mazda', 'mx_5_miata'], ['mazda', 'mx_5_miata_rf'], ['mazda', 'mazda2'], ['mazda', 'mazda3'], ['mazda', 'mazda5'], ['mazda', 'mazda6'], ['mazda', 'mazdaspeed_miata_mx_5'], ['mazda', 'mazdaspeed3'], ['mazda', 'millenia'], ['mazda', 'pickup_truck'], ['mazda', 'protege'], ['mazda', 'protege5'], ['mazda', 'rx_7'], ['mazda', 'rx_8'], ['mazda', 'tribute'], ['mazda', 'tribute_hybrid'], ['mercedes_benz', '190'], ['mercedes_benz', '190sl'], ['mercedes_benz', '200'], ['mercedes_benz', '230'], ['mercedes_benz', '230sl'], ['mercedes_benz', '240'], ['mercedes_benz', '280se'], ['mercedes_benz', '280sl'], ['mercedes_benz', '300'], ['mercedes_benz', '300c'], ['mercedes_benz', '380sl'], ['mercedes_benz', '450sl'], ['mercedes_benz', '600'], ['mercedes_benz', 'a_class'], ['mercedes_benz', 'amg_a_35'], ['mercedes_benz', 'amg_glb_35'], ['mercedes_benz', 'amg_gt'], ['mercedes_benz', 'amg_gt_43'], ['mercedes_benz', 'amg_gt_53'], ['mercedes_benz', 'amg_gt_63'], ['mercedes_benz', 'b_class'], ['mercedes_benz', 'b_class_electric_drive'], ['mercedes_benz', 'c_all'], ['mercedes_benz', 'amg_c'], ['mercedes_benz', 'amg_c_43'], ['mercedes_benz', 'amg_c_63'], ['mercedes_benz', 'c_class'], ['mercedes_benz', 'cl_class'], ['mercedes_benz', 'cla_all'], ['mercedes_benz', 'amg_cla'], ['mercedes_benz', 'amg_cla_35'], ['mercedes_benz', 'amg_cla_45'], ['mercedes_benz', 'cla_250'], ['mercedes_benz', 'cla_class'], ['mercedes_benz', 'clk_class'], ['mercedes_benz', 'cls_all'], ['mercedes_benz', 'amg_cls_53'], ['mercedes_benz', 'amg_cls_63'], ['mercedes_benz', 'cls_450'], ['mercedes_benz', 'cls_550'], ['mercedes_benz', 'cls_class'], ['mercedes_benz', 'e_all'], ['mercedes_benz', 'amg_e'], ['mercedes_benz', 'amg_e_43'], ['mercedes_benz', 'amg_e_53'], ['mercedes_benz', 'amg_e_63'], ['mercedes_benz', 'e_class'], ['mercedes_benz', 'eqb_350'], ['mercedes_benz', 'eqs_450_plus'], ['mercedes_benz', 
'eqs_580'], ['mercedes_benz', 'g_all'], ['mercedes_benz', 'amg_g'], ['mercedes_benz', 'amg_g_63'], ['mercedes_benz', 'g_550_4x4_squared'], ['mercedes_benz', 'g_class'], ['mercedes_benz', 'gl_all'], ['mercedes_benz', 'amg_gl'], ['mercedes_benz', 'gl_class'], ['mercedes_benz', 'gla_all'], ['mercedes_benz', 'amg_gla'], ['mercedes_benz', 'amg_gla_35'], ['mercedes_benz', 'amg_gla_45'], ['mercedes_benz', 'gla_250'], ['mercedes_benz', 'gla_class'], ['mercedes_benz', 'glb_250'], ['mercedes_benz', 'glc_all'], ['mercedes_benz', 'amg_glc_43'], ['mercedes_benz', 'amg_glc_63'], ['mercedes_benz', 'glc_300'], ['mercedes_benz', 'glc_350e'], ['mercedes_benz', 'glc_class'], ['mercedes_benz', 'gle_all'], ['mercedes_benz', 'amg_gle'], ['mercedes_benz', 'amg_gle_43'], ['mercedes_benz', 'amg_gle_53'], ['mercedes_benz', 'amg_gle_63'], ['mercedes_benz', 'gle_350'], ['mercedes_benz', 'gle_400'], ['mercedes_benz', 'gle_450'], ['mercedes_benz', 'gle_550e_plug_in_hybrid'], ['mercedes_benz', 'gle_580'], ['mercedes_benz', 'gle_class'], ['mercedes_benz', 
'glk_class'], ['mercedes_benz', 'gls_all'], ['mercedes_benz', 'amg_gls_63'], ['mercedes_benz', 'gls_450'], ['mercedes_benz', 'gls_550'], ['mercedes_benz', 'gls_580'], ['mercedes_benz', 'maybach_gls_600'], ['mercedes_benz', 'm_class'], ['mercedes_benz', 'maybach_s'], ['mercedes_benz', 'maybach_s_560'], ['mercedes_benz', 'maybach_s_580'], ['mercedes_benz', 'maybach_s_650'], ['mercedes_benz', 'metris'], ['mercedes_benz', 'r_class'], ['mercedes_benz', 's_all'], ['mercedes_benz', 'amg_s'], ['mercedes_benz', 'amg_s_63'], ['mercedes_benz', 'amg_s_65'], ['mercedes_benz', 's_class'], ['mercedes_benz', 'sl_all'], ['mercedes_benz', 'amg_sl'], ['mercedes_benz', 'amg_sl_55'], ['mercedes_benz', 'amg_sl_63'], ['mercedes_benz', 'sl_450'], ['mercedes_benz', 'sl_550'], ['mercedes_benz', 'sl_class'], ['mercedes_benz', 'slc_all'], ['mercedes_benz', 'amg_slc_43'], ['mercedes_benz', 'slc_300'], ['mercedes_benz', 'slk_all'], ['mercedes_benz', 'slk_class'], ['mercedes_benz', 'slr_mclaren'], ['mercedes_benz', 'sls_amg'], ['mercedes_benz', 'sprinter'], ['mercedes_benz', 'sprinter_1500'], ['mercedes_benz', 'sprinter_2500'], ['mercedes_benz', 'sprinter_3500'], ['mercedes_benz', 'sprinter_3500xd'], ['mercedes_benz', 'sprinter_4500'], ['mitsubishi', '3000gt'], ['mitsubishi', 'diamante'], ['mitsubishi', 'eclipse'], ['mitsubishi', 'eclipse_cross'], ['mitsubishi', 'endeavor'], ['mitsubishi', 'expo'], ['mitsubishi', 'galant'], ['mitsubishi', 'lancer'], ['mitsubishi', 'lancer_evolution'], ['mitsubishi', 'lancer_sportback'], ['mitsubishi', 'mirage'], ['mitsubishi', 'mirage_g4'], ['mitsubishi', 'montero'], ['mitsubishi', 'montero_sport'], ['mitsubishi', 'outlander'], ['mitsubishi', 'outlander_phev'], ['mitsubishi', 'outlander_sport'], ['mitsubishi', 'pickup_truck'], ['mitsubishi', 'raider'], ['mitsubishi', 'sigma'], ['mitsubishi', 'i_miev'], ['nissan', '200sx'], ['nissan', '240sx'], ['nissan', '280zx'], ['nissan', '300zx'], ['nissan', '350z'], ['nissan', '370z'], ['nissan', 'altima'], ['nissan', 'altima_hybrid'], ['nissan', 'armada'], ['nissan', 'cube'], ['nissan', 'frontier'], ['nissan', 'gt_r'], ['nissan', 'juke'], ['nissan', 'kicks'], ['nissan', 'leaf'], ['nissan', 'maxima'], ['nissan', 'murano'], ['nissan', 'murano_crosscabriolet'], ['nissan', 'murano_hybrid'], ['nissan', 'nv_vans'], ['nissan', 'nv_cargo'], ['nissan', 'nv_cargo_nv1500'], ['nissan', 'nv_cargo_nv2500_hd'], ['nissan', 
'nv_cargo_nv3500_hd'], ['nissan', 'nv_passenger'], ['nissan', 'nv_passenger_nv3500_hd'], ['nissan', 'nv200'], ['nissan', 'nx'], ['nissan', 'pathfinder'], ['nissan', 'pathfinder_hybrid'], ['nissan', 'pickup_truck'], ['nissan', 'quest'], ['nissan', 'rogue'], ['nissan', 'rogue_hybrid'], ['nissan', 'rogue_select'], ['nissan', 'rogue_sport'], ['nissan', 'sentra'], ['nissan', 'titan'], ['nissan', 'titan_xd'], ['nissan', 'van'], ['nissan', 'versa'], ['nissan', 'versa_note'], ['nissan', 'xterra'], ['nissan', 'z'], ['porsche', '356'], ['porsche', '718_boxster'], ['porsche', '718_cayman'], ['porsche', '718_spyder'], ['porsche', '911'], ['porsche', '912'], ['porsche', '914'], ['porsche', '918_spyder'], ['porsche', '924'], ['porsche', '928'], ['porsche', '930'], ['porsche', '944'], ['porsche', '968'], ['porsche', 'boxster'], ['porsche', 'carrera_gt'], ['porsche', 'cayenne'], ['porsche', 'cayenne_e_hybrid'], ['porsche', 'cayenne_e_hybrid_coupe'], ['porsche', 'cayenne_hybrid'], ['porsche', 'cayman'], ['porsche', 'macan'], ['porsche', 'panamera'], ['porsche', 'panamera_e_hybrid'], ['porsche', 'panamera_e_hybrid_sport_turismo'], ['porsche', 'panamera_hybrid'], ['porsche', 'panamera_sport_turismo'], ['porsche', 's90'], ['porsche', 'taycan'], ['porsche', 'taycan_cross_turismo'], ['ram', '1500'], ['ram', '1500_classic'], ['ram', '2500'], ['ram', '3500'], ['ram', 'cargo'], ['ram', 'promaster_1500'], ['ram', 'promaster_2500'], ['ram', 'promaster_2500_window_van'], ['ram', 'promaster_3500'], ['ram', 'promaster_3500_window_van'], ['ram', 'promaster_city'], 
['subaru', '1600'], ['subaru', 'ascent'], ['subaru', 'b9_tribeca'], ['subaru', 'brz'], ['subaru', 'baja'], ['subaru', 'crosstrek'], ['subaru', 'crosstrek_hybrid'], ['subaru', 'dl'], ['subaru', 'forester'], ['subaru', 'impreza'], ['subaru', 'impreza_outback_sport'], ['subaru', 'impreza_wrx'], ['subaru', 'impreza_wrx_sti'], ['subaru', 'legacy'], ['subaru', 'outback'], ['subaru', 'sti_s209'], ['subaru', 'tribeca'], 
['subaru', 'wrx'], ['subaru', 'wrx_sti'], ['subaru', 'xv_crosstrek'], ['subaru', 'xv_crosstrek_hybrid'], ['tesla', 'model_3'], ['tesla', 'model_s'], ['tesla', 'model_x'], ['tesla', 'model_y'], ['tesla', 'roadster'], ['toyota', '4runner'], ['toyota', '86'], ['toyota', 'avalon'], ['toyota', 'avalon_hybrid'], ['toyota', 'c_hr'], ['toyota', 'camry'], ['toyota', 'camry_hybrid'], ['toyota', 'camry_solara'], ['toyota', 
'celica'], ['toyota', 'corolla'], ['toyota', 'corolla_cross'], ['toyota', 'corolla_hatchback'], ['toyota', 'corolla_hybrid'], ['toyota', 'corolla_im'], ['toyota', 'corona'], ['toyota', 'cressida'], ['toyota', 'echo'], ['toyota', 'fj_cruiser'], ['toyota', 'gr86'], ['toyota', 'highlander'], ['toyota', 'highlander_hybrid'], ['toyota', 'land_cruiser'], ['toyota', 'mr2'], ['toyota', 'matrix'], ['toyota', 'mirai'], ['toyota', 'pickup_truck'], ['toyota', 'previa'], ['toyota', 'prius'], ['toyota', 'prius_plug_in'], ['toyota', 'prius_prime'], ['toyota', 'prius_c'], ['toyota', 'prius_v'], ['toyota', 'rav4'], ['toyota', 'rav4_ev'], ['toyota', 'rav4_hybrid'], ['toyota', 'rav4_prime'], ['toyota', 'sequoia'], ['toyota', 'sienna'], ['toyota', 'supra'], ['toyota', 't100'], ['toyota', 'tacoma'], ['toyota', 'tercel'], ['toyota', 'tundra'], ['toyota', 'tundra_hybrid'], ['toyota', 'van'], ['toyota', 'venza'], ['toyota', 'yaris'], ['toyota', 'yaris_sedan'], ['toyota', 'yaris_ia'], ['toyota', 'bz4x'], ['volkswagen', '1600'], ['volkswagen', 'arteon'], ['volkswagen', 'atlas'], ['volkswagen', 'atlas_cross_sport'], ['volkswagen', 'beetle'], ['volkswagen', 'beetle_pre_1980'], ['volkswagen', 'cc'], ['volkswagen', 'cabrio'], ['volkswagen', 'cabriolet'], ['volkswagen', 'corrado'], ['volkswagen', 'eos'], ['volkswagen', 'eurovan'], ['volkswagen', 'fox'], ['volkswagen', 'gli'], ['volkswagen', 'gti'], ['volkswagen', 'golf'], ['volkswagen', 'golf_alltrack'], ['volkswagen', 'golf_gti'], ['volkswagen', 'golf_r'], ['volkswagen', 'golf_sportwagen'], ['volkswagen', 'id.4'], ['volkswagen', 'jetta'], ['volkswagen', 'jetta_gli'], ['volkswagen', 'jetta_hybrid'], ['volkswagen', 'jetta_sportwagen'], ['volkswagen', 'karmann_ghia'], ['volkswagen', 'microbus'], ['volkswagen', 'new_beetle'], ['volkswagen', 'new_cabrio'], ['volkswagen', 'passat'], ['volkswagen', 'phaeton'], ['volkswagen', 'r32'], ['volkswagen', 'rabbit'], ['volkswagen', 'routan'], ['volkswagen', 'super_beetle'], ['volkswagen', 'taos'], ['volkswagen', 'thing'], ['volkswagen', 'tiguan'], ['volkswagen', 'tiguan_limited'], ['volkswagen', 'touareg'], ['volkswagen', 'touareg_2'], ['volkswagen', 'touareg_hybrid'], ['volkswagen', 'type_3'], ['volkswagen', 'van'], ['volkswagen', 'vanagon'], ['volkswagen', 'e_golf'], ['volvo', '164'], ['volvo', '240'], ['volvo', '740'], ['volvo', '760'], ['volvo', '850'], ['volvo', '940'], ['volvo', 'c30'], ['volvo', 'c40_recharge_pure_electric'], ['volvo', 'c70'], ['volvo', 'coupe'], ['volvo', 'dl'], ['volvo', 
's40'], ['volvo', 's60'], ['volvo', 's60_cross_country'], ['volvo', 's60_hybrid'], ['volvo', 's60_inscription'], ['volvo', 's60_recharge_plug_in_hybrid'], ['volvo', 's70'], ['volvo', 's80'], ['volvo', 's90'], ['volvo', 's90_hybrid'], ['volvo', 's90_recharge_plug_in_hybrid'], ['volvo', 'v50'], ['volvo', 'v60'], 
['volvo', 'v60_cross_country'], ['volvo', 'v60_hybrid'], ['volvo', 'v60_recharge_plug_in_hybrid'], ['volvo', 'v70'], ['volvo', 'v90'], ['volvo', 'v90_cross_country'], ['volvo', 'xc40'], ['volvo', 'xc40_recharge_pure_electric'], ['volvo', 'xc60'], ['volvo', 'xc60_hybrid'], ['volvo', 'xc60_recharge_plug_in_hybrid'], ['volvo', 'xc70'], ['volvo', 'xc90'], ['volvo', 'xc90_hybrid'], ['volvo', 'xc90_recharge_plug_in_hybrid'], ['ac', '428'], ['ac', 'ace'], ['ac', 'aceca'], ['ac', 'shelby_cobra'], ['alfa_romeo', '164'], ['alfa_romeo', '1900'], ['alfa_romeo', '2000'], ['alfa_romeo', '2600'], ['alfa_romeo', '4c'], ['alfa_romeo', '4c_spider'], ['alfa_romeo', '8c_competizione'], ['alfa_romeo', 'duetto'], ['alfa_romeo', 'gtv'], ['alfa_romeo', 'giulia'], ['alfa_romeo', 'giulietta'], ['alfa_romeo', 'spider'], ['alfa_romeo', 'sprint'], ['alfa_romeo', 'stelvio'], ['am_general', 'hummer'], ['american_motors', 'ambassador'], ['american_motors', 'classic'], ['american_motors', 'concord'], ['american_motors', 'eagle_30'], ['american_motors', 'encore'], ['american_motors', 'hornet'], ['american_motors', 'matador'], ['american_motors', 'metropolitan'], ['american_motors', 'pacer'], ['american_motors', 'rogue'], ['aston_martin', 'db_ar1_zagato'], ['aston_martin', 'db11'], ['aston_martin', 'db2_4'], ['aston_martin', 'db4'], ['aston_martin', 'db5'], ['aston_martin', 'db6'], ['aston_martin', 'db7'], ['aston_martin', 'db7_vantage'], ['aston_martin', 'db9'], ['aston_martin', 'dbs'], ['aston_martin', 'dbx'], ['aston_martin', 'rapide'], ['aston_martin', 'rapide_s'], ['aston_martin', 'v12_vanquish'], ['aston_martin', 'v12_vantage'], ['aston_martin', 'v12_vantage_s'], ['aston_martin', 'v8_vantage'], ['aston_martin', 'v8_vantage_s'], ['aston_martin', 'vanquish'], ['aston_martin', 'vantage'], ['aston_martin', 'vantage_gt'], ['aston_martin', 'virage'], ['aston_martin', 'volante'], ['austin_healey', '100'], ['austin_healey', '100_6'], ['austin_healey', '100m'], ['austin_healey', 
'3000'], ['austin_healey', '3000_mk_ii'], ['austin_healey', '3000_mk_iii'], ['austin_healey', 'sprite'], ['avanti_motors', 'avanti'], ['avanti_motors', 'avanti_ii'], ['bentley', 'arnage'], ['bentley', 'azure'], ['bentley', 'bentayga'], ['bentley', 'bentayga_hybrid'], ['bentley', 'brooklands'], ['bentley', 'continental'], ['bentley', 'continental_flying_spur'], ['bentley', 'continental_gt'], ['bentley', 'continental_gtc'], ['bentley', 'continental_supersports'], ['bentley', 'corniche'], ['bentley', 'eight'], ['bentley', 'flying_spur'], ['bentley', 'flying_spur_hybrid'], ['bentley', 'mark_vi'], ['bentley', 'mulsanne'], ['bentley', 'r_type'], ['bentley', 's1'], ['bentley', 's3'], ['bentley', 't2'], ['bentley', 'turbo_r'], ['bugatti', 'chiron'], ['bugatti', 'veyron'], ['bugatti', 'veyron_16.4'], ['citroen', 'ds21'], ['datsun', '110'], ['datsun', '1500'], ['datsun', '1600'], ['datsun', '2000'], ['datsun', '200sx'], ['datsun', '210'], ['datsun', '240z'], ['datsun', '280z'], ['datsun', '280zx'], ['datsun', '510'], ['datsun', '620'], ['datsun', 'maxima'], ['datsun', 'sentra'], ['delorean', 'dmc_12'], ['desoto', 'adventurer'], ['desoto', 'custom'], ['desoto', 'deluxe'], ['desoto', 'firedome'], ['desoto', 'sc'], ['detomaso', 'mangusta'], 
['detomaso', 'pantera'], ['edsel', 'corsair'], ['edsel', 'pacer'], ['edsel', 'ranger'], ['edsel', 'villager'], ['ferrari', '308'], ['ferrari', '328'], ['ferrari', '330'], ['ferrari', '348'], ['ferrari', '360_modena'], ['ferrari', '360_spider'], ['ferrari', '365'], ['ferrari', '400i'], ['ferrari', '456_gt'], ['ferrari', '456_m'], ['ferrari', '458_italia'], ['ferrari', '458_speciale'], ['ferrari', '458_spider'], ['ferrari', '488_gtb'], ['ferrari', '488_pista'], ['ferrari', '488_pista_spider'], ['ferrari', '488_spider'], ['ferrari', '512'], ['ferrari', '512_tr'], ['ferrari', '550_maranello'], ['ferrari', '575_m'], ['ferrari', '599_gtb_fiorano'], ['ferrari', '599_gto'], ['ferrari', '612_scaglietti'], ['ferrari', '812_gts'], ['ferrari', '812_superfast'], ['ferrari', 'california'], ['ferrari', 'challenge_stradale'], ['ferrari', 'daytona'], ['ferrari', 'dino'], ['ferrari', 'f12berlinetta'], ['ferrari', 'f12tdf'], ['ferrari', 'f355'], ['ferrari', 'f40'], ['ferrari', 'f430'], ['ferrari', 'f50'], ['ferrari', 'f8_spider'], ['ferrari', 
'f8_tributo'], ['ferrari', 'ff'], ['ferrari', 'gt'], ['ferrari', 'gt_2_plus_2'], ['ferrari', 'gtc4lusso'], ['ferrari', 'gto'], ['ferrari', 'laferrari_aperta'], ['ferrari', 'mondial'], ['ferrari', 'mondial_t'], ['ferrari', 'portofino'], ['ferrari', 'portofino_m'], ['ferrari', 'roma'], ['ferrari', 'sf90_spider'], ['ferrari', 'sf90_stradale'], ['ferrari', 'superamerica'], ['ferrari', 'testarossa'], ['fiat', '1200'], ['fiat', '124'], ['fiat', '124_spider'], ['fiat', '128'], ['fiat', '1500'], ['fiat', '1900'], ['fiat', 
'500'], ['fiat', '500c'], ['fiat', '500l'], ['fiat', '500x'], ['fiat', '500e'], ['fiat', '600'], ['fiat', '850'], ['fiat', 'pininfarina'], ['fiat', 'spider_2000'], ['fisker', 'karma'], ['genesis', 'g70'], ['genesis', 'g80'], ['genesis', 'g90'], ['genesis', 'gv60'], ['genesis', 'gv70'], ['genesis', 'gv80'], ['geo', 'metro'], ['geo', 'prizm'], ['geo', 'storm'], ['geo', 'tracker'], ['hudson', 'commodore'], ['hudson', 'custom'], ['hudson', 'deluxe'], ['hudson', 'eight'], ['hudson', 'hornet'], ['hudson', 'pickup_truck'], ['hudson', 'standard'], ['hudson', 'super'], ['hudson', 'super_eight'], ['hudson', 'super_six'], ['hummer', 'h1'], ['hummer', 'h1_alpha'], ['hummer', 'h2'], ['hummer', 'h3'], ['hummer', 'h3t'], ['international', 'm'], ['international', 'mxt'], ['international', 'pickup_truck'], ['international', 'scout'], ['isuzu', 'amigo'], ['isuzu', 'axiom'], ['isuzu', 'isuzu_trucks'], ['isuzu', 'pickup_truck'], ['isuzu', 'i_290'], ['isuzu', 'rodeo'], ['isuzu', 'rodeo_sport'], ['isuzu', 'trooper'], ['isuzu', 'vehicross'], ['jensen', 'gt'], ['jensen', 'interceptor'], ['jensen', 'jensen_healey'], ['kaiser', 'darrin'], ['kaiser', 'manhattan'], ['kaiser', 'special'], ['karma', 'gs_6'], ['karma', 'revero'], ['lamborghini', '400_gt'], ['lamborghini', 'aventador'], ['lamborghini', 'aventador_s'], ['lamborghini', 'aventador_svj'], ['lamborghini', 'countach'], ['lamborghini', 'diablo'], ['lamborghini', 'gallardo'], ['lamborghini', 'huracan'], ['lamborghini', 'huracan_evo'], ['lamborghini', 'huracan_sto'], ['lamborghini', 'islero'], ['lamborghini', 'murcielago'], ['lamborghini', 'silhouette'], ['lamborghini', 'urus'], ['lasalle', '328'], ['lasalle', '340'], ['lasalle', '50'], ['lotus', 'elise'], ['lotus', 'esprit'], ['lotus', 'esprit_v8'], ['lotus', 'evora'], ['lotus', 'evora_400'], ['lotus', 'evora_gt'], ['lotus', 'exige'], ['lotus', 'exige_s'], ['lucid', 'air'], ['maserati', '228'], ['maserati', '3500'], ['maserati', '430'], ['maserati', 'bora'], ['maserati', 'coupe'], ['maserati', 'ghibli'], ['maserati', 'gransport'], ['maserati', 'gransport_spyder'], ['maserati', 'granturismo'], ['maserati', 'indy'], ['maserati', 'khamsin'], ['maserati', 'levante'], ['maserati', 'mc20'], ['maserati', 'mexico'], ['maserati', 'quattroporte'], ['maserati', 'sebring'], ['maserati', 'spyder'], ['maybach', 'type_57'], ['maybach', 'type_62'], ['mclaren', '570gt'], ['mclaren', '570s'], ['mclaren', '600lt'], ['mclaren', '620r'], ['mclaren', '650s'], ['mclaren', '675lt'], ['mclaren', '720s'], ['mclaren', '765lt'], ['mclaren', 'elva'], ['mclaren', 'gt'], ['mclaren', 'mp4_12c'], ['mclaren', 
'p1'], ['mclaren', 'senna'], ['mercury', 'brougham'], ['mercury', 'capri'], ['mercury', 'colony_park'], 
['mercury', 'comet'], ['mercury', 'cougar'], ['mercury', 'custom'], ['mercury', 'eight'], ['mercury', 'grand_marquis'], ['mercury', 'marauder'], ['mercury', 'mariner'], ['mercury', 'mariner_hybrid'], ['mercury', 'marquis'], ['mercury', 'medalist'], ['mercury', 'milan'], ['mercury', 'milan_hybrid'], ['mercury', 
'montclair'], ['mercury', 'montego'], ['mercury', 'monterey'], ['mercury', 'mountaineer'], ['mercury', 'parklane'], ['mercury', 'sable'], ['mercury', 'series_19a'], ['mercury', 'tracer'], ['mercury', 'villager'], ['mercury', 'voyager'], ['mercury', 'zephyr'], ['mg', 'mga'], ['mg', 'mgb'], ['mg', 'midget'], ['mg', 'tc_roadster'], ['mg', 'td'], ['mg', 'tf'], ['mg', 'yt'], ['mini', 'clubman'], ['mini', 'convertible'], ['mini', 'cooper'], ['mini', 'cooper_clubman'], ['mini', 'cooper_countryman'], ['mini', 'cooper_s'], 
['mini', 'cooper_s_clubman'], ['mini', 'cooper_s_countryman'], ['mini', 'countryman'], ['mini', 'coupe'], ['mini', 'e_countryman'], ['mini', 'hardtop'], ['mini', 'john_cooper_works_gp'], ['mini', 'paceman'], 
['mini', 'roadster'], ['mini', 'se_countryman'], ['mini', 'se_hardtop'], ['morgan', 'plus_4'], ['morgan', 'roadster'], ['nash', '400'], ['nash', '600'], ['nash', '880'], ['nash', 'ambassador'], ['nash', 'deluxe'], ['nash', 'metropolitan'], ['nash', 'special'], ['nash', 'standard'], ['nash', 'statesman'], ['nash', 'super'], ['oldsmobile', '442'], ['oldsmobile', '76'], ['oldsmobile', '88'], ['oldsmobile', '98'], ['oldsmobile', 'achieva'], ['oldsmobile', 'alero'], ['oldsmobile', 'aurora'], ['oldsmobile', 'bravada'], ['oldsmobile', 'custom'], ['oldsmobile', 'custom_cruiser'], ['oldsmobile', 'cutlass'], ['oldsmobile', 'cutlass_calais'], ['oldsmobile', 'cutlass_ciera'], ['oldsmobile', 'cutlass_supreme'], ['oldsmobile', 'defender'], ['oldsmobile', 'delta_88'], ['oldsmobile', 'dynamic_88'], ['oldsmobile', 'eighty_eight'], ['oldsmobile', 'fiesta'], ['oldsmobile', 'intrigue'], ['oldsmobile', 'lss'], ['oldsmobile', 'model_a'], ['oldsmobile', 'model_b'], ['oldsmobile', 'model_h'], ['oldsmobile', 'model_s'], ['oldsmobile', 'model_x'], ['oldsmobile', 'regency'], ['oldsmobile', 'silhouette'], ['oldsmobile', 'special'], ['oldsmobile', 'starfire'], ['oldsmobile', 'super_88'], ['oldsmobile', 'toronado'], ['oldsmobile', 'vista_cruiser'], ['opel', 
'1900'], ['opel', 'caravan'], ['opel', 'gt'], ['packard', '110'], ['packard', '120'], ['packard', '1200'], ['packard', '1600'], ['packard', '200'], ['packard', '300'], ['packard', '400'], ['packard', '626'], 
['packard', '640'], ['packard', '645'], ['packard', '740'], ['packard', '745'], ['packard', '840'], ['packard', '900'], ['packard', 'caribbean'], ['packard', 'cavalier'], ['packard', 'clipper'], ['packard', 'custom'], ['packard', 'deluxe'], ['packard', 'eight'], ['packard', 'lebaron'], ['packard', 'model_18'], 
['packard', 'model_a'], ['packard', 'model_b'], ['packard', 'model_s'], ['packard', 'patrician'], ['packard', 'standard'], ['packard', 'super'], ['packard', 'super_eight'], ['pagani', 'huayra'], ['plymouth', 
'acclaim'], ['plymouth', 'barracuda'], ['plymouth', 'belvedere'], ['plymouth', 'cambridge'], ['plymouth', 'colt'], ['plymouth', 'concord'], ['plymouth', 'conquest'], ['plymouth', 'cranbrook'], ['plymouth', 'cuda'], ['plymouth', 'deluxe'], ['plymouth', 'duster'], ['plymouth', 'fury'], ['plymouth', 'gtx'], ['plymouth', 'grand_voyager'], ['plymouth', 'laser'], ['plymouth', 'neon'], ['plymouth', 'pickup_truck'], ['plymouth', 'prowler'], ['plymouth', 'roadrunner'], ['plymouth', 'satellite'], ['plymouth', 'savoy'], ['plymouth', 'scamp'], ['plymouth', 'sebring'], ['plymouth', 'sedan_delivery'], ['plymouth', 'special_deluxe'], ['plymouth', 'sport_fury'], ['plymouth', 'standard'], ['plymouth', 'suburban'], ['plymouth', 'valiant'], ['plymouth', 'van'], ['plymouth', 'volare'], ['plymouth', 'voyager'], ['polestar', '1'], ['polestar', '2'], ['pontiac', '2000'], ['pontiac', 'aztek'], ['pontiac', 'bonneville'], ['pontiac', 'catalina'], ['pontiac', 'chieftain'], ['pontiac', 'custom'], ['pontiac', 'deluxe'], ['pontiac', 'fiero'], ['pontiac', 'firebird'], ['pontiac', 'g3'], ['pontiac', 'g5'], ['pontiac', 'g6'], ['pontiac', 'g8'], ['pontiac', 'gto'], ['pontiac', 'grand_am'], ['pontiac', 'grand_prix'], ['pontiac', 'grand_ville'], ['pontiac', 'lemans'], ['pontiac', 'montana'], ['pontiac', 'montana_sv6'], ['pontiac', 'phoenix'], ['pontiac', 'safari'], 
['pontiac', 'solstice'], ['pontiac', 'star_chief'], ['pontiac', 'streamliner'], ['pontiac', 'sunfire'], 
['pontiac', 'super_deluxe'], ['pontiac', 'tempest'], ['pontiac', 'torrent'], ['pontiac', 'vibe'], ['qvale', 'mangusta'], ['rivian', 'r1s'], ['rivian', 'r1t'], ['rolls_royce', 'corniche'], ['rolls_royce', 'cullinan'], ['rolls_royce', 'dawn'], ['rolls_royce', 'ghost'], ['rolls_royce', 'phantom'], ['rolls_royce', 
'phantom_coupe'], ['rolls_royce', 'phantom_drophead_coupe'], ['rolls_royce', 'phantom_v'], ['rolls_royce', 'phantom_vi'], ['rolls_royce', 'silver_cloud_i'], ['rolls_royce', 'silver_cloud_ii'], ['rolls_royce', 'silver_cloud_iii'], ['rolls_royce', 'silver_dawn'], ['rolls_royce', 'silver_seraph'], ['rolls_royce', 
'silver_shadow'], ['rolls_royce', 'silver_shadow_ii'], ['rolls_royce', 'silver_spirit'], ['rolls_royce', 'silver_spur'], ['rolls_royce', 'silver_spur_ii'], ['rolls_royce', 'silver_wraith'], ['rolls_royce', 'silver_wraith_ii'], ['rolls_royce', 'wraith'], ['saab', '9_3'], ['saab', '9_3x'], ['saab', '9_4x'], ['saab', '9_5'], ['saab', '9_7x'], ['saab', '900'], ['saab', '9000'], ['saab', '96'], ['saab', 'gt'], ['saab', 'monte_carlo'], ['saab', 'sonett'], ['saleen', 's7'], ['saturn', 'astra'], ['saturn', 'aura'], ['saturn', 'aura_hybrid_all'], ['saturn', 'aura_green_line'], ['saturn', 'ion'], ['saturn', 'l'], ['saturn', 'ls'], ['saturn', 'lw'], ['saturn', 'outlook'], ['saturn', 'sc'], ['saturn', 'sl'], ['saturn', 'sw'], ['saturn', 'sky'], ['saturn', 'vue'], ['saturn', 'vue_hybrid_all'], ['saturn', 'vue_green_line'], ['saturn', 'vue_hybrid'], ['scion', 'fr_s'], ['scion', 'ia'], ['scion', 'im'], ['scion', 'iq'], ['scion', 'tc'], ['scion', 'xa'], ['scion', 'xb'], ['scion', 'xd'], ['smart', 'eq_fortwo'], ['smart', 'fortwo'], ['smart', 'fortwo_electric_drive'], ['studebaker', '440'], ['studebaker', 'avanti'], ['studebaker', 'challenger'], ['studebaker', 'champion'], ['studebaker', 'commander'], ['studebaker', 'daytona'], ['studebaker', 'dictator'], ['studebaker', 'golden_hawk'], ['studebaker', 'gran_turismo_hawk'], ['studebaker', 'land_cruiser'], ['studebaker', 'lark'], ['studebaker', 'model_a'], ['studebaker', 'model_b'], ['studebaker', 'model_h'], ['studebaker', 'pickup_truck'], ['studebaker', 'president'], ['studebaker', 'regal'], ['sunbeam', 'alpine'], ['sunbeam', 'tiger'], ['suzuki', 'aerio'], ['suzuki', 'equator'], ['suzuki', 'forenza'], ['suzuki', 'grand_vitara'], ['suzuki', 'kizashi'], ['suzuki', 'reno'], ['suzuki', 'sx4'], ['suzuki', 'samurai'], ['suzuki', 'sidekick'], ['suzuki', 'vitara'], ['suzuki', 'xl7'], ['triumph', '1200'], ['triumph', '2000'], ['triumph', 'gt6'], ['triumph', 'spitfire'], ['triumph', 'tr250'], ['triumph', 'tr3'], ['triumph', 'tr4'], ['triumph', 'tr6'], ['triumph', 'tr7'], ['triumph', 'tr8'], ['willys', 'cj_5'], ['willys', 'jeepster'], ['willys', 'maverick'], ['willys', 'pickup_truck']]


def getMakes():
    page = requests.get('https://www.cars.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    makesPathList = soup.find_all('select', class_='sds-text-field')
    for i in makesPathList:
        if i.get('id') == 'makes':
            makesPath = i
    makesPath2 = makesPath.find_all('option')
    makesList = []
    for i in makesPath2:
        if 'All makes' not in i:
            makesList.append(i.get('value').replace(' ', '_'))
    print(makesList)
    return makesList

def getModels():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.cars.com/'
    browser.get(url)
    
    browser.find_element(By.XPATH, '/html/body/section/div[2]/div[1]/section[2]/div[1]/div/div/form[1]/div/div/div[1]/div/select/option[4]').click()
        
    makesList = getMakes()
    modelsList = []
    counter = 1
    group = 1
    for n in makesList:
        if n == 'ac':
            counter = 1
            group = 2
        print('group = '+str(group)+'counter = '+str(counter))
        try:
            makesSelect = browser.find_element(By.XPATH, '/html/body/section/div[2]/div[1]/section[2]/div[1]/div/div/form[1]/div/div/div[2]/div/select/optgroup['+str(group)+']/option['+str(counter)+']').click()
        except:
            print('Not Found: '+'group = '+str(group)+'counter = '+str(counter))
        # makesInput = Select(makesSelect)
        # makesInput.select_by_visible_text(n)
        time.sleep(4)
        counter+=1
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        modelsPathList = soup.find_all('select', class_='sds-text-field')
        for i in modelsPathList:
            if i.get('id') == 'models':
                modelsPath = i
        modelsPath2 = modelsPath.find_all('option')
        for i in modelsPath2:
            if 'All models' not in i:
                modelVal = i.get('value').split('-')
                modelsList.append([n,modelVal[1]])
        # except:
        #     print(n+' not found')
    
    print(modelsList) 
    return modelsList
    
def massScrape1():
    modelsList = models
    makesList = makes
    errorList = []
    for i in makesList:
        try:
            scrapedData = Scrape1(i)
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape1 Error: '+i)
    print(errorList)

def massScrape2():
    modelsList = models
    makesList = makes
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape2(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape2 Error: '+i[0]+'-'+i[1])
    print(errorList)
            
def massScrape3():
    modelsList = models
    makesList = makes
    errorList = []
    for i in makesList:
        try:
            scrapedData = Scrape3(i)
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape3 Error: '+i)            
    print(errorList)    
    
def massScrape4():
    modelsList = models
    makesList = makes
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape4(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape4 Error: '+i[0]+'-'+i[1])
    print(errorList)
    
def massScrape5():
    modelsList = models
    makesList = makes
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape5(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape5 Error: '+i[0]+'-'+i[1])
    print(errorList)
              
massScrape2()

