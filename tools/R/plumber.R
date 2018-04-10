# plumber.R
library(ParamHelpers)
library(mlrMBO)
is.not.null <- function(x) ! is.null(x)
# Ref: https://stackoverflow.com/questions/17278591/r-integer-key-value-map
new.hashtable <- function() {
  e <- new.env()
  list(set = function(key, value) assign(as.character(key), value, e),
       get = function(key) get(as.character(key), e),
       rm = function(key) rm(as.character(key), e))
}
workflow_table <- new.hashtable()
design_object_table <- new.hashtable()
opt_state_table <- new.hashtable()

#' @post /mlrMBO/initiate
function(req, id, wf){
  if(is.not.null(id) && is.not.null(wf)) {
    workflow_table$set(id, wf)
    initial_design = create_initial_design(id)
    list(
      id,
      initial_design
    )
  } else {
    msg <- "Please provide valid inputs for id and/or workflow."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

#' @post /mlrMBO/createArtifacts
function(req, id) {
  if(is.not.null(id)) {
    wf = workflow_table$get(id)
    des = design_object_table$get(id)
    if(is.not.null(wf) && is.not.null(des)) {
      ctrl = makeMBOControl()
      ctrl = setMBOControlTermination(ctrl, iters=wf$optimizer_iterations)
      acquisition_criteria = create_acquisition_criteria(wf$acquisition_method)
      ctrl = setMBOControlInfill(ctrl, crit = acquisition_criteria)
      opt_state_table$set(id, initSMBO(par.set = wf$params, design = des, control = ctrl, minimize = TRUE, noisy = TRUE))
      list(result=jsonlite::unbox(TRUE))
    } else {
      msg <- "Please first create an initialDesign"
      res$status <- 400 # Bad request
      list(result=jsonlite::unbox(msg))
    }
  } else {
    msg <- "Please provide valid id."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

#' @post /mlrMBO/initialDesign/update
function(req, res, id, initial_design_values){
  if(is.not.null(id)) {
    initial_design = design_object_table$get(id)
    if(is.not.null(initial_design)) {
      if (length(initial_design_values) == nrow(initial_design)) {
        initial_design$y = c(initial_design_values)
        design_object_table$set(id, initial_design)
        list(result=jsonlite::unbox(TRUE))
      } else {
        msg <- "Provide exact number of results for initial design."
        res$status <- 400 # Bad request
        list(result=jsonlite::unbox(msg))
      }
      
    } else {
      msg <- "Please first create initialDesign."
      res$status <- 400 # Bad request
      list(result=jsonlite::unbox(msg))
    }
  } else {
    msg <- "Please provide valid id."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

#' @post /mlrMBO/model/update
function(req, res, id, knobs, value){
  if(is.not.null(id)) {
    opt.state = opt_state_table$get(id)
    if(is.not.null(opt.state) && is.not.null(value)) {
      knobs = data.frame(knobs, stringsAsFactors = FALSE)
      opt.state <- updateSMBO(opt.state, x = knobs, y = value)
      opt_state_table$set(id, opt.state)
      list(result=jsonlite::unbox(TRUE))
    } else {
      msg <- "Please create initialDesign and artifacts first."
      res$status <- 400 # Bad request
      list(result=jsonlite::unbox(msg))
    }
  } else {
    msg <- "Please provide valid id."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

#' @post /mlrMBO/model/getProposedPoint
function(req, res, id) {
  if(is.not.null(id)) {
    opt.state = opt_state_table$get(id)
    if(is.not.null(opt.state) && is.not.null(id)) {
      proposed_points = proposePoints(opt.state)$prop.points
      opt_state_table$set(id, opt.state)
      proposed_points
    } else {
      msg <- "Please create initialDesign and artifacts first."
      res$status <- 400 # Bad request
      list(result=jsonlite::unbox(msg))
    }
  } else {
    msg <- "Please provide valid id."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

#' @post /mlrMBO/finalize
function(req, res, id){
  if(is.not.null(id)) {
    opt_state_table$set(id, NULL)
    workflow_table$set(id, NULL)
    opt_state_table$set(id, NULL)
    list(result=jsonlite::unbox(TRUE))
  } else {
    msg <- "Please create initialDesign and artifacts first."
    res$status <- 400 # Bad request
    list(result=jsonlite::unbox(msg))
  }
}

create_initial_design <- function(id){
  create_knobs(id)
  wf = workflow_table$get(id)
  design_object_table$set(id, generateDesign(wf$optimizer_iterations_in_design, par.set = wf$params))
  design_object_table$get(id)
}

create_knobs <- function(id) {
  wf = workflow_table$get(id)
  optimizer_iterations = wf$optimizer_iterations
  optimizer_iterations_in_design = wf$optimizer_iterations_in_design
  knob_list = list()
  knobs = as.data.frame(wf$knobs)
  
  for(i in 1:nrow(knobs)) {
    row <- knobs[i,]
    # do stuff with row (knob)
    knob_name = row$name
    param = makeNumericParam(id = knob_name, lower = row$min, upper = row$max)
    knob_list[[knob_name]] = param
  }
  wf$params = makeParamSet(params=knob_list)
  workflow_table$set(id, wf)
}

create_acquisition_criteria <- function(acquisition_method) {
  if (identical(acquisition_method, "mr")) {
    makeMBOInfillCritMeanResponse()
  } else if (identical(acquisition_method, "se")) {
    makeMBOInfillCritStandardresult()
  } else if (identical(acquisition_method, "cb")) {
    makeMBOInfillCritCB()
  } else if (identical(acquisition_method, "aei")) {
    makeMBOInfillCritEI()
  } else if (identical(acquisition_method, "eqi")) {
    makeMBOInfillCritEQI()
  } else {
    makeMBOInfillCritEI()
  }
}

