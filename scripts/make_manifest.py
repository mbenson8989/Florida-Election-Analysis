import hashlib, json, os
RAW='/workspace/florida/raw'
# url, download time (box-local America/Chicago, from the curl/date logs of this session), notes
M = {
 'fl_results_20221108_extract.txt': ('POST https://results.elections.myflorida.com/ResultsExtract.Asp (ElectionDate=11/8/2022, OfficialResults=Y, PartyRaces=N)', '2026-11-20T04:28:07-06:00', '2022 General, all races, county level, tab-delimited, OFFICIAL. Pass 1 source for 2022 governor votes.'),
 'results_11-8-2022.txt': ('https://results.elections.myflorida.com/downloadresults.asp?ElectionDate=11/8/2022&DATAMODE=', '2026-11-20T04:27:30-06:00', 'Extract utility form page (HTML) showing field layout; not data.'),
 'fl_gov_detail_20221108.html': ('https://results.elections.myflorida.com/DetailRpt.Asp?ELECTIONDATE=11/8/2022&RACE=GOV&PARTY=&DIST=&GRP=&DATAMODE=', '2026-11-20T04:32:10-06:00', '2022 Governor county detail report, "Official Results". Pass 2 source for 2022 governor votes; Total row = DOE statewide totals.'),
 'fl_turnout_20221108.html': ('https://results.elections.myflorida.com/TurnoutRpt.asp?ElectionDate=11/8/2022&DATAMODE=', '2026-11-20T04:31:39-06:00', '2022 General "Voter Registration and Turnout" by county, Official Results. Turnout = ballots cast (both passes, different parsers).'),
 'home_results.html': ('https://results.elections.myflorida.com/', '2026-11-20T04:28:30-06:00', 'Results archive home (frameset). Election list (ElectionRaces.asp) shows no 2026 General entry; 11/3/2026 extract returned header only.'),
 '20261103_ElecResultsFL.txt': ('https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.txt?v=52821560', '2026-11-20T04:29:20-06:00', '2026 General results, all races, county, tab-delimited (linked from floridaelectionwatch.gov/Downloads). Pass 1 source for 2026 governor votes. Fetched with curl -k: server sends GoDaddy R1 root not in box CA bundle (chain inspected: *.floridados.gov <- GoDaddy TLS Intermediate CA DV - R1v1 <- GoDaddy TLS Root CA - R1).'),
 '20261103_ElecResultsFL.xls': ('https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.xls?v=52821560', '2026-11-20T04:29:21-06:00', 'Byte-identical to the .txt (same md5); kept for completeness, not used.'),
 '20261103_ElecResultsFL_PipeDlm_Info.txt': ('https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Info.txt?v=52821560', '2026-11-20T04:29:21-06:00', 'Pipe-delimited info file (races, candidates, units). Pass 2 source (with Votes file). curl -k as above.'),
 '20261103_ElecResultsFL_PipeDlm_Votes.txt': ('https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Votes.txt?v=52821560', '2026-11-20T04:29:21-06:00', 'Pipe-delimited votes file. Pass 2 source for 2026 governor votes. All 670 governor records carry status "I" (Incomplete). curl -k as above.'),
 'ResultsFileLayoutPipeDelimited.pdf': ('https://flelectionfiles.floridados.gov/enightfilespublic/ResultsFileLayoutPipeDelimited.pdf?v=52821560', '2026-11-20T04:29:21-06:00', 'Layout spec for the pipe files.'),
 'few_gov_by_county_2026.html': ('https://floridaelectionwatch.gov/ContestResultsByCounty/160000', '2026-11-20T04:28:49-06:00', '2026 Governor results by county (HTML), page header "Official Election Results". Cross-source check for 2026 governor votes; Total row.'),
 'few_governor_statewide_2026.html': ('https://floridaelectionwatch.gov/StateOffices/Governor', '2026-11-20T04:28:40-06:00', '2026 Governor statewide totals (DOE-reported state total).'),
 'few_CountyReportingStatus.html': ('https://floridaelectionwatch.gov/CountyReportingStatus', '2026-11-20T04:29:00-06:00', '2026 County Reporting Status: Voter Turnout (ballots cast), Eligible Active Registered Voters, completion flags. 2026 ballots cast source (both passes, different parsers).'),
 'few_ElectionDayTurnout.html': ('https://floridaelectionwatch.gov/ElectionDayTurnout', '2026-11-20T04:29:00-06:00', 'Election-day-only turnout, election night (not used for metrics).'),
 'few_Downloads.html': ('https://floridaelectionwatch.gov/Downloads', '2026-11-20T04:29:00-06:00', 'Downloads page linking the 2026 results files.'),
 'few_Timeline.html': ('https://floridaelectionwatch.gov/Timeline', '2026-11-20T04:29:00-06:00', 'Certification timeline (official returns due Nov 16; Canvassing Commission Nov 17, 2026).'),
 'few_home.html': ('https://floridaelectionwatch.gov/', '2026-11-20T04:28:49-06:00', 'Election Watch home; header "2026 General Election November 3, 2026 Official Election Results".'),
 'few_trackcounty_ALA.html': ('https://floridaelectionwatch.gov/TrackCounty/ALA', '2026-11-20T04:28:49-06:00', 'Alachua track page (contest ids).'),
 'bookclosing_2022gen_1_party_by_county.pdf': ('https://files.floridados.gov/media/706001/1-by-party-by-county.pdf', '2026-11-20T04:31:50-06:00', '2022 General book closing (Oct 11, 2022) active registered voters by party by county. Pass 1 source for 2022 registration. No Excel version located for 2022 (media ids 706000-706010 probed).'),
 'bookclosing_2022gen_3_party_by_county_by_race.pdf': ('https://files.floridados.gov/media/706005/3-by-party-by-county-by-race.pdf', '2026-11-20T04:31:50-06:00', '2022 General book closing by party by race. Pass 2 source for 2022 registration (Dem section total; county total = sum of all party sections).'),
 'bookclosing_2026gen_1_party_by_county.xlsx': ('https://dos.fl.gov/media/711453/1-party-by-county.xlsx', '2026-11-20T04:31:50-06:00', '2026 General book closing (Oct 5, 2026) by party by county. Pass 1 source for 2026 registration.'),
 'bookclosing_2026gen_1_party_by_county.pdf': ('https://dos.fl.gov/media/711452/1-party-by-county.pdf', '2026-11-20T04:31:50-06:00', 'Same report as PDF. Pass 2 source for 2026 registration.'),
 'bookclosing_2026gen_3_party_by_county_by_race.xlsx': ('https://dos.fl.gov/media/711457/3-party-by-county-by-race.xlsx', '2026-11-20T04:31:50-06:00', '2026 by party by race (supplementary cross-check).'),
 'dos_bookclosing_page.html': ('https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/bookclosing/', '2026-11-20T04:29:30-06:00', 'Book closing index page (2026 only; 2022 files located via files.floridados.gov).'),
 'dos_voter_turnout_page.html': ('https://dos.fl.gov/elections/data-statistics/elections-data/voter-turnout/', '2026-11-20T04:29:30-06:00', 'Statewide historical turnout page.'),
 'vr_archive_2022.zip': ('https://dos.fl.gov/media/709149/2022-archived.zip', '2026-11-20T04:30:04-06:00', '2022 monthly registration archive (not book closing; not used for metrics).'),
}
out=[]
for f in sorted(os.listdir(RAW)):
    p=os.path.join(RAW,f); b=open(p,'rb').read()
    u,t,n=M.get(f,('?','?','UNLISTED'))
    import datetime
    t=datetime.datetime.fromtimestamp(os.stat(p).st_mtime).astimezone().isoformat(timespec='seconds')
    out.append(dict(file='raw/'+f,url=u,downloaded=t,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),notes=n))
json.dump(out,open('/workspace/florida/MANIFEST.json','w'),indent=1)
with open('/workspace/florida/MANIFEST.md','w') as fh:
    fh.write('# Raw file manifest (Florida audit)\n\nDownload time = file write time on the box, America/Chicago (CST, UTC-6).\n\n| File | Source URL | Downloaded (CST) | Bytes | SHA-256 | Notes |\n|---|---|---|---|---|---|\n')
    for r in out: fh.write(f"| {r['file']} | {r['url']} | {r['downloaded']} | {r['bytes']} | `{r['sha256'][:16]}…` | {r['notes']} |\n")
print([r['file'] for r in out if r['notes']=='UNLISTED'])
