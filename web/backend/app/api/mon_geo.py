from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
import random

router = APIRouter()
@router.get("/top_categories", response_description="Offline sources")
async def top_categories(request: Request):
    date = datetime.datetime.utcnow()
    data = [
    {
      'id': 1,
      'title': 'USA',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'United States',
      'delta': '0',
    },
    {
      'id': 2,
      'title': 'BRA',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Brazil',
      'delta': '0',
    },
    {
      'id': 3,
      'title': 'DEU',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Germany',
      'delta': '0',
    },
    {
      'id': 4,
      'title': 'ISR',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Israel',
      'delta': '0',
    },
    {
      'id': 5,
      'title': 'AUS',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Australia',
      'delta': '0',
    },
    {
      'id': 6,
      'title': 'FRA',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'France',
      'delta': '0',
    },
    {
      'id': 7,
      'title': 'PAK',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Pakistan',
      'delta': '0',
    },
    {
      'id': 8,
      'title': 'HND',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Honduras',
      'delta': '0',
    },
    {
      'id': 9,
      'title': 'GAB',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Gabon',
      'delta': '0',
    },
    {
      'id': 10,
      'title': 'JAM',
      'count': 0,
      'norm_count': 0,
      'subtitle': 'Jamaica',
      'delta': '0',
    }
    ]
    return data

@router.get("/map_data", response_description="Geo coordinates for map")
async def map_data(request: Request):
  data = [
    {
      'city_code': 'USA',
      'population': 50,
      'lnt': 40.7170,
      'lat': -84.0037,
    },
    {
      'city_code': 'BRA',
      'population': 45,
      'lnt': 55.7170,
      'lat': -116.0037,
    },
    {
      'city_code': 'DEU',
      'population': 40,
      'lnt': 50.8534,
      'lat': 14.3488,
    },
    {
      'city_code': 'ISR',
      'population': 35,
      'lnt': 41.0138,
      'lat': 28.9497,
    },
    {
      'city_code': 'AUS',
      'population': 30,
      'lnt': 39.9075,
      'lat': 116.3972,
    },
    {
      'city_code': 'FRA',
      'population': 25,
      'lnt': 48.8534,
      'lat': 2.3488,
    },
    {
      'city_code': 'PAK',
      'population': 20,
      'lnt': 31.5497,
      'lat': 74.3436,
    },
    {
      'city_code': 'HND',
      'population': 15,
      'lnt': -34.6051,
      'lat': -58.4004,
    },
    {
      'city_code': 'GAB',
      'population': 10,
      'lnt': 6.4531,
      'lat': 13.3958,
    },
    {
      'city_code': 'JAM',
      'population': 5,
      'lnt': -10.6051,
      'lat': -68.4004,
    }
  ]
  return data

@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
  name = 'Incidents'
  labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
  label = '+0'
  data = [0, 0, 0, 0, 0, 0, 0]
  response_data = {
    'name': name,
    'labels': labels,
    'label': label,
    'data': data,
  }
  return response_data

@router.get("/polar", response_description="Polar chart max Errors")
async def polar(request: Request):
  labels = ['United States', 'Canada', 'Germany', 'Israel', 'Australia']
  data = [0, 0, 0, 0, 0]
  response_data = {
    'labels': labels,
    'data': data,
  }
  return response_data