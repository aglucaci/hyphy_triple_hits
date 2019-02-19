RequireVersion ("2.3.12");


LoadFunctionLibrary("libv3/all-terms.bf"); // must be loaded before CF3x4
LoadFunctionLibrary("libv3/UtilityFunctions.bf");
LoadFunctionLibrary("libv3/IOFunctions.bf");
LoadFunctionLibrary("libv3/tasks/estimators.bf");
LoadFunctionLibrary("libv3/tasks/alignments.bf");
LoadFunctionLibrary("libv3/models/codon.bf");
LoadFunctionLibrary("libv3/tasks/trees.bf");
LoadFunctionLibrary("libv3/tasks/genetic_code.bf");
LoadFunctionLibrary("modules/io_functions.ibf");
LoadFunctionLibrary("modules/selection_lib.ibf");
LoadFunctionLibrary("libv3/models/codon/MG_REV.bf");
LoadFunctionLibrary("libv3/models/codon/MG_REV_MH.bf");
LoadFunctionLibrary("libv3/models/codon/MG_REV_TRIP.bf");
LoadFunctionLibrary("libv3/convenience/math.bf");

utility.SetEnvVariable ("NORMALIZE_SEQUENCE_NAMES", TRUE);

fitter.analysis_description = {terms.io.info : "Fit a codon model to a sequence alignment (fixed tree) and report the fit and parameter values",
                           terms.io.version : "0.1",
                           terms.io.authors : "Sergei L Kosakovsky Pond",
                           terms.io.contact : "spond@temple.edu",
                           terms.io.requirements : "in-frame codon alignment and a phylogenetic tree"
                          };

io.DisplayAnalysisBanner (fitter.analysis_description);

fitter.json = {};

namespace fitter {
    LoadFunctionLibrary ("modules/shared-load-file.bf");
    load_file ({utility.getGlobalValue("terms.prefix"): "fitter", utility.getGlobalValue("terms.settings") : {utility.getGlobalValue("terms.settings.branch_selector") : "selection.io.SelectAllBranches"}});
}

namespace fitter {
    doGTR ("fitter");
}

io.ReportProgressMessageMD ("fitter", "codon-fit", "Fitting the codon model");


utility.SetEnvVariable ("VERBOSITY_LEVEL", 1);


fitter.partitioned_one_hit_results =  estimators.FitCodonModel (fitter.filter_names, fitter.trees, "models.codon.MG_REV.ModelDescription", fitter.codon_data_info [utility.getGlobalValue("terms.code")],
 {
    utility.getGlobalValue("terms.run_options.model_type"): utility.getGlobalValue("terms.global"),
    utility.getGlobalValue("terms.run_options.retain_lf_object"): TRUE
}, fitter.gtr_results);


utility.Extend (fitter.gtr_results[terms.global],
                {
                    terms.parameters.multiple_hit_rate : { utility.getGlobalValue ("terms.fit.MLE") : 0.05, terms.fix : FALSE},
                    terms.parameters.triple_hit_rate : { utility.getGlobalValue ("terms.fit.MLE") : 0.05, terms.fix : FALSE}

                });

fitter.partitioned_two_hit_results =  estimators.FitCodonModel (fitter.filter_names, fitter.trees, "models.codon.MG_REV_MH.ModelDescription", fitter.codon_data_info [utility.getGlobalValue("terms.code")],
 {
    utility.getGlobalValue("terms.run_options.model_type"): utility.getGlobalValue("terms.global"),
    utility.getGlobalValue("terms.run_options.retain_lf_object"): TRUE
}, fitter.gtr_results);

fitter.partitioned_codon_results = estimators.FitCodonModel (fitter.filter_names, fitter.trees, "models.codon.MG_REV_TRIP.ModelDescription", fitter.codon_data_info [utility.getGlobalValue("terms.code")], {
    utility.getGlobalValue("terms.run_options.model_type"): utility.getGlobalValue("terms.global"),
    utility.getGlobalValue("terms.run_options.retain_lf_object"): TRUE
    //utility.getGlobalValue("terms.run_options.retain_lf_object"): keep_lf,
    // utility.getGlobalValue("terms.run_options.retain_model_object"): keep_model
}, fitter.gtr_results);

io.ReportProgressMessageMD("fitter", "codon-fit", "* " + selection.io.report_fit (fitter.partitioned_codon_results, 0, (^"fitter.codon_data_info")[utility.getGlobalValue ("terms.data.sample_size")]));

console.log ("\n Single Hit Results: \n");

utility.ForEachPair (fitter.partitioned_one_hit_results[terms.global], "_p_", "_v_",
'
    console.log (_p_ + " => " + _v_ [terms.fit.MLE]);

');

console.log ("\n Double Hit Results: \n");

utility.ForEachPair (fitter.partitioned_two_hit_results[terms.global], "_p_", "_v_",
'
    console.log (_p_ + " => " + _v_ [terms.fit.MLE]);

');


console.log ("\n Triple Hit Results: \n");
utility.ForEachPair (fitter.partitioned_codon_results[terms.global], "_p_", "_v_",
'
    console.log (_p_ + " => " + _v_ [terms.fit.MLE]);

');




//Export(lf_serialized, ^(fitter.partitioned_codon_results[terms.likelihood_function]));
//fprintf(stdout, lf_serialized, "\n");

// ^ dereferences the name supplied by the namespace.model[terms.likelihood_function]));

fitter.triple_hit_distribution = {terms.parameters.omega_ratio : ((fitter.partitioned_codon_results[terms.global])[terms.parameters.omega_ratio])[terms.fit.MLE],
			       	  terms.parameters.multiple_hit_rate : ((fitter.partitioned_codon_results[terms.global])[terms.parameters.multiple_hit_rate])[terms.fit.MLE],
			       	  terms.parameters.triple_hit_rate: ((fitter.partitioned_codon_results[terms.global])[terms.parameters.triple_hit_rate])[terms.fit.MLE]
			       			       	 };

fitter.one_hit_distribution = {terms.parameters.omega_ratio : ((fitter.partitioned_one_hit_results[terms.global])[terms.parameters.omega_ratio])[terms.fit.MLE],
			       	  terms.parameters.multiple_hit_rate : ((fitter.partitioned_one_hit_results[terms.global])[terms.parameters.multiple_hit_rate])[terms.fit.MLE],
			       	  terms.parameters.triple_hit_rate: ((fitter.partitioned_one_hit_results[terms.global])[terms.parameters.triple_hit_rate])[terms.fit.MLE]
			       			       	 };

fitter.two_hit_distribution = {terms.parameters.omega_ratio : ((fitter.partitioned_two_hit_results[terms.global])[terms.parameters.omega_ratio])[terms.fit.MLE],
			       	  terms.parameters.multiple_hit_rate : ((fitter.partitioned_two_hit_results[terms.global])[terms.parameters.multiple_hit_rate])[terms.fit.MLE],
			       	  terms.parameters.triple_hit_rate: ((fitter.partitioned_two_hit_results[terms.global])[terms.parameters.triple_hit_rate])[terms.fit.MLE]
			       			       	 };


/* json output is the likelihood function for each model. */

selection.io.json_store_lf (fitter.json,
                          "Single hit model",
                           fitter.partitioned_one_hit_results[terms.fit.log_likelihood],
                           fitter.partitioned_one_hit_results[terms.parameters] + 9, // +9 comes from CF3x4
                           fitter.sample_size,
                           fitter.one_hit_distribution,
                           1);

selection.io.json_store_lf (fitter.json,
                         "Double hit model",
                          fitter.partitioned_two_hit_results[terms.fit.log_likelihood],
                          fitter.partitioned_two_hit_results[terms.parameters] + 9, // +9 comes from CF3x4
                          fitter.sample_size,
                          fitter.two_hit_distribution,
                          2);


 selection.io.json_store_lf (fitter.json,
			                     "Triple hit model",
                            fitter.partitioned_codon_results[terms.fit.log_likelihood],
                            fitter.partitioned_codon_results[terms.parameters] + 9, // +9 comes from CF3x4
                            fitter.sample_size,
                            fitter.triple_hit_distribution,
                            3);

//io.SpoolJSON (fitter.json, fitter.codon_data_info [terms.json.json]);
io.SpoolJSON (fitter.json, "MG_REV_TRIP_test.json");
return fitter.json;
