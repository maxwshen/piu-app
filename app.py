import os, pickle, functools, string
import pandas as pd
from flask import Flask, redirect, render_template, json
import boto3
from markupsafe import escape
import urllib.parse

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

s3 = boto3.client('s3', 
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
                  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

S3_SAFE_CHARS = string.ascii_letters + string.digits + "!-_.*'()"
REPLACE_CHAR = '_'
def s3_safe(name):
  convert_safe = lambda char: char if char in S3_SAFE_CHARS else REPLACE_CHAR
  return ''.join(convert_safe(char) for char in name)


@functools.lru_cache(maxsize=None)
def fetch_csv(nm):
  # If not locally available, download from S3
  local_fn = f'data/{nm}.csv'
  if not os.path.isfile(local_fn):
    s3.download_file(os.environ['S3_BUCKET_NAME'], f'{nm}.csv', local_fn)
  df = pd.read_csv(local_fn, index_col=0)
  return df


@functools.lru_cache(maxsize=None)
def get_data(nm):
  local_fn = f'data/{nm}.pkl'
  if not os.path.isfile(local_fn):
    s3.download_file(os.environ['S3_BUCKET_NAME'], f'{s3_safe(nm)}.pkl', local_fn)
  with open(local_fn, 'rb') as f:
    data = pickle.load(f)
  return data


all_df = fetch_csv('charts_all')
import lib
local_cols, table_cols = lib.parse_table_data()

feature_df = fetch_csv('features')
import skill


'''
  Dynamically serve content - charts
'''
@app.route('/chart/<stepchart>')
def chart_page(stepchart):
  # if stepchart == 'mitotsudaira':
  #   stepchart = 'Mitotsudaira - ETIA. D19 arcade'
  # elif stepchart == 'superfantasy':
  #   stepchart = 'Super Fantasy - SHK S16 arcade'
  # elif stepchart == 'kos':
  #   stepchart = 'King of Sales - Norazo S21 arcade'
  stepchart = urllib.parse.unquote_plus(stepchart)

  # Check if nm in database, otherwise return 'not found' page

  data = get_data(stepchart)
  info_dict = {k: v for k, v in zip(data[0][0], data[0][1])}
  info_dict = lib.update_info_dict(info_dict)

  # Render HTML template using parsed files
  return render_template('chart.html.jinja', 
      info=info_dict, 
      data=data,
      lib=lib,
  )


@app.route('/skill/<skill_name>')
def skill_page(skill_name):
  skill_name = urllib.parse.unquote_plus(skill_name)
  chart_lists = skill.get_skill_text(skill_name)
  return render_template('skill.html.jinja',
      skill_name=skill_name,
      singles_charts_str=chart_lists['singles'],
      doubles_charts_str=chart_lists['doubles'],
  )


@app.route('/chart')
def main_chart_page():
  return render_template('home_chart.html.jinja',
      local_cols=local_cols, 
      table_cols=table_cols,
      get_url=lambda chart: lib.get_url('chart', chart),
  )


@app.route('/skill')
def main_skill_page():
  skill_list = skill.get_skill_main_page()
  return render_template('home_skill.html.jinja', skill_list=skill_list)


@app.route('/')
def home():
  return render_template('home.html.jinja',
      local_cols=local_cols, 
      table_cols=table_cols,
      get_url=lambda chart: lib.get_url('chart', chart),
  )

