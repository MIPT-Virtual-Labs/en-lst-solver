# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:31:24 2021

@author: mikhail
"""

import sys
import plotly.io as pio
import json
from handle_request import handle_request

sys.path.insert(1, '../en-lst-solver')

def main(response):
    fig_json = response["figures"][0]
    fig_dict = json.loads(fig_json)
    pio.kaleido.write_image(fig_dict, '../out/Spatial spectrum.jpg')

if __name__ == "__main__":
    params = dict(N=800)
    request = dict(problem='SS', args=params)
    response = handle_request(request)
    main(response)