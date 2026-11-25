# Raw file manifest (Florida audit)

Download time = file write time on the box, America/Chicago (CST, UTC-6).

| File | Source URL | Downloaded (CST) | Bytes | SHA-256 | Notes |
|---|---|---|---|---|---|
| raw/20261103_ElecResultsFL.txt | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.txt?v=52821560 | 2026-11-20T19:15:38-06:00 | 365374 | `6da5bdddd2f6dbd0…` | 2026 General results, all races, county, tab-delimited (linked from floridaelectionwatch.gov/Downloads). Pass 1 source for 2026 governor votes. Fetched with curl -k: server sends GoDaddy R1 root not in box CA bundle (chain inspected: *.floridados.gov <- GoDaddy TLS Intermediate CA DV - R1v1 <- GoDaddy TLS Root CA - R1). |
| raw/20261103_ElecResultsFL.xls | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.xls?v=52821560 | 2026-11-20T19:15:38-06:00 | 365374 | `6da5bdddd2f6dbd0…` | Byte-identical to the .txt (same md5); kept for completeness, not used. |
| raw/20261103_ElecResultsFL_PipeDlm_Info.txt | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Info.txt?v=52821560 | 2026-11-20T19:15:39-06:00 | 68873 | `7311ccd89e95411b…` | Pipe-delimited info file (races, candidates, units). Pass 2 source (with Votes file). curl -k as above. |
| raw/20261103_ElecResultsFL_PipeDlm_Votes.txt | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Votes.txt?v=52821560 | 2026-11-20T19:15:35-06:00 | 141307 | `a8a8365475a472ff…` | Pipe-delimited votes file. Pass 2 source for 2026 governor votes. All 670 governor records carry status "I" (Incomplete). curl -k as above. |
| raw/ResultsFileLayoutPipeDelimited.pdf | https://flelectionfiles.floridados.gov/enightfilespublic/ResultsFileLayoutPipeDelimited.pdf?v=52821560 | 2026-11-20T19:16:06-06:00 | 249019 | `1d9359422347c65d…` | Layout spec for the pipe files. |
| raw/bookclosing_2022gen_1_party_by_county.pdf | https://files.floridados.gov/media/706001/1-by-party-by-county.pdf | 2026-11-20T19:15:34-06:00 | 100438 | `a2a1e25a4cce642d…` | 2022 General book closing (Oct 11, 2022) active registered voters by party by county. Pass 1 source for 2022 registration. No Excel version located for 2022 (media ids 706000-706010 probed). |
| raw/bookclosing_2022gen_3_party_by_county_by_race.pdf | https://files.floridados.gov/media/706005/3-by-party-by-county-by-race.pdf | 2026-11-20T19:15:52-06:00 | 238035 | `37fd26098fcca884…` | 2022 General book closing by party by race. Pass 2 source for 2022 registration (Dem section total; county total = sum of all party sections). |
| raw/bookclosing_2026gen_1_party_by_county.pdf | https://dos.fl.gov/media/711452/1-party-by-county.pdf | 2026-11-20T19:16:00-06:00 | 183595 | `00e87ffee4e26e08…` | Same report as PDF. Pass 2 source for 2026 registration. |
| raw/bookclosing_2026gen_1_party_by_county.xlsx | https://dos.fl.gov/media/711453/1-party-by-county.xlsx | 2026-11-20T19:16:04-06:00 | 40874 | `4784f9f82e2074db…` | 2026 General book closing (Oct 5, 2026) by party by county. Pass 1 source for 2026 registration. |
| raw/bookclosing_2026gen_3_party_by_county_by_race.xlsx | https://dos.fl.gov/media/711457/3-party-by-county-by-race.xlsx | 2026-11-20T19:15:51-06:00 | 100472 | `336fc66c2bcf282d…` | 2026 by party by race (supplementary cross-check). |
| raw/dos_bookclosing_page.html | https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/bookclosing/ | 2026-11-20T19:16:09-06:00 | 55017 | `d9270fcdbc0bd700…` | Book closing index page (2026 only; 2022 files located via files.floridados.gov). |
| raw/dos_voter_turnout_page.html | https://dos.fl.gov/elections/data-statistics/elections-data/voter-turnout/ | 2026-11-20T19:16:03-06:00 | 32259 | `440dec73d5974730…` | Statewide historical turnout page. |
| raw/few_CountyReportingStatus.html | https://floridaelectionwatch.gov/CountyReportingStatus | 2026-11-20T19:15:51-06:00 | 169710 | `35413739f9ee1b6b…` | 2026 County Reporting Status: Voter Turnout (ballots cast), Eligible Active Registered Voters, completion flags. 2026 ballots cast source (both passes, different parsers). |
| raw/few_Downloads.html | https://floridaelectionwatch.gov/Downloads | 2026-11-20T19:15:52-06:00 | 24007 | `374e7172658a4b1d…` | Downloads page linking the 2026 results files. |
| raw/few_ElectionDayTurnout.html | https://floridaelectionwatch.gov/ElectionDayTurnout | 2026-11-20T19:16:15-06:00 | 86002 | `9d9b4cacb18ea23c…` | Election-day-only turnout, election night (not used for metrics). |
| raw/few_Timeline.html | https://floridaelectionwatch.gov/Timeline | 2026-11-20T19:16:00-06:00 | 26459 | `0085a24aa3b83232…` | Certification timeline (official returns due Nov 16; Canvassing Commission Nov 17, 2026). |
| raw/few_gov_by_county_2026.html | https://floridaelectionwatch.gov/ContestResultsByCounty/160000 | 2026-11-20T19:15:37-06:00 | 85508 | `ae7093ec9d26581e…` | 2026 Governor results by county (HTML), page header "Official Election Results". Cross-source check for 2026 governor votes; Total row. |
| raw/few_governor_statewide_2026.html | https://floridaelectionwatch.gov/StateOffices/Governor | 2026-11-20T19:15:37-06:00 | 35414 | `69364ba761dc0892…` | 2026 Governor statewide totals (DOE-reported state total). |
| raw/few_home.html | https://floridaelectionwatch.gov/ | 2026-11-20T19:16:18-06:00 | 23925 | `996641edbd14d5db…` | Election Watch home; header "2026 General Election November 3, 2026 Official Election Results". |
| raw/few_trackcounty_ALA.html | https://floridaelectionwatch.gov/TrackCounty/ALA | 2026-11-20T19:15:37-06:00 | 125744 | `6c25d2d43d07e4c2…` | Alachua track page (contest ids). |
| raw/fl_gov_detail_20221108.html | https://results.elections.myflorida.com/DetailRpt.Asp?ELECTIONDATE=11/8/2022&RACE=GOV&PARTY=&DIST=&GRP=&DATAMODE= | 2026-11-20T19:16:20-06:00 | 20465 | `d135b0fe8c7ce367…` | 2022 Governor county detail report, "Official Results". Pass 2 source for 2022 governor votes; Total row = DOE statewide totals. |
| raw/fl_results_20221108_extract.txt | POST https://results.elections.myflorida.com/ResultsExtract.Asp (ElectionDate=11/8/2022, OfficialResults=Y, PartyRaces=N) | 2026-11-20T19:15:52-06:00 | 404954 | `38dc8a11148b4ac6…` | 2022 General, all races, county level, tab-delimited, OFFICIAL. Pass 1 source for 2022 governor votes. |
| raw/fl_turnout_20221108.html | https://results.elections.myflorida.com/TurnoutRpt.asp?ElectionDate=11/8/2022&DATAMODE= | 2026-11-20T19:15:35-06:00 | 18629 | `a7bfb88c5e6c3f2b…` | 2022 General "Voter Registration and Turnout" by county, Official Results. Turnout = ballots cast (both passes, different parsers). |
| raw/home_results.html | https://results.elections.myflorida.com/ | 2026-11-20T19:15:29-06:00 | 2043 | `d99f120d3eb0e507…` | Results archive home (frameset). Election list (ElectionRaces.asp) shows no 2026 General entry; 11/3/2026 extract returned header only. |
| raw/results_11-8-2022.txt | https://results.elections.myflorida.com/downloadresults.asp?ElectionDate=11/8/2022&DATAMODE= | 2026-11-20T19:16:13-06:00 | 9226 | `85f1c41bc59705eb…` | Extract utility form page (HTML) showing field layout; not data. |
| raw/vr_archive_2022.zip | https://dos.fl.gov/media/709149/2022-archived.zip | 2026-11-20T19:16:02-06:00 | 305801 | `411d00366375bd77…` | 2022 monthly registration archive (not book closing; not used for metrics). |

## Resources graphics (added Nov 22, 2026; *2026 unofficial labels refreshed Nov 24, 2026)

| File | SHA-256 |
|---|---|
| graphics/flip/FL_Flip_01_Liberty.png | `253ec9a3def380a13dd70e8e0a8efe288515a8cc4e2eabccad237ead1975e4b1` |
| graphics/flip/FL_Flip_02_Hendry.png | `98ef4b7c6da11881f4095873121611f645118a28bc401f92987490c094f68eb8` |
| graphics/flip/FL_Flip_03_Calhoun.png | `5efe8bd31617d6c60c6215d4231c87d2c2d53d637981d19d6bc3975dfd9378b6` |
| graphics/flip/FL_Flip_04_Hardee.png | `c6c826bd26c0a351a52b449f46d98188225cad0b5e8e383b05168cf8303e6def` |
| graphics/flip/FL_Flip_05_DeSoto.png | `bcd32288b04e900000c6793b62d2db9c36e5a19e652e384ff7d5989b436b58bd` |
| graphics/flip/FL_Flip_06_Hamilton.png | `73e4d9d936e889e8470ce69ae267c0427d6664ffe2fb26a6ee82e44710356c36` |
| graphics/flip/FL_Flip_07_Okeechobee.png | `73be4eadb94dcb1ea3296bc981a41b6662622f69129bb55aa8def70b2882417d` |
| graphics/flip/FL_Flip_08_Glades.png | `b67dd5f7ccc244e3a5f6e6ef39fd9b7c5c4cc5f469a92f37612c2e7469eaf1ff` |
| graphics/flip/FL_Flip_09_Taylor.png | `633464cc37433013bfcc6a136222b5ac9af38833823a5966597d4f0ed6e5dce3` |
| graphics/flip/FL_Flip_10_Madison.png | `96848c05ab491ac85f7bfb10d0e7c9dd7324729bbe13955f1a382e153ccd409e` |
| graphics/guarantee/FL_Guarantee_Clause_1080x1080.png | `b8488d3d13c23f256921df29ef74fa7a36be5f023a6e78df8cbdc02298dc0919` |
| graphics/guarantee/FL_Guarantee_Clause_1600x900.png | `088926e8c69cbe080c207d836139e733e36c8c171cb17007ec98df31acea5bba` |
| graphics/guarantee/X_post.txt | `1c8083d52ba8caece80191868d93e39921a9c2c9950c4e58dbf70f5011b20f11` |

## Output files relabeled *2026 unofficial (Nov 24, 2026)

| File | SHA-256 |
|---|---|
| pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf | `45f24cce7ddfc0bcbac61c3ba3386e3d5417ec88701211727a6dc116433b9f7d` |
| data/florida_governor_2022_2026_by_county.csv | `9c097ed2224ec44dd8ac519a2d0b5ffaf360265d7d7f4505d1e893ca866667fc` |
| data/summary.json | `b9b897510510dbb94222ed7760106dab9d8ee59d027c881feb43e29ea130bd4b` |
| charts/FL_DeltaG_by_County.png | `db5d88bea7cd98eda3cf41cf5c8731d45c2ffe622672623fde4ca72fd4ca6a39` |
| charts/FL_DeltaG_vs_Registration_Drop_Fit.png | `fef24b922ce8e63d958ddef2ea0865a0b74825aacc74e9710fd3955cc95dd349` |
| charts/FL_Over_Ballot_Check.png | `9c06c95134eb1a63912e6c7864a4c3d36ba2f65a3292b1fcde0bdbb79caa4e78` |
| charts/FL_Residual_Bars_by_Ballots.png | `9c3cba7f358583a0245581247c370a718c6f9e9b838e364ecc0163c988a80efd` |
| charts/FL_Slope_G2022_to_G2026.png | `ba6c209c033b5fd27ee95382673a13d9ff7e605e3764cc5d2683073fc9d4db0e` |
| charts/FL_Surplus_Residuals_2022.png | `05ce79cbf08abc8f43bba1c0d695648b3ac8e38aeaaee57f8c77479662f8add0` |
| charts/FL_Surplus_Residuals_2026.png | `b2c3abe7f77fab3f6fa90b425e72c6c8cb5af80a2d4d8c2a637e400f0ca7e3d1` |
| charts/FL_Surplus_S_vs_D_2022.png | `996ada3d8d4605d487da70caa2b0e8b99e9c3b7f1050b4deea9aab81078416a9` |
| charts/FL_Surplus_S_vs_D_2026.png | `b6acea24c4941e6455db4387edf7f5ad66e1eacfdb574cfc056d1f4d6c71cdbc` |

## Kansas-format rebuild files (Nov 24, 2026; *2026 unofficial)

| File | SHA-256 |
|---|---|
| data/FL_Expected_Loss_Residual_Offset_Votes_by_County.csv | `c79bbc9a52ce5043ff828c34600ad9ad1bbaa3c0a32f9fd50209fe7bc4048c76` |
| data/FL_Absentee_Mail_Early_ElectionDay_by_County.csv | `b7839975b58e7f7589bcf16d649f56c9ee961af40f8345bf380d9b7db9da27a7` |
| data/FL_67_County_Voting_Equipment_VerifiedVoting.csv | `d1298d447bd71002a28f9ca9648fa455625b9743565ea8d2468ee15dd2591a9e` |
| graphics/social/FL_Top10_Flip_Counties.csv | `95de424f0ef699bccf456fb78a5c714c64c2142a648277ce94dfd123dcf01d69` |
| letters/Florida_Attorney_General_Letter.pdf | `bbf530e17db015c116e9f20efd92514b15dc61d988e33beadfbe9e325d24022f` |
| letters/Florida_Attorney_General_Letter.docx | `9800d639c24f4b759c6253f2084eb900fc8a85d426101e1ca0d64252c455cac1` |
| downloads/Florida_67_County_SOE_Records_Request_Tracker.xlsx | `00e112e404bb857842d611a68c0601aba1ef5cd28bfde42cf9c10fc935f77590` |
| downloads/Florida_County_to_District_Lookup.csv | `06dae8d24ce1eb5c09494563d1af3844560adb3f3f383c3411205aef08558fee` |
| downloads/Florida_SOE_Letters_All_67_Counties.zip | `ebbd7b673f2cee9a5377a19b2e3e8751314c29535901f31a39f23794ace1384d` |
| downloads/Florida_SOE_Letters_District_1_Southwest.zip | `07c41905a585c9434b002a770456e75e869bb04d5b1f95cb298ed7a6b9e09779` |
| downloads/Florida_SOE_Letters_District_2_Northeast.zip | `80ef090819cbf71831ad4f6464e8416c945deaf2b0b3cf3f5842fcbe988047ea` |
| downloads/Florida_SOE_Letters_District_3_Northwest.zip | `ff629c862ba2c60b31959785c0d3a29325922930bd114c81d0b81241ecd01a02` |
| downloads/Florida_SOE_Letters_District_4_Southeast.zip | `23613c6b5e859c41756a863b97674596600671ed747b8b29848d4f16ec70162e` |
| downloads/Florida_SOE_Letters_District_5_Central.zip | `a532d19ad92aec588c002acbc67ed4b0d30b970e0b6c2cd7fce5a7f1cc1b33e2` |
| downloads/Florida_SOE_Letters_District_6_South.zip | `e79588abf4f061142790bbd9398e8e6a0f3f356d11aa4693cf98d634c8179383` |
| downloads/Florida_SOE_Letters_District_7_West_Central.zip | `a169fd952e77c97e385788f3fd0a9d522e566a327710406eeac69a87f9bb6c25` |
| charts/FL_Slope_G2022_to_G2026_County_Slope_Chart.png | `18e57414236c8b495480b34ce1e82b61925852a986d83afc6cf8250a18633695` |
| charts/FL_Forward_Surplus_Fit_S_vs_D.png | `5a0a7cd062b57cc699fc90eb258bd8c3a9fd60550debc6b8c61f7451997f2be1` |
| charts/FL_DeltaG_Bars_by_Population.png | `23cdc83395eb60b311447f90ac4313cdf296877a4a601c1a5ec4b29893bf60e3` |
| charts/FL_DeltaG_by_Population_Scatter_Names.png | `a07fff2a96d5819c15bc68009c61d5542dc5fd85ff96f86d3e496db915693d6f` |
| charts/FL_Stacked_Share_Reg_Loss_by_2022_Dem_Share.png | `be7e4a1b24b7e6c8599930e817fc95fd30001df09d516584456dba83a44db0eb` |
| charts/FL_Stacked_Share_Reg_Loss_by_Population.png | `bdda622a35fba01c549af5418ea1830c4246403549cd73952a1cf5b81a584e6a` |
| charts/FL_Expected_Loss_Residual_Bars_by_Population.png | `3a5b80633e897f937f27da2e8fe97b3a2170995c24442d24bb0848d7a13c027f` |
| charts/FL_governor_2022_Dem_share_vs_gain_bar_chart.png | `fb0b3bc2d1bb7598284f61a10eccc66e05ed352c58b5fa8452ab3a8db077e1c2` |
| charts/FL_Ceiling_Counties_DeltaG_by_Population.png | `0b4ae056311a6b59063a0b8affc0c6ed61a11923aaa940bb833c2e3a88b85489` |
| charts/FL_Absentee_Mail_Early_ElectionDay_Shares_by_Population.png | `ed26b57a11e86bd1388e0b429903efe13a37cc294ef0a315642a8cc80a96b27b` |
| graphics/social/FL_Top10_Flip_Counties.csv | `95de424f0ef699bccf456fb78a5c714c64c2142a648277ce94dfd123dcf01d69` |
| graphics/social/flip/FL_Flip_01_Liberty.png | `253ec9a3def380a13dd70e8e0a8efe288515a8cc4e2eabccad237ead1975e4b1` |
| graphics/social/flip/FL_Flip_02_Hendry.png | `98ef4b7c6da11881f4095873121611f645118a28bc401f92987490c094f68eb8` |
| graphics/social/flip/FL_Flip_03_Calhoun.png | `5efe8bd31617d6c60c6215d4231c87d2c2d53d637981d19d6bc3975dfd9378b6` |
| graphics/social/flip/FL_Flip_04_Hardee.png | `c6c826bd26c0a351a52b449f46d98188225cad0b5e8e383b05168cf8303e6def` |
| graphics/social/flip/FL_Flip_05_DeSoto.png | `bcd32288b04e900000c6793b62d2db9c36e5a19e652e384ff7d5989b436b58bd` |
| graphics/social/flip/FL_Flip_06_Hamilton.png | `73e4d9d936e889e8470ce69ae267c0427d6664ffe2fb26a6ee82e44710356c36` |
| graphics/social/flip/FL_Flip_07_Okeechobee.png | `73be4eadb94dcb1ea3296bc981a41b6662622f69129bb55aa8def70b2882417d` |
| graphics/social/flip/FL_Flip_08_Glades.png | `b67dd5f7ccc244e3a5f6e6ef39fd9b7c5c4cc5f469a92f37612c2e7469eaf1ff` |
| graphics/social/flip/FL_Flip_09_Taylor.png | `633464cc37433013bfcc6a136222b5ac9af38833823a5966597d4f0ed6e5dce3` |
| graphics/social/flip/FL_Flip_10_Madison.png | `96848c05ab491ac85f7bfb10d0e7c9dd7324729bbe13955f1a382e153ccd409e` |
| graphics/social/guarantee/FL_Guarantee_Clause_1080x1080.png | `b8488d3d13c23f256921df29ef74fa7a36be5f023a6e78df8cbdc02298dc0919` |
| graphics/social/guarantee/FL_Guarantee_Clause_1600x900.png | `088926e8c69cbe080c207d836139e733e36c8c171cb17007ec98df31acea5bba` |
| graphics/social/guarantee/X_post.txt | `1c8083d52ba8caece80191868d93e39921a9c2c9950c4e58dbf70f5011b20f11` |
| graphics/social/summary/FL_Flip_00_Summary_Top10.png | `38d273fa7ce2adf0c22beb207ce58f7143456c2c1e431b5def9c2658b35a367b` |
