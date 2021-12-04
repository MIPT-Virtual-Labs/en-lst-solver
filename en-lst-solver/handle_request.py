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
        
    if problem_name == 'ACS':
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
    return response_dict