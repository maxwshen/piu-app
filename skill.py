'''
  Handle skill pages
'''
from collections import defaultdict
from os import altsep
import pandas as pd
import app, lib

'''
  Parameters
'''
MIN_FREQUENCY = 0.01
TOP_N_PER_LEVEL = 15


'''
  Functions
'''
def add_sordlevel_col(df):
  # todo - move this somewhere else?
  get_sord = lambda ss: 'S' if 'S' in ss else 'D'
  df.loc[:, 'sord'] = [get_sord(ss) for ss in df['Steptype simple']]
  df.loc[:, 'sordlevel'] = df['sord'] + df['Level'].astype(str)
  return df


def get_top_charts_by_skill(df, skill, 
      n = TOP_N_PER_LEVEL, min_fq = MIN_FREQUENCY):
  # df = feature_df_notbeginner
  col = SKILL_NAME_TO_COL[skill]
  res_df = pd.DataFrame()
  subcols = {
    'Name (unique)': 'Stepchart',
    'Level': 'Level',
    'sord': 'sord',
    'Pack': 'Pack',
    col: 'Score',
  }
  internal_cols = list(subcols.keys())
  display_cols = list(subcols.values())
  
  for _, dfs in df.groupby('sordlevel'):
    top_dfs = dfs.sort_values(by=col, ascending=False).iloc[:n]
    if skill in NO_FQ_FILTER_SKILLS:
      top_dfs = top_dfs[top_dfs[col] > 0]
    else:
      top_dfs = top_dfs[top_dfs[col] >= min_fq]

    res_df = res_df.append(top_dfs[internal_cols])

  singles_df = res_df[res_df['sord'] == 'S'].drop(columns=['sord'])
  doubles_df = res_df[res_df['sord'] == 'D'].drop(columns=['sord'])
  return display_cols, singles_df, doubles_df


'''
  Primary
'''
def get_skill_text(skill):
  '''
    Build plain-text and links:
      S16: <chart1>, <chart2>, ...
    Avoid table: Too much user interaction

    all_text['singles' / 'doubles'] = <br>-separated list of charts
  '''
  res = get_top_charts_by_skill(feature_df_notbeginner, skill)
  display_cols, singles_df, doubles_df = res
  all_text = defaultdict(list)
  cats = ['singles', 'doubles']
  for cat, df in zip(cats, [singles_df, doubles_df]):
    sord = 'S' if cat == 'singles' else 'D'
    for _, lvl_df in df.groupby('Level'):
      charts = list(lvl_df['Name (unique)'])
      chart_strs = lib.chart_list_plain(charts)

      level = lvl_df['Level'].iloc[0]
      lvl_str = f'{sord}{level}: ' + ', '.join(chart_strs)
      all_text[cat].append(lvl_str)

  for cat in cats:
    if cat not in all_text:
      all_text[cat] = 'None'
    else:
      all_text[cat] = '<br>'.join(all_text[cat])
  return all_text


def get_skill_main_page():
  # List skills
  strs = []
  for skill in SKILL_NAMES:
    url = lib.get_url('skill', skill)
    string = f'<a href="{url}">{skill}</a>'
    strs.append(string)
  return '<br>'.join(strs)


'''
  Global vars
'''
feature_df = app.feature_df
feature_df = add_sordlevel_col(feature_df)

feature_df['Twist angle - any - frequency'] = 1 - feature_df['Twist angle - none - frequency']

LOWER_LVL = 7
UPPER_LVL = 24
feature_df_notbeginner = feature_df[(feature_df['Level'] >= LOWER_LVL) &
                                    (feature_df['Level'] <= UPPER_LVL)]

SKILL_COLS_TO_NAME = {
  'Run - frequency': 'Run',
  'Drill - frequency': 'Drill',
  'Twist angle - none - frequency': 'No twists',
  'Twist angle - 90 - frequency': '90 twist',
  'Twist angle - close diagonal - frequency': 'Close diagonal twist',
  'Twist angle - far diagonal - frequency': 'Far diagonal twist',
  'Twist solo diagonal - frequency': 'Solo diagonal twist',
  'Twist angle - 180 - frequency': '180 twist',
  'Twist angle - any - frequency': 'Twist',
  'Travel (mm) - 80%': 'Travel',
  'Rhythm change - frequency': 'Irregular rhythm',
  'Jump - frequency': 'Jump',
  'Hold taps - frequency': 'Hold tap',
  'Double step - frequency': 'Double step',
  'Jack - frequency': 'Jack',
  'Footswitch - frequency': 'Footswitch',
  'Bracket - frequency': 'Bracket',
  'Triple - frequency': 'Triple',
  'Quad - frequency': 'Quad',
  'Bracket jump run - frequency': 'Bracket jump run',
  'Hold tap single foot - frequency': 'Bracket hold tap',
  'Bracket footswitch - frequency': 'Bracket footswitch',
  'Bracket drill - frequency': 'Bracket drill',
  'Staggered hit - frequency': 'Rolling hit',
  'Hold footslide - frequency': 'Hold footslide',
  'Hold footswitch - frequency': 'Hold footswitch',
  'Side3 singles - frequency': 'Side3 singles',
  'Mid4 doubles - frequency': 'Mid4 doubles',
  'Mid6 doubles - frequency': 'Mid6 doubles',
  'Stairs, singles - frequency': '5-panel stair',
  'Stairs, doubles - frequency': '10-panel stair',
  'Broken stairs, doubles - frequency': '9-panel stair',
  'Spin - frequency': 'Spin',
  'Splits - frequency': 'Splits',
  'Hands - frequency': 'Hands',
}
SKILL_COLS = list(SKILL_COLS_TO_NAME.keys())
SKILL_NAMES = list(SKILL_COLS_TO_NAME.values())
SKILL_NAME_TO_COL = {nm: col for nm, col in zip(SKILL_NAMES, SKILL_COLS)}

NO_FQ_FILTER_SKILLS = [
  'Splits',
  'Hands',
  'Bracket',
  'Triple',
  'Quad',
  '5-panel stair',
  '10-panel stair',
  '9-panel stair',
  'Bracket jump run',
  'Bracket hold tap',
  'Bracket footswitch',
  'Bracket drill',
  'Hold footslide',
  'Hold footswitch',
  'Spin',
  '180 twist',
  'Solo diagonal twist',
]

'''
  Run
'''
def test():
  display_cols, singles_df, doubles_df = get_top_charts_by_skill(feature_df_notbeginner, 'Twists')
  print(display_cols)
  print(singles_df)
  print(doubles_df)
  return


if __name__ == '__main__':
  test()
