#pragma once

#include "clam/crab/crab_cfg.hh"
#include "crab/config.h"
#include "crab/domains/linear_constraints.hpp"                     
#include "crab/domains/intervals.hpp"                      
#include "crab/domains/dis_intervals.hpp"                      
#include "crab/domains/split_dbm.hpp"
#include "crab/domains/boxes.hpp"
#ifdef HAVE_APRON
#include "crab/domains/apron_domains.hpp"
#else 
#include "crab/domains/elina_domains.hpp"
#endif 
#include "crab/domains/array_smashing.hpp"
#include "crab/domains/term_equiv.hpp"
#include "crab/domains/flat_boolean_domain.hpp"
#include "crab/domains/combined_domains.hpp"
#include "crab/domains/wrapped_interval_domain.hpp"
//#include "crab/domains/array_sparse_graph.hpp"
//#include "crab/domains/nullity.hpp"

/*
   Definition of the abstract domains (no instantiation done here)
*/

namespace clam {

  using namespace crab::domains;
  using namespace ikos;

  /* BEGIN MACROS only for internal use */
  // The base numerical domain 
  #define BASE(DOM) base_ ## DOM
  // Array functor domain where the base domain is a reduced product
  // of a boolean domain with the numerical domain DOM.
  #define ARRAY_BOOL_NUM(DOM) \
    typedef array_smashing<flat_boolean_numerical_domain<BASE(DOM)>> DOM
  // Array functor domain where the base domain is DOM
  #define ARRAY_NUM(DOM) \
    typedef array_smashing<BASE(DOM)> DOM;
  /* END MACROS only for internal use */
  
  //////
  //  Non-array smashing domains
  /////

  // Intervals
  typedef interval_domain<number_t, varname_t> interval_domain_t;
  // Wrapped Interval Domain
  typedef wrapped_interval_domain<number_t, varname_t> wrapped_interval_domain_t;
  // Zones using sparse DBMs in split normal form
  typedef SplitDBM<number_t, varname_t> split_dbm_domain_t;
  // Boxes
  typedef boxes_domain<number_t, varname_t> boxes_domain_t;
  // Disjunctive Intervals
  typedef dis_interval_domain<number_t, varname_t> dis_interval_domain_t;
  #ifdef HAVE_APRON
  typedef apron_domain<number_t, varname_t, apron_domain_id_t::APRON_OCT> oct_domain_t;
  typedef apron_domain<number_t, varname_t, apron_domain_id_t::APRON_PK> pk_domain_t;
  #else
  typedef elina_domain<number_t, varname_t, elina_domain_id_t::ELINA_OCT> oct_domain_t;
  typedef elina_domain<number_t, varname_t, elina_domain_id_t::ELINA_PK> pk_domain_t;
  #endif
  // Reduced product of intervals and congruences
  typedef numerical_congruence_domain<interval_domain_t> ric_domain_t;
  /// Term functor domain with Intervals (VMCAI'16)
  typedef crab::cfg::var_factory_impl::str_var_alloc_col::varname_t str_varname_t;
  typedef interval_domain<number_t, str_varname_t> str_interval_dom_t;
  typedef term::TDomInfo<number_t, varname_t, str_interval_dom_t> idom_info;
  typedef term_domain<idom_info> term_int_domain_t;
  /// -- Term functor domain with DisIntervals (VMCAI'16)
  typedef dis_interval_domain<number_t, str_varname_t> str_dis_interval_dom_t;
  typedef term::TDomInfo<number_t, varname_t, str_dis_interval_dom_t> dis_idom_info;
  typedef term_domain<dis_idom_info> term_dis_int_domain_t;
  // Reduced product of Term(DisIntervals) with split zones
  typedef reduced_numerical_domain_product2<term_dis_int_domain_t, split_dbm_domain_t,
					    reduced_product_impl::term_dbm_params> num_domain_t;



  //////
  // Array Smashing Base domains
  //////

  /// -- Flat boolean domain
  typedef flat_boolean_domain<number_t, varname_t> boolean_domain_t;

  /// -- Intervals
  typedef interval_domain<number_t, varname_t> BASE(arraySmashing_interval_domain_t);
  // // -- enable apron version for more precise backward operations
  // typedef apron_domain<number_t, varname_t, apron_domain_id_t::APRON_INT>
  // BASE(interval_domain_t);
  /// -- Wrapped interval domain (APLAS'12)
  typedef wrapped_interval_domain<number_t, varname_t> BASE(arraySmashing_wrapped_interval_domain_t);
  /// -- Zones using sparse DBMs in split normal form (SAS'16)
  typedef SplitDBM<number_t, varname_t> BASE(arraySmashing_split_dbm_domain_t);
  /// -- Boxes
  typedef boxes_domain<number_t, varname_t> BASE(arraySmashing_boxes_domain_t);
  // typedef diff_domain<flat_boolean_numerical_domain<BASE(interval_domain_t)>,
  // 		         boxes_domain<number_t, varname_t> > BASE(boxes_domain_t);
  /// -- DisIntervals
  typedef dis_interval_domain <number_t, varname_t> BASE(arraySmashing_dis_interval_domain_t);
  #ifdef HAVE_APRON
  /// -- Apron domains
  typedef apron_domain<number_t, varname_t, apron_domain_id_t::APRON_OCT>
  BASE(arraySmashing_oct_domain_t);
  typedef apron_domain<number_t, varname_t, apron_domain_id_t::APRON_PK>
  BASE(arraySmashing_pk_domain_t);
  #else
  /// -- Elina domains
  typedef elina_domain<number_t, varname_t, elina_domain_id_t::ELINA_OCT>
  BASE(arraySmashing_oct_domain_t);
  typedef elina_domain<number_t, varname_t, elina_domain_id_t::ELINA_PK>
  BASE(arraySmashing_pk_domain_t);
  #endif 
  /// -- Reduced product of intervals with congruences
  typedef numerical_congruence_domain<BASE(arraySmashing_interval_domain_t)> BASE(arraySmashing_ric_domain_t);
  /// -- Term functor domain with Intervals (VMCAI'16)
  typedef crab::cfg::var_factory_impl::str_var_alloc_col::varname_t str_varname_t;
  typedef interval_domain<number_t, str_varname_t> str_interval_dom_t;
  typedef term::TDomInfo<number_t, varname_t, str_interval_dom_t> idom_info;
  typedef term_domain<idom_info> BASE(arraySmashing_term_int_domain_t);
  /// -- Term functor domain with DisIntervals (VMCAI'16)
  typedef dis_interval_domain<number_t, str_varname_t> str_dis_interval_dom_t;
  typedef term::TDomInfo<number_t, varname_t, str_dis_interval_dom_t> dis_idom_info;
  typedef term_domain<dis_idom_info> BASE(arraySmashing_term_dis_int_domain_t);
  /// -- Reduced product of Term(DisIntervals) with split zones
  typedef reduced_numerical_domain_product2<BASE(arraySmashing_term_dis_int_domain_t),
					    BASE(arraySmashing_split_dbm_domain_t),
					    reduced_product_impl::term_dbm_params> BASE(arraySmashing_num_domain_t);

  //ARRAY_BOOL_NUM(interval_domain_t);
  //ARRAY_BOOL_NUM(split_dbm_domain_t);
  //ARRAY_BOOL_NUM(dis_interval_domain_t);
  //ARRAY_BOOL_NUM(oct_domain_t);
  //ARRAY_BOOL_NUM(pk_domain_t);
  //ARRAY_BOOL_NUM(ric_domain_t);
  //ARRAY_BOOL_NUM(term_int_domain_t);  
  //ARRAY_BOOL_NUM(term_dis_int_domain_t);  
  //ARRAY_BOOL_NUM(num_domain_t);
  // Boxes can reason natively about booleans so that's why we don't
  // combine it with a boolean domain.
  //ARRAY_NUM(boxes_domain_t);
  /* domains that preserve machine arithmetic semantics */
  //ARRAY_BOOL_NUM(wrapped_interval_domain_t);


  ARRAY_NUM(arraySmashing_interval_domain_t);
  ARRAY_NUM(arraySmashing_split_dbm_domain_t);
  ARRAY_NUM(arraySmashing_dis_interval_domain_t); 
  ARRAY_NUM(arraySmashing_oct_domain_t);
  ARRAY_NUM(arraySmashing_pk_domain_t);
  ARRAY_NUM(arraySmashing_ric_domain_t);
  ARRAY_NUM(arraySmashing_term_int_domain_t);  
  ARRAY_NUM(arraySmashing_term_dis_int_domain_t);
  ARRAY_NUM(arraySmashing_num_domain_t);
  ARRAY_NUM(arraySmashing_wrapped_interval_domain_t);
  ARRAY_NUM(arraySmashing_boxes_domain_t);
  
} // end namespace crab-llvm
