# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:16:43 2021

@author: mikhail
"""



import sys
sys.path.insert(1, '../en-lst-solver')

import plotly.io as pio
import json
from handle_request import handle_request

def main(response):
    fig_json_ai = response["figures"][0]
    fig_dict_ai = json.loads(fig_json_ai)
    pio.kaleido.write_image(fig_dict_ai, '../out/Unstable modes.jpg')
    
    fig_json_ac = response["figures"][1]
    fig_dict_ac = json.loads(fig_json_ac)
    pio.kaleido.write_image(fig_dict_ac, '../out/Amplification_curves.jpg')

if __name__ == "__main__":
    #params = dict(omega_min=1000, omega_max=7000, number_of_omegas=8)
    params = dict(omega_min=1000, omega_max=2000, number_of_omegas=2)
    request = dict(problem="ACS", args=params)
    response = handle_request(request)
    main(response)
    
    
    
    
    
    
    