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

## Resources graphics (added Nov 22, 2026)

| File | SHA-256 |
|---|---|
| graphics/flip/FL_Flip_01_Liberty.png | `803db5e8734e62b8f58cc010b2ce7cb1599139d819c09c3163f02ad65a23e054` |
| graphics/flip/FL_Flip_02_Hendry.png | `8905f7272dad355a23337f8822f397075be49b87424e48b40b4eec8c4732f1db` |
| graphics/flip/FL_Flip_03_Calhoun.png | `f38328b911ae1c754ab29f5990a65dada5b4bdd07c504c75acbb52ac9dba8ba4` |
| graphics/flip/FL_Flip_04_Hardee.png | `99bf26d46a9e50eb723b82b43fbe49ce069816ebfeb07e673d0df5d6741ff67b` |
| graphics/flip/FL_Flip_05_DeSoto.png | `dd362848b8f096a2d7587e167513bd8acfe6d2d4ffc9245e65321bd16d1bd826` |
| graphics/flip/FL_Flip_06_Hamilton.png | `42b9a5382dd2c648a95b271417956096a4485f6bbcedf9fccf4183fc57745c90` |
| graphics/flip/FL_Flip_07_Okeechobee.png | `46e544bfef94f2681af0624a28c982e261c8e18fc415a1732624b59424a7c59a` |
| graphics/flip/FL_Flip_08_Glades.png | `209f94288ba13d0c47830028fd0ddd622907616432fd97f313bd21d1fb06b8de` |
| graphics/flip/FL_Flip_09_Taylor.png | `dc5f5bb669ad831ba4b818a1bccd4b81d00c85a725acd16f481865965a11903d` |
| graphics/flip/FL_Flip_10_Madison.png | `bed69a13cf1c50f44a253a6b693a8d8594c17cec367e4fbb8e2830e961928827` |
| graphics/guarantee/FL_Guarantee_Clause_1080x1080.png | `b8488d3d13c23f256921df29ef74fa7a36be5f023a6e78df8cbdc02298dc0919` |
| graphics/guarantee/FL_Guarantee_Clause_1600x900.png | `088926e8c69cbe080c207d836139e733e36c8c171cb17007ec98df31acea5bba` |
| graphics/guarantee/X_post.txt | `1c8083d52ba8caece80191868d93e39921a9c2c9950c4e58dbf70f5011b20f11` |
