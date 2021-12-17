# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:16:43 2021

@author: mikhail
"""

import sys
import plotly.io as pio
import json
from handle_request import handle_request

sys.path.insert(1, '../en-lst-solver')

def main(response):
    fig_json_ai = response["figures"][0]
    fig_dict_ai = json.loads(fig_json_ai)
    pio.kaleido.write_image(fig_dict_ai, '../out/Unstable modes.jpg')
    
    fig_json_ac = response["figures"][1]
    fig_dict_ac = json.loads(fig_json_ac)
    pio.kaleido.write_image(fig_dict_ac, '../out/Amplification_curves.jpg')
    
    
    # #plot amplification curves
    # for i in range(number_of_omegas):
    #     plt.plot(x_mesh, amplification_curves[i])
    
    # plt.plot(0.784, 7.82, 'ro', label = 'Tu= 0,12 %')
    # plt.plot(1.25, 10.7, 'ro')
    # plt.plot(0.597, 6.45, 'bo',  label = 'Tu= 0,2 %')
    # plt.plot(1.02, 9.32, 'bo')
    # plt.ylim(0, 18)
    # plt.legend()
    # name = 'Расчет положений ЛТП'
    # plt.title(name)
    # plt.savefig('../out/Amplification_curves.jpg')

if __name__ == "__main__":
    #params = dict(omega_min=1000, omega_max=7000, number_of_omegas=8)
    params = dict(omega_min=1000, omega_max=2000, number_of_omegas=2)
    request = dict(problem="ACS", args=params)
    response = handle_request(request)
    main(response)
    
    
    
    
    
    
    