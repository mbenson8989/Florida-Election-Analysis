# Only the list of output field names is shared (no parsing or math is shared between passes).
FIELDS_INT = ['dem22','govtot22','rep22','ballots22','demreg22','totreg22',
              'dem26','govtot26','rep26','ballots26','demreg26','totreg26',
              'dem_chg','ballots_chg','demreg_chg','totreg_chg']
FIELDS_FRAC = ['S22','S26','R22','R26','G22','G26','dG','drop','resid_regloss',
               'implied_regloss','dem_chg_pct','ballots_chg_pct','demreg_chg_pct',
               'fit_pred','fit_resid','implied_fit','DR_over_ballots22','DR_over_ballots26',
               'gov_over_ballots22','gov_over_ballots26',
               'sfit_pred22','sfit_res22','sfit_pred26','sfit_res26']
