# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:16:52 2021

@author: mikhail
"""
import sys
sys.path.insert(1, '../en-lst-solver')

import plotly.io as pio
import json
from handle_request import handle_request

def main(response):
    fig_json = response["figures"][0]
    fig_dict = json.loads(fig_json)
    pio.kaleido.write_image(fig_dict, '../out/Temporal spectrum.jpg')

if __name__ == "__main__":
    params = dict(alpha=1, Re=10000)
    request = dict(problem="TS", args=params)
    response = handle_request(request)
    main(response)
    
    
    
    
    
    
    
    
    
    