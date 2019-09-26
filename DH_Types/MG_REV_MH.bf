LoadFunctionLibrary("../codon.bf");
LoadFunctionLibrary("../DNA.bf");
LoadFunctionLibrary("../parameters.bf");
LoadFunctionLibrary("../frequencies.bf");
LoadFunctionLibrary("../../UtilityFunctions.bf");
LoadFunctionLibrary("MG_REV.bf");

/** @module models.codon.MG_REV_MH */

/**
 * @name models.codon.MG_REV_MH.ModelDescription
 * @param {String} type
 * @param {String} code
 */
lfunction models.codon.MG_REV_MH.ModelDescription(type, code) {

    // piggy-back on the standard MG_REV model for most of the code

    mg_base = models.codon.MG_REV.ModelDescription (type, code);
    mg_base[utility.getGlobalValue("terms.description")] = "The Muse-Gaut 94 codon-substitution model coupled with the general time reversible (GTR) model of nucleotide substitution, which allows for two-hit substitutions";
    mg_base[utility.getGlobalValue("terms.model.q_ij")] = "models.codon.MG_REV_MH._GenerateRate";

    return mg_base;
}


lfunction models.codon.MG_REV_MH._GenerateRate(fromChar, toChar, namespace, model_type, model) {
    return models.codon.MG_REV_MH._GenerateRate_generic (fromChar, toChar, namespace, model_type,
    model[utility.getGlobalValue("terms.translation_table")],
        "alpha", utility.getGlobalValue("terms.parameters.synonymous_rate"),
        "beta", utility.getGlobalValue("terms.parameters.nonsynonymous_rate"),
        "omega", utility.getGlobalValue("terms.parameters.omega_ratio"),
        "delta_type1", utility.getGlobalValue("terms.parameters.multiple_hit_rate1"),
        "delta_type2", utility.getGlobalValue("terms.parameters.multiple_hit_rate2")
        );
        }

/**
 * @name models.codon.MG_REV_MH._GenerateRate
 * @param {Number} fromChar
 * @param {Number} toChar
 * @param {String} namespace
 * @param {String} model_type
 * @param {Matrix} _tt - translation table
 */


lfunction models.codon.MG_REV_MH._GenerateRate_generic (fromChar, toChar, namespace, model_type, _tt, alpha, alpha_term, beta, beta_term, omega, omega_term, delta_type1, delta_type2, delta_term1, delta_term2) {

    _GenerateRate.p = {};
    _GenerateRate.diff = models.codon.diff.complete(fromChar, toChar);
    diff_count = utility.Array1D (_GenerateRate.diff);

    if (diff_count == 1 || diff_count == 2) {

        _GenerateRate.p[model_type] = {};
        _GenerateRate.p[utility.getGlobalValue("terms.global")] = {};

        nuc_rate = "";

        for (i = 0; i < diff_count; i += 1) {
            if ((_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.from")] > (_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.to")]) {
                nuc_p = "theta_" + (_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.to")] + (_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.from")];
            } else {
                nuc_p = "theta_" + (_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.from")] +(_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.to")];
            }
            nuc_p = parameters.ApplyNameSpace(nuc_p, namespace);
            (_GenerateRate.p[utility.getGlobalValue("terms.global")])[terms.nucleotideRateReversible((_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.from")], (_GenerateRate.diff[i])[utility.getGlobalValue("terms.diff.to")])] = nuc_p;

            nuc_rate = parameters.AppendMultiplicativeTerm (nuc_rate, nuc_p);
       }


        rate_entry = nuc_rate;

        if (_tt[fromChar] != _tt[toChar]) {
            if (model_type == utility.getGlobalValue("terms.global")) {
                aa_rate = parameters.ApplyNameSpace(omega, namespace);
                (_GenerateRate.p[model_type])[omega_term] = aa_rate;
            } else {
                aa_rate = beta;
                (_GenerateRate.p[model_type])[beta_term] = aa_rate;
            }
            rate_entry += "*" + aa_rate;
        } else {
            if (model_type == utility.getGlobalValue("terms.local")) {
                (_GenerateRate.p[model_type])[alpha_term] = alpha;
                rate_entry += "*" + alpha;
            } else {
                _GenerateRate.p[utility.getGlobalValue("terms.model.rate_entry")] = nuc_rate;
            }


        }

        if (diff_count == 2) {
            //console.log("Position 0 change:" + (_GenerateRate.diff["0"])["position"]);
            //console.log("Position 1 change:" + (_GenerateRate.diff["1"])["position"]);

            aMutation = (_GenerateRate.diff["0"])["position"];
            bMutation = (_GenerateRate.diff["1"])["position"];

            // Meaning, is it position 1 and 2, or position 2 and 3 of a codon which is double mutated
            if (aMutation + 1 == bMutation) {
                //console.log(fromChar + " " + toChar + " DOUBLE HIT - TYPE 1");
                if (model_type == utility.getGlobalValue("terms.global")) {
                    delta_rate = parameters.ApplyNameSpace(delta_type1, namespace);
                    (_GenerateRate.p[model_type])[delta_term1] = delta_rate;
                    rate_entry += "*" + delta_rate;
                } else {
                    (_GenerateRate.p[model_type])[delta_term1] = delta_type1;
                    rate_entry += "*" + delta_rate;
                }

            } else {
                //console.log("DOUBLE HIT - TYPE 2");
                //console.log(fromChar + " " + toChar + " DOUBLE HIT - TYPE 2");
                if (model_type == utility.getGlobalValue("terms.global")) {
                    delta_rate = parameters.ApplyNameSpace(delta_type2, namespace);
                    (_GenerateRate.p[model_type])[delta_term2] = delta_rate;
                    rate_entry += "*" + delta_rate;

                } else {
                    (_GenerateRate.p[model_type])[delta_term2] = delta_type2;
                    rate_entry += "*" + delta_rate;
                }
            }

            /*
            if (model_type == utility.getGlobalValue("terms.global")) {
                delta_rate = parameters.ApplyNameSpace(delta, namespace);
                (_GenerateRate.p[model_type])[delta_term] = delta_rate;
                rate_entry += "*" + delta_rate;

            } else {
                (_GenerateRate.p[model_type])[delta_term] = delta;
                rate_entry += "*" + delta_rate;
            }
            */


        }

        _GenerateRate.p[utility.getGlobalValue("terms.model.rate_entry")] = rate_entry;
    }
    return _GenerateRate.p;
}
