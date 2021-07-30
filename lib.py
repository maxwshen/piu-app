from urllib.parse import quote_plus

import app

all_df = app.fetch_files('charts_all')
NAME = list(all_df['Name (unique)'])
NAME_TO_IDX = {nm: idx for idx, nm in enumerate(NAME)}
LEVEL = [str(s) for s in all_df['METER']]
SORD = list(all_df['Steptype simple'])
TITLE = list(all_df['TITLE'])
STEPTYPE = list(all_df['SONGTYPE'])
PACK = list(all_df['Pack'])

'''
  Strings
'''
def get_url(branch, string):
  # todo: only supports 1-depth folder structure, update
  return '../' + branch + '/' + quote_plus(f'{string}', safe='')


def abbreviate_chart(chart):
  idx = NAME_TO_IDX[chart]
  charttype = STEPTYPE[idx].lower()
  title = TITLE[idx]
  filts = [' - FULL SONG -', ' - SHORT CUT -']
  for filt in filts:
    title = title.replace(filt, '')
  if charttype == 'arcade':
    return ' '.join([title, SORD[idx] + LEVEL[idx]])
  else:
    return ' '.join([title, SORD[idx] + LEVEL[idx], charttype])


'''
  Dynamic content for chart page
'''
def update_info_dict(info_dict):
  parse_difficulty_percentile(info_dict)
  parse_similar_charts(info_dict)

  return info_dict


def parse_difficulty_percentile(info_dict):
  pct = float(info_dict['predicted difficulty percentile'])
  ranges = {
    (0, 0.10): ('Easy', '#7cb82f'),
    (0.10, 0.25): ('Easy-medium', '#efb920'),
    (0.25, 0.75): ('Medium', '#f47b16'),
    (0.75, 0.925): ('Hard', '#ec4339'),
    (0.925, 1.0): ('Very hard', '#c11f1d'),
  }
  string, color = [pkg for r, pkg in ranges.items() if r[0] <= pct <= r[1]][0]
  info_dict['difficulty string'] = string
  info_dict['difficulty string color'] = color
  return


def parse_similar_charts(info_dict):
  # abbreviate step charts, make urls, form string
  lvl_strs = []
  for level, charts in info_dict['similar charts'].items():
    chart_strs = []
    for chart in charts:
      abbrev_chart = abbreviate_chart(chart)
      url = get_url('chart', chart)
      chart_str = f'<a href="{url}">{abbrev_chart}</a>'
      chart_strs.append(chart_str)
    lvl_str = f'{level}: ' + ', '.join(chart_strs)
    lvl_strs.append(lvl_str)
  info_dict['parsed similar charts'] = '<br>'.join(lvl_strs)
  return 


'''
  Stepchart abbreviation
'''
