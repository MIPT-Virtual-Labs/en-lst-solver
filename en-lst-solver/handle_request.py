# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 14:03:39 2021

@author: Mikhail
"""

from typing import List, Optional

from pydantic import BaseModel, ValidationError, validator

from temporal_functions import temporal_solve, TS_InputParameters
from spatial_functions import spatial_solve, SS_InputParameters
from amplification_curves_functions import amplfication_curves_solve, ACS_InputParameters

import pandas as pd
import plotly.express as px
import numpy as np

class Error(BaseModel):
    error: str
    field: str


class Response(BaseModel):
    errors: Optional[List[Error]]
    description: Optional[str]
    solution: Optional[dict]
    status: str

    @validator("status")
    def validate_status(cls, st, values):
        if st == "error":
            if "errors" not in values:
                raise ValueError("status is set to `error` but no errors provided")
        else:
            if "errors" in values and values["errors"]:
                raise ValueError(f"status is not {st} but errors were found")
        if st == "failed" and "description" not in values:
            raise ValueError("status is set to `failed` but no description provided")
        return st


def handle_request(request_json: dict) -> dict:

    problem_name = request_json["problem"]

    if problem_name not in ['TS', 'SS', 'ACS']:

        errors = [Error(error=f"Unknown problem: `{problem_name}`", field="problem")]
        response = Response(status="error", errors=errors)
        return response.dict()

    args = request_json["args"]

    if problem_name == 'TS':
        try:
            p = TS_InputParameters(**args)
        except ValidationError as ve:
            errors = [Error(error=e["msg"], field=e["loc"][0]) for e in ve.errors()]
            response = Response(status="error", errors=errors)
            return response.dict()
    
        try:
            solution = temporal_solve(p)
        except Exception as e:
            response = Response(status="failed", description=str(e))
            return response.dict()
      
    if problem_name == 'SS':
        try:
            p = SS_InputParameters(**args)
        except ValidationError as ve:
            errors = [Error(error=e["msg"], field=e["loc"][0]) for e in ve.errors()]
            response = Response(status="error", errors=errors)
            return response.dict()
    
        try:
            solution = spatial_solve(p)
        except Exception as e:
            response = Response(status="failed", description=str(e))
            return response.dict()
        
    if problem_name == "ACS":
        try:
            p = ACS_InputParameters(**args)
        except ValidationError as ve:
            errors = [Error(error=e["msg"], field=e["loc"][0]) for e in ve.errors()]
            response = Response(status="error", errors=errors)
            return response.dict()
    
        try:
            solution = amplfication_curves_solve(p)
        except Exception as e:
            response = Response(status="failed", description=str(e))
            return response.dict()

    response = Response(status="done", solution=solution)
    response_dict = response.dict()
    
    if problem_name == 'TS':
        eigvals = response_dict['solution']['data']
        df = pd.DataFrame({"c_re": eigvals.real, "c_im": eigvals.imag})
        df['data'] = 'Numerical'
        fig = px.scatter(df, x="c_re", y="c_im", color='data')
        fig.update_layout(xaxis_range=[0, 1], yaxis_range=[-1, 0.1])
        fig_json = fig.to_json()
        response_figs = {"figures": [fig_json]}
        
    if problem_name == 'SS':
        eigvals = response_dict['solution']['data']
        df = pd.DataFrame({"a_re": eigvals.real, "a_im": eigvals.imag})
        df['data'] = 'Numerical'
        paper_data = np.array([[0.2600153645394847,0.005216576864792044],
                        [0.2649509597575349,0.04520717573104338],
                        [0.267293525846102,0.08786938036706515],
                        [0.2709547061794915,0.12519574002357303],
                        [0.2732972722680586,0.1678579446595948],
                        [0.27947781613066175,0.2158461721950946],
                        [0.28170988381882467,0.27850858730426],
                        [0.28521636639164843,0.3438352416231689],
                        [0.28491433743054384,0.3985024835830948],
                        [0.28456810910927766,0.46116980973227817],
                        [0.28552576191277995,0.5211679856317001],
                        [0.29872663748105743,0.23180950777347475],
                        [0.5419115170904193,0.08201296514564738],
                        [0.7428786411853847,0.3402968372902284],
                        [0.28653498063647076,0.5718327299769883]])
        paper_data /= 1.72
        df_paper = pd.DataFrame({"a_re": paper_data[:,0], "a_im": paper_data[:,1]})
        df_paper['data'] = 'Paper'
        df = pd.concat([df, df_paper], ignore_index=True)
        fig = px.scatter(df, x="a_re", y="a_im", color='data')
        fig.update_layout(xaxis_range=[0.1, 0.5], yaxis_range=[-0.1, 0.3])
        fig_json = fig.to_json()
        response_figs = {"figures": [fig_json]}
        
    if problem_name == "ACS":
        x_mesh = response_dict['solution']['x_mesh']
        ai_for_omega = response_dict['solution']['ai_for_omega']
        amplification_curves = response_dict['solution']['amplification_curves']
        omega_min = p.omega_min
        omega_max = p.omega_max
        number_of_omegas = p.number_of_omegas
        omega_mesh = np.linspace(omega_min, omega_max, number_of_omegas)
        df = pd.DataFrame({"x": x_mesh, "ai": ai_for_omega[0], "omega": str(omega_mesh[0])})
        for i in range(number_of_omegas):
            text = str(omega_mesh[i])
            df_next = pd.DataFrame({"x": x_mesh, "ai": ai_for_omega[i], "omega": text})
            df = pd.concat([df, df_next], ignore_index=True)  
        fig = px.scatter(df, x="x", y="ai", color='omega')
        fig_json_ai = fig.to_json()
        
        #plot amplification curves
        df = pd.DataFrame({"x": x_mesh, "N": amplification_curves[0], "omega": str(omega_mesh[0])})
        for i in range(number_of_omegas):
            text = str(omega_mesh[i])
            df_next = pd.DataFrame({"x": x_mesh, "N": amplification_curves[i], "omega": text})
            df = pd.concat([df, df_next], ignore_index=True) 
        fig = px.scatter(df, x="x", y="N", color='omega')
        fig_json_AC = fig.to_json()
        
        response_figs = {"figures": [fig_json_ai, fig_json_AC]}
        
        
    return response_figs










