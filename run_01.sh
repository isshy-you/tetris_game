#!/bin/csh -f
./start_01.sh -l 1 > log/start_01_lv1.log ; mv result/result_ish01.json result/result_ish01_lv1.json
./start_01.sh -l 2 > log/start_01_lv2_1.log ; mv result/result_ish01.json result/result_ish01_lv2_1.json
./start_01.sh -l 2 > log/start_01_lv2_2.log ; mv result/result_ish01.json result/result_ish01_lv2_2.json
./start_01.sh -l 2 > log/start_01_lv2_3.log ; mv result/result_ish01.json result/result_ish01_lv2_3.json
./start_01.sh -l 3 > log/start_01_lv3_1.log ; mv result/result_ish01.json result/result_ish01_lv3_1.json
./start_01.sh -l 3 > log/start_01_lv3_2.log ; mv result/result_ish01.json result/result_ish01_lv3_2.json
./start_01.sh -l 3 > log/start_01_lv3_3.log ; mv result/result_ish01.json result/result_ish01_lv3_3.json
