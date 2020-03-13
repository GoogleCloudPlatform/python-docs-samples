# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
# flake8: noqa
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_filter_limit_row_regex 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_cells_per_col 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_cells_per_row 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_cells_per_row_offset 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_col_family_regex 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_col_qualifier_regex 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_col_range 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_value_range 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_value_regex 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_limit_timestamp_range 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00

'''

snapshots['test_filter_limit_block_all 1'] = ''

snapshots['test_filter_limit_pass_all 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_modify_strip_value 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb:  @2019-05-01 00:00:00+00:00
\tdata_plan_01gb:  @2019-04-30 23:00:00+00:00
\tdata_plan_05gb:  @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell:  @2019-05-01 00:00:00+00:00
\tconnected_wifi:  @2019-05-01 00:00:00+00:00
\tos_build:  @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb:  @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell:  @2019-05-01 00:00:00+00:00
\tconnected_wifi:  @2019-05-01 00:00:00+00:00
\tos_build:  @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb:  @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell:  @2019-05-01 00:00:00+00:00
\tconnected_wifi:  @2019-05-01 00:00:00+00:00
\tos_build:  @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb:  @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell:  @2019-05-01 00:00:00+00:00
\tconnected_wifi:  @2019-05-01 00:00:00+00:00
\tos_build:  @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb:  @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tconnected_cell:  @2019-05-01 00:00:00+00:00
\tconnected_wifi:  @2019-05-01 00:00:00+00:00
\tos_build:  @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_modify_apply_label 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00 [labelled]
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00 [labelled]
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [labelled]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00 [labelled]

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [labelled]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00 [labelled]

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [labelled]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00 [labelled]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00 [labelled]

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00 [labelled]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00 [labelled]

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00 [labelled]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [labelled]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00 [labelled]
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00 [labelled]

'''

snapshots['test_filter_composing_chain 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_composing_interleave 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_filter_composing_condition 1'] = '''Reading data for phone#4c410523#20190501:
Column Family cell_plan
\tdata_plan_01gb: false @2019-05-01 00:00:00+00:00 [filtered-out]
\tdata_plan_01gb: true @2019-04-30 23:00:00+00:00 [filtered-out]
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [filtered-out]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [filtered-out]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [filtered-out]
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00 [filtered-out]

Reading data for phone#4c410523#20190502:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [filtered-out]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [filtered-out]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [filtered-out]
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00 [filtered-out]

Reading data for phone#4c410523#20190505:
Column Family cell_plan
\tdata_plan_05gb: true @2019-05-01 00:00:00+00:00 [filtered-out]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00 [filtered-out]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [filtered-out]
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00 [filtered-out]

Reading data for phone#5c10102#20190501:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00 [passed-filter]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [passed-filter]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [passed-filter]
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00 [passed-filter]

Reading data for phone#5c10102#20190502:
Column Family cell_plan
\tdata_plan_10gb: true @2019-05-01 00:00:00+00:00 [passed-filter]
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00 [passed-filter]
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00 [passed-filter]
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00 [passed-filter]

'''
