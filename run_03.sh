#!/bin/csh -f
./start_03.sh -l 1 > log/start_03_lv1.log ; mv result/result_ish03.json result/result_ish03_lv1.json
./start_03.sh -l 2 > log/start_03_lv2_1.log ; mv result/result_ish03.json result/result_ish03_lv2_1.json
./start_03.sh -l 2 > log/start_03_lv2_2.log ; mv result/result_ish03.json result/result_ish03_lv2_2.json
./start_03.sh -l 2 > log/start_03_lv2_3.log ; mv result/result_ish03.json result/result_ish03_lv2_3.json
./start_03.sh -l 3 > log/start_03_lv3_1.log ; mv result/result_ish03.json result/result_ish03_lv3_1.json
./start_03.sh -l 3 > log/start_03_lv3_2.log ; mv result/result_ish03.json result/result_ish03_lv3_2.json
./start_03.sh -l 3 > log/start_03_lv3_3.log ; mv result/result_ish03.json result/result_ish03_lv3_3.json
